import os
from datetime import date
from RENTAL_OBJECT.rental_object import Rental
from VEHICLES.vehicle import vehicle_from_csv_line
from USERS.CLIENTS.clients import client_from_csv_line
from USERS.ADMINS.admins import admin_from_csv_line
from custom_exceptions import (
    ClientAlreadyExists,
    ClientNotFound,
    WorkerAlreadyExists,
    WorkerNotFound,
    RentalAlreadyExists,
    RentalNotFound,
    VehicleAlreadyRegistered,
    VehicleNotFound
)

class ShopManagement:
    def __init__(self, csv_path="DATABASE/rentals.csv",vehicles_csv_path="DATABASE/vehicles.csv",clients_csv_path="DATABASE/clients.csv",workers_csv_path="DATABASE/admins.csv"):
        self.__clients = []
        self.__workers = []
        self.__rentals = []
        self.__vehicles = []
        self.__csv_path = csv_path
        self.__vehicles_csv_path = vehicles_csv_path
        self.__clients_csv_path = clients_csv_path
        self.__workers_csv_path = workers_csv_path

    def get_clients(self):
        return self.__clients

    def get_workers(self):
        return self.__workers

    def get_rentals(self):
        return self.__rentals

    def add_client(self, client):
        for c in self.__clients:
            if c.get_id() == client.get_id():
                raise ClientAlreadyExists()

        for w in self.__workers:
            if w.get_id() == client.get_id():
                raise ClientAlreadyExists()

        self.__clients.append(client)

    def add_worker(self, worker):
        for w in self.__workers:
            if w.get_id() == worker.get_id():
                raise WorkerAlreadyExists()

        for c in self.__clients:
            if c.get_id() == worker.get_id():
                raise WorkerAlreadyExists()

        self.__workers.append(worker)

    def add_rental(self, rental):
        for r in self.__rentals:
            if r.get_rental_id() == rental.get_rental_id():
                raise RentalAlreadyExists()
        self.__rentals.append(rental)

    def find_client(self, client_id):
        for c in self.__clients:
            if c.get_id() == client_id:
                return c
        raise ClientNotFound()

    def find_worker(self, worker_id):
        for w in self.__workers:
            if w.get_id() == worker_id:
                return w
        raise WorkerNotFound()

    def find_rental(self, rental_id):
        for r in self.__rentals:
            if r.get_rental_id() == rental_id:
                return r
        raise RentalNotFound()
    
    def find_vehicle(self, license_plate):
        for vehicle in self.__vehicles:
            if vehicle.get_license_plate() == license_plate:
                return vehicle
        raise VehicleNotFound()

    def remove_rental(self, rental_id):
        for r in self.__rentals:
            if r.get_rental_id() == rental_id:
                self.__rentals.remove(r)
                return
        raise RentalNotFound()

    def get_active_rentals(self):
        active = []
        for r in self.__rentals:
            if r.is_active():
                active.append(r)
        return active

    def load_rentals_csv(self, vehicle_lookup, user_lookup):
        if not os.path.exists(self.__csv_path):
            return
        f = open(self.__csv_path, "r")
        lines = f.readlines()
        f.close()

        for i in range(1, len(lines)):
            if lines[i].strip() == "":
                continue
            parts = lines[i].strip().split(",")
            vehicle = vehicle_lookup(parts[1])
            user = user_lookup(int(parts[2]))
            rental = Rental(parts[0], vehicle, user, date.fromisoformat(parts[3]), date.fromisoformat(parts[4]), int(parts[5]), parts[7], int(parts[6]))
            self.__rentals.append(rental)

    def add_vehicle(self, vehicle):
        for existing_vehicle in self.__vehicles:
            if existing_vehicle.get_license_plate() == vehicle.get_license_plate():
                raise VehicleAlreadyRegistered()
        self.__vehicles.append(vehicle)

    def get_vehicles(self):
        return self.__vehicles

    def load_vehicles_csv(self):
        if not os.path.exists(self.__vehicles_csv_path):
            return

        f = open(self.__vehicles_csv_path, "r")
        lines = f.readlines()
        f.close()

        self.__vehicles = []

        for i in range(1, len(lines)):
            if lines[i].strip() == "":
                continue

            vehicle = vehicle_from_csv_line(lines[i])
            self.add_vehicle(vehicle)
            
    def load_clients_csv(self):
        if not os.path.exists(self.__clients_csv_path):
            return

        f = open(self.__clients_csv_path, "r")
        lines = f.readlines()
        f.close()

        self.__clients = []

        for i in range(1, len(lines)):
            if lines[i].strip() == "":
                continue

            client = client_from_csv_line(lines[i], self.__vehicles)
            self.add_client(client)
    
    def load_workers_csv(self):
        if not os.path.exists(self.__workers_csv_path):
            return

        f = open(self.__workers_csv_path, "r")
        lines = f.readlines()
        f.close()

        self.__workers = []

        for i in range(1, len(lines)):
            if lines[i].strip() == "":
                continue

            admin = admin_from_csv_line(lines[i])
            self.add_worker(admin)

    def save_vehicles_csv(self):
        f = open(self.__vehicles_csv_path, "w")
        f.write("type,brand,color,license_plate,model,matriculation_date,mileage,last_maintenance_date,last_maintenance_mileage\n")

        for vehicle in self.__vehicles:
            f.write(vehicle.to_csv_line() + "\n")

        f.close()

    def save_rentals_csv(self):
        f = open(self.__csv_path, "w")
        f.write("rental_id,license_plate,user_id,start,end,kms_allowed,kms_done,assurance\n")
        for r in self.__rentals:
            f.write(r.to_csv_line() + "\n")
        f.close()
        

    def save_clients_csv(self):
        f = open(self.__clients_csv_path, "w")
        f.write("id,name,date_of_birth,vehicles\n")

        for client in self.__clients:
            f.write(client.to_csv_line() + "\n")

        f.close()


    def save_workers_csv(self):
        f = open(self.__workers_csv_path, "w")
        f.write("id,name,date_of_birth,role\n")

        for worker in self.__workers:
            f.write(worker.to_csv_line() + "\n")

        f.close()

    def save_all_csv(self):
        self.save_vehicles_csv()
        self.save_clients_csv()
        self.save_workers_csv()
        self.save_rentals_csv()
        
    def load_all_csv(self):
        self.load_vehicles_csv()
        self.load_clients_csv()
        self.load_workers_csv()
        self.load_rentals_csv(self.find_vehicle, self.find_client)