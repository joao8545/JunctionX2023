class Patient:
    def __init__(self,name,surname,region,n_fractions) -> None:
        self.name=name
        self.surname=surname
        self.region=region
        self.n_fractions=n_fractions
        self.ntfy_topic=None
        self.full_name=" ".join([name, surname])
        self.appointments={}
        pass
    def __repr__(self) -> str:
        return f"My name is {self.name} {self.surname}. I need {self.n_fractions} for {self.region}\n"
    def add_topic(self,topic):
        self.ntfy_topic=topic

class Machine:
    def __init__(self,machine_type) -> None:
        pass
    
class Appointment:
    def __init__(self,id,start_time) -> None:
        pass
