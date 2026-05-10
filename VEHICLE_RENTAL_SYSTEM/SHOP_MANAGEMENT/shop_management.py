from custom_exceptions import VehicleAlreadyRegistered

class ShopManagement:
    def __init__(self):
        self.__vehicles = []

    def add_vehicle(self, vehicle):
        for existing_vehicle in self.__vehicles:
            if existing_vehicle.get_license_plate() == vehicle.get_license_plate():
                raise VehicleAlreadyRegistered()
        self.__vehicles.append(vehicle)

    def get_vehicles(self):
        return self.__vehicles
        
