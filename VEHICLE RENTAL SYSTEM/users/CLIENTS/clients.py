from users import User
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
                v.update_info(kms)
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