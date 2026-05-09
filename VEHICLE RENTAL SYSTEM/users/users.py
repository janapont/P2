from abc import ABC, abstractmethod
from datetime import date
from exceptions import InvalidName, InvalidDateOfBirth

class User(ABC):
    __counter = 0

    def __init__(self, name, date_of_birth):
        self.validate_name(name)
        self.validate_date_of_birth(date_of_birth)
        User.__counter += 1
        self.__name = name
        self.__date_of_birth = date_of_birth
        self.__id = User.__counter

    def get_name(self):
        return self.__name

    def get_date_of_birth(self):
        return self.__date_of_birth

    def get_id(self):
        return self.__id

    def validate_name(self, name):
        if not isinstance(name, str):
            raise InvalidName("Name must be a string.")
        if name.strip() == "":
            raise InvalidName("Name cannot be empty.")

    def validate_date_of_birth(self, date_of_birth):
        if not isinstance(date_of_birth, date):
            raise InvalidDateOfBirth("Date of birth must be a date object.")
        if date_of_birth > date.today():
            raise InvalidDateOfBirth("Date of birth must be in the past.")

    def get_age (self):
        today = date.today()
        age = today.year - self.__date_of_birth.year
        if today.month < self.__date_of_birth.month:
            age -= 1
        elif today.month == self.__date_of_birth.month:
            if today.day < self.__date_of_birth.day:
                age -= 1
        return age
    
    def update_name(self, name):
        self.validate_name(name)
        self.__name = name

    def update_date_of_birth(self, date_of_birth):
        self.validate_date_of_birth(date_of_birth)
        self.__date_of_birth = date_of_birth

    @abstractmethod
    def get_type(self):    # TO APPLY POLYMORPHISM
        pass