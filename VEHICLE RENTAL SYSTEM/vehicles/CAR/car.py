from datetime import date
from vehicles.vehicle import Vehicle

class Car(Vehicle):
    #no cal init

    def calculate_ITV(self):
        matric = self.get_matriculation_date()
        age = self.get_age_years()

        if age < 4: #first 4 years
            return self._add_years(matric, 4)  #next one will be same date + 4 years 
        elif age < 10:
            if (age - 4) % 2 == 0: #després de l'any 4, shaura de fer al 6, 8, 10
                next_year = age + 2
            else:
                next_year = age + 1
            return self._add_years(matric, next_year)
        else:
            return self._add_years(matric, age + 1) #a partir de l'any 10 cada any

    def maintenance_schedule(self): #for cars, maintenance is every year
        matric = self.get_matriculation_date()
        age = self.get_age_years()
        return self._add_years(matric, age + 1) #next maintenance will always be next year