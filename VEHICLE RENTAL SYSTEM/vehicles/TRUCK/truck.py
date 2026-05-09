from VEHICLES.vehicle import Vehicle
from datetime import date

class Truck(Vehicle):

    def calculate_ITV(self):
        matric = self.get_matriculation_date()
        today = date.today()

        # Años 1-10: cada año
        next_itv = self._add_years(matric, 1)
        year_10 = self._add_years(matric, 10)

        while next_itv <= today and next_itv < year_10:
            next_itv = self._add_years(next_itv, 1)

        if next_itv > today:
            return next_itv

        # A partir del año 10: cada 6 meses
        next_itv = year_10
        while next_itv <= today:
            next_itv = self._add_months(next_itv, 6)
        return next_itv
    
    def maintenance_schedule(self):
        last_date = self.get_last_maintenance_date()
        last_km = self.get_last_maintenance_mileage()
        matric = self.get_matriculation_date()

        if last_date is None:
            last_date = matric
            last_km = 0

        next_by_time = self._add_months(last_date, 2)

        if self.get_mileage() - last_km >= 1000:
            return date.today()
        return next_by_time