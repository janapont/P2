"""Motorbike class, inherits from Vehicle."""
from VEHICLES.vehicle import Vehicle
from datetime import date
class Motorbike(Vehicle):
    
    def calculate_ITV(self):
        matric = self.get_matriculation_date()
        today = date.today()

        # Primera ITV: año 4
        next_itv = self._add_years(matric, 4)
        # A partir de ahí, cada 2 años
        while next_itv <= today:
            next_itv = self._add_years(next_itv, 2)
        return next_itv
            
    def maintenance_schedule(self):
        last_date = self.get_last_maintenance_date()
        last_km = self.get_last_maintenance_mileage()
        matric = self.get_matriculation_date()

        if last_date is None:
            last_date = matric
            last_km = 0

        next_by_time = self._add_years(last_date, 1)

        if self.get_mileage() - last_km >= 1000:
            return date.today()   
        return next_by_time