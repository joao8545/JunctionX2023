import os
from pymongo import MongoClient
from data_models import *
import random
from ntfy_wrapper import Notifier
from apscheduler.schedulers.background import BaseScheduler
from datetime import datetime
ntfy = Notifier(topics="patient4")

mongodb_address = os.environ.get("MONGODB_ADDRESS", "mongodb://localhost:27017/")
client = MongoClient(mongodb_address)
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
            patient_storage.insert_one(p.toJSON())
    with open("machines.txt") as file:
        for line in file.readlines()[1:]:
            l=line.split(",")
            sched={}
            for date in ["2023-11-29","2023-11-25","2023-11-24","2023-11-26","2023-11-27","2023-11-28","2023-11-23","2023-11-22","2023-11-21","2023-11-20","2023-11-19"]:
                sched[date]={}
                for h in range(8,18):
                    usage=[]
                    for j in range(12):
                        typed=random.choice(["patient_name","empty","maintenance"])
                        value=typed
                        if typed=="patient_name":
                            value=random.choice(list(patient_storage.find()))['full_name']
                        usage.append(value)
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
            timeline_data[kw].append({'label':f"{hour}:00",'bars':[{'start': (i)*5, 'status': "idle" if data[i]=="empty" else "maintenance" if data[i]=="maintenance" else "patient", 'label': data[i]} for i in range(len(data))]})
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
            break
    return {"slots":response,"bookable":bookable}

def get_machine_schedule_of_day(machine,day):
    return {f"{day}":get_machine_schedule(machine)[day]}

def get_patient_data(full_name):
    pass

def get_appointment(id):
    pass

def add_machine_data(data):
    pass

def add_patient_data(data):
    pass

def create_appointment(patient_name,machine_name,days):

    appointment_storage=db["appointments"]
    patient=db["patients"].find_one({'full_name':patient_name})
    machine=db["machines"].find_one({'name':machine_name})
    ntfy = Notifier(topics=patient['ntfy_topic'])
    ntfy(f"Session in machine {machine_name} scheduled for {days}")
    appointment_storage.insert_one({"patient":patient_name,"machine":machine_name,'days':days.split(",")})
    p=Patient(**patient)
    m=Machine(**machine)
    for d in days.split(","):
        p.appointments[d]=machine
        date="-".join(d.split("-")[:3])
        h=d.split("-")[3]
        h_index=int(h)
        min=int(d.split("-")[4])//5
        #BaseScheduler.add_job(lambda :ntfy(f"Session in machine {machine_name} is about to start"),'date', run_date=datetime(d.split("-")[0], d.split("-")[1], d.split("-")[2], d.split("-")[3], d.split("-")[4], 0))
        for i in range(min,min+int(p.duration//5)):
            index=i
            if index>=12:
                index=i-12
                h_index+=i//12
            m.schedule[date][str(h_index)][index]=p.full_name
    db["patients"].update_one({'full_name': patient_name}, {'$set': p.__dict__})
    db["machines"].update_one({'name': machine_name}, {'$set': m.__dict__})

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
    create_db()