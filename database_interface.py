from pymongo import MongoClient
from data_models import *
import random

client = MongoClient('mongodb://100.90.187.82:27017/')
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
            #patient_storage.insert_one({"name":name, "surname":surname,"fractions":fractions,"region":region,"topic":'patient1','full_name':" ".join([name, surname]), 'appointments':{}})
    with open("machines.txt") as file:
        for line in file.readlines()[1:]:
            l=line.split(",")
            sched={}
            for date in ["2023-11-25","2023-11-24","2023-11-26"]:
                sched[date]={}
                for h in range(8,18):
                    usage=[]
                    for j in range(12):
                        usage.append(random.choice(["patient_name","empty","maintanence"]))
                    sched[date][str(h)]=usage
            machine_storage.insert_one({"name":l[0],"machine_type":l[1],"schedule":sched})

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
            timeline_data[kw].append({'label':f"{hour}:00",'bars':[{'start': (i+1)*5, 'status': "idle" if data[i]=="empty" else "maintenance" if data[i]=="maintanence" else "patient", 'label': data[i]} for i in range(len(data))]})
    #timeline_data=[{'label': '17:00', 'bars': [{'start': 0, 'status': 'patient', 'label': 'joao da silva'}]}]
    #print(timeline_data)
    return timeline_data[kw]

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
    create_db()