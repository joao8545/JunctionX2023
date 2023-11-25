from data_models import *
import random

random.seed(0)

N_PATIENTS=100
with open("names.txt") as file:
    names=file.readlines()
with open("surnames.txt") as file:
    surnames=file.readlines()

with open("data.csv") as file:
    cancer_types=[]
    for line in file.readlines()[1:]:
        cancer_types.append(line.split(";"))

def generate_patients(names,surnames,types,total_patients):
    patients=[]
    for i in range(len(types)):
        quantity=round(float(types[i][-1])*total_patients/100)
        for _ in range(quantity):
            patients.append(Patient(random.choice(names).strip(),random.choice(surnames).strip(),types[i][0],random.choice(types[i][6].split(",")).strip()))
    return patients

patients= generate_patients(names,surnames,cancer_types,N_PATIENTS)
with open("patients.txt","w") as out:
    out.write("name,surname,fractions,region\n")
    for p in patients:
        out.write(f"{p.name},{p.surname},{p.n_fractions},{p.region},\n")
