from pymongo import MongoClient
from data_models import *
import random

client = MongoClient('mongodb://100.90.168.156:27017/')
db=client.Varian

def create_db():
    patient_storage=db["patients"]
    machine_storage=db["machines"]
    with open("patients.txt") as file:
        for line in file.readlines()[1:]:
            l=line.split(",")
            name=l[0]
            surname=l[1]
            fractions=l[2]
            region=l[3]
            p=Patient(name,surname,region,fractions)
            #patient_storage.insert_one(p.toJSON())
    with open("machines.txt") as file:
        for line in file.readlines()[1:]:
            l=line.split(",")
            sched={}
            for date in ["2023-11-29","2023-11-25","2023-11-24","2023-11-26","2023-11-27","2023-11-28"]:
                sched[date]={}
                for h in range(8,18):
                    usage=[]
                    for j in range(12):
                        usage.append(random.choice(["patient_name","empty","maintanence"]))
                    sched[date][str(h)]=usage
            m=Machine(l[0],l[1],schedule=sched)
            machine_storage.insert_one(m.toJSON())

def get_machine_schedule(machine_name):
    machine_storage=db["machines"]
    data=machine_storage.find_one({'name':machine_name})
    sched=data["schedule"]
    timeline_data={}
    for kw in sched.keys():
        daily=sched[kw]
        timeline_data[kw]=[]
        for hour in daily.keys():
            data=daily[hour]
            timeline_data[kw].append({'label':f"{hour}:00",'bars':[{'start': (i)*5, 'status': "idle" if data[i]=="empty" else "maintenance" if data[i]=="maintanence" else "patient", 'label': data[i]} for i in range(len(data))]})
    #timeline_data=[{'label': '17:00', 'bars': [{'start': 0, 'status': 'patient', 'label': 'joao da silva'}]}]
    #print(timeline_data)
    return timeline_data

def get_treatment_info(machine_name,patient_name):
    machine=Machine(**db["machines"].find_one({'name':machine_name}))
    patient=Patient(**db["patients"].find_one({'full_name':patient_name}))
    treatment_info=get_available_periods(machine.name,patient.duration/5,patient.fractions)
    return treatment_info

def get_machine_info(machine):
    machine_storage=db["machines"]
    data=machine_storage.find_one({'name':machine})
    m=Machine(**data)
    data=m.toJSON()
    #data["other_info"]=get_available_periods(machine,3)
    return data

def get_available_periods(machine, num_seg,fract):
    machine_storage=db["machines"]
    data=machine_storage.find_one({'name':machine})
    sched=data["schedule"]
    response=[]
    sequential_days=0
    bookable=False
    for day in sched.keys():
        daily=sched[day]
        sequential_spots=0
        day_complete=False
        for hour in daily.keys():
            if day_complete:
                sequential_days+=1
                break
            data=daily[hour]
            for i in range(len(data)):
                spot=data[i]
                if spot=="empty":
                    if sequential_spots==0:
                        start=f"{day}-{hour}-{i*5}"
                    sequential_spots+=1
                else:
                    sequential_spots=0
                if sequential_spots>=num_seg:
                    response.append(start)
                    day_complete=True
                    break
        if not day_complete:
            sequential_days=0
        if sequential_days>=int(fract):
            bookable= True
    return {"slots":response,"bookable":bookable}



def get_patient_data(full_name):
    pass

def get_appointment(id):
    pass

def add_machine_data(data):
    pass

def add_patient_data(data):
    pass

def add_appointment(id):
    pass

def get_all_patients():
    patients=db["patients"].find()

    return list(map(lambda p: Patient(**p),patients))

def get_all_machines():
    machines=db["machines"].find()
    return list(map(lambda m: Machine(**m),machines))


if __name__ == '__main__':
    pass
    #create_db()