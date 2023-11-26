import json
class Patient:
    def __init__(self,name,surname,region,fractions,ntfy_topic=None,*args,**kwargs) -> None:
        self.name=name
        self.surname=surname
        self.region=region
        self.fractions=fractions
        self.ntfy_topic=ntfy_topic
        self.full_name=" ".join([name, surname])
        self.appointments={}
        if self.ntfy_topic is None:
            self.ntfy_topic=f"{self.name}_{self.surname}_ntfy"
        self.duration=self.get_duration()
    def __repr__(self) -> str:
        return f"My name is {self.name} {self.surname}. I need {self.fractions} for {self.region}\n"
    def add_topic(self,topic):
        self.ntfy_topic=topic

    def get_name(self):
        return self.full_name

    def get_duration(self):
        if self.region in ["Breast","Head & neck","Abdomen","Pelvis","Lung","Lung special"]:
            return 15
        if self.region in ["Crane","Whole Brain"]:
            return 10
        if self.region in ["Breast special"]:
            return 20
        return 30
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4))

class Machine:
    def __init__(self,name,machine_type,schedule={},*args,**kwargs) -> None:
        #schedule={date:{hour:[patient_name|empty|maintenance(x12)]}}
        self.name=name
        self.machine_type=machine_type
        self.schedule=schedule
        self.full_name=self.get_full_name()
    def can_treat(self,region)->bool:
        match self.machine_type:
            case "TB":
                return region in ["Craniospinal","Breast","Breast special","Head & neck","Abdomen","Pelvis","Crane","Lung","Lung special"]
            case "VB":
                return region in ["Breast","Head & neck","Abdomen","Pelvis","Crane","Lung","Lung special","Whole Brain"]
            case "U":
                return region in ["Breast","Whole Brain"]
            case _:
                return False
            
    def get_full_name(self)->str:
        match self.machine_type:
            case "TB":
                return "TrueBeam"
            case "VB":
                return "VitalBeam"
            case "U":
                return "Unique-Clinac"

    def get_name(self):
        return self.name
    
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4))

class Appointment:
    def __init__(self,id,start_time) -> None:
        pass
    
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4))
