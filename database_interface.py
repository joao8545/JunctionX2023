from pymongo import MongoClient
from data_models import *

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
            machine_storage.insert_one({"name":l[0],"machine_type":l[1]})

def get_machine_data(machine_name):
    pass

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

#create_db()