import os
from datetime import date
from RENTAL_OBJECT.rental_object import Rental
from custom_exceptions import (
    ClientAlreadyExists,
    ClientNotFound,
    WorkerAlreadyExists,
    WorkerNotFound,
    RentalAlreadyExists,
    RentalNotFound,
    VehicleAlreadyRegistered
)

class ShopManagement:
    def __init__(self, csv_path="DATABASE/rentals.csv"):
        self.__clients = []
        self.__workers = []
        self.__rentals = []
        self.__vehicles = []
        self.__csv_path = csv_path

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
        self.__clients.append(client)

    def add_worker(self, worker):
        for w in self.__workers:
            if w.get_id() == worker.get_id():
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

    def save_csv(self):
        f = open(self.__csv_path, "w")
        f.write("rental_id,license_plate,user_id,start,end,kms_allowed,kms_done,assurance\n")
        for r in self.__rentals:
            f.write(r.to_csv_line() + "\n")
        f.close()

    def load_csv(self, vehicle_lookup, user_lookup):
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
            rental = Rental(parts[0], vehicle, user, date.fromisoformat(parts[3]), date.fromisoformat(parts[4]), int(parts[5]), parts[7])
            self.__rentals.append(rental)

    def add_vehicle(self, vehicle):
        for existing_vehicle in self.__vehicles:
            if existing_vehicle.get_license_plate() == vehicle.get_license_plate():
                raise VehicleAlreadyRegistered()
        self.__vehicles.append(vehicle)

    def get_vehicles(self):
        return self.__vehicles
        