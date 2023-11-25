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
        pass
    def __repr__(self) -> str:
        return f"My name is {self.name} {self.surname}. I need {self.fractions} for {self.region}\n"
    def add_topic(self,topic):
        self.ntfy_topic=topic
    def get_name(self):
        return self.full_name

class Machine:
    def __init__(self,machine_type) -> None:
        pass
    
class Appointment:
    def __init__(self,id,start_time) -> None:
        pass
