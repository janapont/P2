from VEHICLES.vehicle import Vehicle
from datetime import date


class Car(Vehicle):
    #no cal init

    def calculate_ITV(self):
        matric = self.get_matriculation_date()
        today = date.today()

        # Año 4: primera ITV
        next_itv = self._add_years(matric, 4)
        if next_itv > today:
            return next_itv

        # Años 4-10: cada 2 años (4, 6, 8, 10)
        for year_offset in (6, 8, 10):
            candidate = self._add_years(matric, year_offset)
            if candidate > today:
                return candidate

        # A partir del año 10: cada año
        next_itv = self._add_years(matric, 11)
        while next_itv <= today:
            next_itv = self._add_years(next_itv, 1)
        return next_itv

    def maintenance_schedule(self): #for cars, maintenance is every year
        last_date = self.get_last_maintenance_date()
        matric = self.get_matriculation_date()

        if last_date is None:
            last_date = matric

        return self._add_years(last_date, 1) #next maintenance will always be 1 year after last one