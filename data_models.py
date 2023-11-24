class Patient:
    def __init__(self,name,surname,region,n_fractions) -> None:
        self.name=name
        self.surname=surname
        self.region=region
        self.n_fractions=n_fractions
        pass
    def __repr__(self) -> str:
        return f"My name is {self.name} {self.surname}. I need {self.n_fractions} for {self.region}\n"
