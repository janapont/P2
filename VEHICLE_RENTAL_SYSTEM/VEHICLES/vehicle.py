from abc import ABC, abstractmethod
from custom_exceptions import (
    InvalidLicensePlateError,
    InvalidMatriculationDateError,
    InvalidMileageError,
    MileageCannotDecreaseError,
)

from datetime import date

class Vehicle(ABC):
    def __init__(self, brand, color, license_plate, model, matriculation_date, mileage):
        if not isinstance(license_plate, str):
            raise InvalidLicensePlateError()
        if (len(license_plate) != 7 or not license_plate[:4].isdigit() 
            or not license_plate[4:].isalpha() or not license_plate[4:].isupper()):
            raise InvalidLicensePlateError()
        if not isinstance(mileage, int) or isinstance(mileage, bool) or mileage < 0:
            raise InvalidMileageError()
        if not isinstance(matriculation_date, date) or matriculation_date > date.today():
            raise InvalidMatriculationDateError()
                
        self.__brand = brand
        self.__color = color
        self.__license_plate = license_plate
        self.__model = model
        self.__matriculation_date = matriculation_date
        self.__mileage = mileage
        self.__last_maintenance_date = None      # se actualiza cuando hace mantenimiento
        self.__last_maintenance_mileage = None

    @abstractmethod
    def calculate_ITV(self):
        pass

    @abstractmethod
    def maintenance_schedule(self):
        pass

    def update_info(self, brand=None, color=None, model=None, mileage=None):
        if brand is not None:
            self.__brand = brand
        if color is not None:
            self.__color = color
        if model is not None:
            self.__model = model
        if mileage is not None:
            if not isinstance(mileage, int) or mileage < 0:
                raise InvalidMileageError()
            if mileage < self.__mileage:
                raise MileageCannotDecreaseError()
            self.__mileage = mileage
            
    def get_age_years(self):
        today = date.today()
        matric = self.__matriculation_date
        years = today.year - matric.year
        if (today.month, today.day) < (matric.month, matric.day):
            years -= 1
        return years

    def _add_years(self, base_date, years): #per afegir anys a una data
        try:
            return base_date.replace(year=base_date.year + years)
        except ValueError:
            return base_date.replace(year=base_date.year + years, day=28) #per dies que no existeixen al mes (tots els messos tenen al menys 28)
        
    def _add_months(self, base_date, months): #per afegir mesos a una data
        total = base_date.month - 1 + months
        new_year = base_date.year + total // 12
        new_month = total % 12 + 1
        try:
            return base_date.replace(year=new_year, month=new_month)
        except ValueError:
            return base_date.replace(year=new_year, month=new_month, day=28) #per dies que no existeixen al mes (tots els messos tenen al menys 28)
        
    def register_maintenance(self, d, km):
        self.__last_maintenance_date = d
        self.__last_maintenance_mileage = km

    def get_brand(self):
        return self.__brand

    def get_color(self):
        return self.__color

    def get_license_plate(self):
        return self.__license_plate

    def get_model(self):
        return self.__model

    def get_matriculation_date(self):
        return self.__matriculation_date

    def get_mileage(self):
        return self.__mileage
    
    def get_last_maintenance_date(self):
        return self.__last_maintenance_date
    
    def get_last_maintenance_mileage(self):
        return self.__last_maintenance_mileage