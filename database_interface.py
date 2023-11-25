from pymongo import MongoClient
from data_models import *

client = MongoClient('mongodb://100.90.187.82:27017/')
db=client.Varian

def create_db():
    storage=db["patients"]
    with open("patients.txt") as file:
        for line in file.readlines()[1:]:
            l=line.split(",")
            name=l[0]
            surname=l[1]
            fractions=l[2]
            region=l[3]
            storage.insert_one({"name":name, "surname":surname,"fractions":fractions,"region":region,"topic":'patient1','full_name':" ".join([name, surname]), 'appointments':{}})

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
    print(patients[0])
    return list(map(lambda p: Patient(**p),patients))