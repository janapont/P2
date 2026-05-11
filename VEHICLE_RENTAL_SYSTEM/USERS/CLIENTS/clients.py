from USERS.users import User
from custom_exceptions import VehicleAlreadyRegistered, VehicleNotFound

class Client(User):
    def __init__(self, name, date_of_birth):
        super().__init__(name, date_of_birth)
        self.__vehicles = []

    def get_type(self):
        return "client"

    def get_vehicles(self):
        return list(self.__vehicles)

    def add_vehicle(self, vehicle):
        for v in self.__vehicles:
            if v.get_license_plate() == vehicle.get_license_plate():
                raise VehicleAlreadyRegistered(f"Vehicle {vehicle.get_license_plate()} is already registered.")
        self.__vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        for v in self.__vehicles:
            if v.get_license_plate() == vehicle.get_license_plate():
                self.__vehicles.remove(v)
                return
        raise VehicleNotFound(f"Vehicle with plate {vehicle.get_license_plate()} not found.")

    def update_vehicle_kms(self, license_plate, kms):
        for v in self.__vehicles:
            if v.get_license_plate() == license_plate:
                v.update_info(mileage=kms)
                return
        raise VehicleNotFound(f"Vehicle with plate {license_plate} not found.")

    def get_next_itv(self, license_plate):
        for v in self.__vehicles:
            if v.get_license_plate() == license_plate:
                return v.calculate_ITV()
        raise VehicleNotFound(f"Vehicle with plate {license_plate} not found.")

    def get_next_maintenance(self, license_plate):
        for v in self.__vehicles:
            if v.get_license_plate() == license_plate:
                return v.maintenance_schedule()
        raise VehicleNotFound(f"Vehicle with plate {license_plate} not found.")
    
    def to_csv_line(self):
        plates = []

        for vehicle in self.get_vehicles():
            plates.append(vehicle.get_license_plate())

        plates_text = "|".join(plates)

        return (
            f"{self.get_id()},"
            f"{self.get_name()},"
            f"{self.get_date_of_birth().isoformat()},"
            f"{plates_text}"
        )
    


def client_from_csv_line(line, vehicles):
    from datetime import date
    parts = line.strip().split(",")

    name = parts[0]
    date_of_birth = date.fromisoformat(parts[1])
    user_id = parts[2]

    client = Client(name, date_of_birth, user_id)

    if len(parts) > 3 and parts[3] != "":
        plates = parts[3].split("|")

        for plate in plates:
            for vehicle in vehicles:
                if vehicle.get_license_plate() == plate:
                    client.add_vehicle(vehicle)

    return client