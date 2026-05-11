"""Unit tests for the ShopManagement class."""
import os
import tempfile
import unittest
from datetime import date, timedelta

from custom_exceptions import (
    ClientAlreadyExists,
    ClientNotFound,
    WorkerAlreadyExists,
    WorkerNotFound,
    RentalAlreadyExists,
    RentalNotFound,
    VehicleAlreadyRegistered,
    VehicleNotFound,
)
from SHOP_MANAGEMENT.shop_management import ShopManagement
from RENTAL_OBJECT.rental_object import Rental
from USERS.CLIENTS.clients import Client
from USERS.ADMINS.admins import Admin
from VEHICLES.CAR.car import Car
from VEHICLES.MOTORBIKE.motorbike import Motorbike
from VEHICLES.TRUCK.truck import Truck


class TestShopManagementSetup(unittest.TestCase):

    def test_new_shop_starts_empty(self):
        shop = ShopManagement()

        self.assertEqual(shop.get_clients(), [])
        self.assertEqual(shop.get_workers(), [])
        self.assertEqual(shop.get_rentals(), [])
        self.assertEqual(shop.get_vehicles(), [])


class TestShopManagementClients(unittest.TestCase):

    def setUp(self):
        self.shop = ShopManagement()

    def test_add_client(self):
        client = Client("Anna", date(2000, 1, 1), 1)

        self.shop.add_client(client)

        self.assertIn(client, self.shop.get_clients())

    def test_cannot_add_two_clients_with_same_id(self):
        client1 = Client("Anna", date(2000, 1, 1), 1)
        client2 = Client("Marc", date(2001, 1, 1), 1)

        self.shop.add_client(client1)

        with self.assertRaises(ClientAlreadyExists):
            self.shop.add_client(client2)

    def test_cannot_add_client_with_same_id_as_worker(self):
        worker = Admin("Worker", date(1990, 1, 1), "mechanic", 1)
        client = Client("Anna", date(2000, 1, 1), 1)

        self.shop.add_worker(worker)

        with self.assertRaises(ClientAlreadyExists):
            self.shop.add_client(client)

    def test_find_client(self):
        client = Client("Anna", date(2000, 1, 1), 1)
        self.shop.add_client(client)

        self.assertEqual(self.shop.find_client(1), client)

    def test_find_client_not_found(self):
        with self.assertRaises(ClientNotFound):
            self.shop.find_client(99)


class TestShopManagementWorkers(unittest.TestCase):

    def setUp(self):
        self.shop = ShopManagement()

    def test_add_worker(self):
        worker = Admin("Worker", date(1990, 1, 1), "mechanic", 1)

        self.shop.add_worker(worker)

        self.assertIn(worker, self.shop.get_workers())

    def test_cannot_add_two_workers_with_same_id(self):
        worker1 = Admin("Worker", date(1990, 1, 1), "mechanic", 1)
        worker2 = Admin("Admin", date(1991, 1, 1), "administrator", 1)

        self.shop.add_worker(worker1)

        with self.assertRaises(WorkerAlreadyExists):
            self.shop.add_worker(worker2)

    def test_cannot_add_worker_with_same_id_as_client(self):
        client = Client("Anna", date(2000, 1, 1), 1)
        worker = Admin("Worker", date(1990, 1, 1), "mechanic", 1)

        self.shop.add_client(client)

        with self.assertRaises(WorkerAlreadyExists):
            self.shop.add_worker(worker)

    def test_find_worker(self):
        worker = Admin("Worker", date(1990, 1, 1), "mechanic", 1)
        self.shop.add_worker(worker)

        self.assertEqual(self.shop.find_worker(1), worker)

    def test_find_worker_not_found(self):
        with self.assertRaises(WorkerNotFound):
            self.shop.find_worker(99)


class TestShopManagementVehicles(unittest.TestCase):

    def setUp(self):
        self.shop = ShopManagement()

    def test_add_vehicle_with_unique_license_plate(self):
        car = Car("Seat", "Red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)

        self.shop.add_vehicle(car)

        self.assertIn(car, self.shop.get_vehicles())

    def test_find_vehicle(self):
        car = Car("Seat", "Red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        self.shop.add_vehicle(car)

        self.assertEqual(self.shop.find_vehicle("1234ABC"), car)

    def test_find_vehicle_not_found(self):
        with self.assertRaises(VehicleNotFound):
            self.shop.find_vehicle("9999ZZZ")

    def test_cannot_add_two_cars_with_same_license_plate(self):
        car1 = Car("Seat", "Red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        car2 = Car("Audi", "Blue", "1234ABC", "A3", date(2021, 1, 1), 5000)

        self.shop.add_vehicle(car1)

        with self.assertRaises(VehicleAlreadyRegistered):
            self.shop.add_vehicle(car2)

    def test_cannot_add_different_vehicle_types_with_same_license_plate(self):
        car = Car("Seat", "Red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        motorbike = Motorbike("Yamaha", "Black", "1234ABC", "MT07", date(2021, 1, 1), 3000)

        self.shop.add_vehicle(car)

        with self.assertRaises(VehicleAlreadyRegistered):
            self.shop.add_vehicle(motorbike)

    def test_can_add_different_vehicles_with_different_license_plates(self):
        car = Car("Seat", "Red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        motorbike = Motorbike("Yamaha", "Black", "5678DEF", "MT07", date(2021, 1, 1), 3000)
        truck = Truck("Volvo", "White", "9012GHI", "FH", date(2018, 1, 1), 50000)

        self.shop.add_vehicle(car)
        self.shop.add_vehicle(motorbike)
        self.shop.add_vehicle(truck)

        self.assertIn(car, self.shop.get_vehicles())
        self.assertIn(motorbike, self.shop.get_vehicles())
        self.assertIn(truck, self.shop.get_vehicles())
        self.assertEqual(len(self.shop.get_vehicles()), 3)


class TestShopManagementRentals(unittest.TestCase):

    def setUp(self):
        self.shop = ShopManagement()
        self.vehicle = Car("Seat", "Red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        self.client = Client("Anna", date(2000, 1, 1), 1)
        self.rental = Rental(
            "R1",
            self.vehicle,
            self.client,
            date.today() - timedelta(days=1),
            date.today() + timedelta(days=1),
            500,
            "basic",
        )

    def test_add_rental(self):
        self.shop.add_rental(self.rental)

        self.assertIn(self.rental, self.shop.get_rentals())

    def test_cannot_add_two_rentals_with_same_id(self):
        rental2 = Rental(
            "R1",
            self.vehicle,
            self.client,
            date.today() - timedelta(days=1),
            date.today() + timedelta(days=1),
            300,
            "medium",
        )

        self.shop.add_rental(self.rental)

        with self.assertRaises(RentalAlreadyExists):
            self.shop.add_rental(rental2)

    def test_find_rental(self):
        self.shop.add_rental(self.rental)

        self.assertEqual(self.shop.find_rental("R1"), self.rental)

    def test_find_rental_not_found(self):
        with self.assertRaises(RentalNotFound):
            self.shop.find_rental("R99")

    def test_remove_rental(self):
        self.shop.add_rental(self.rental)

        self.shop.remove_rental("R1")

        self.assertEqual(self.shop.get_rentals(), [])

    def test_remove_rental_not_found(self):
        with self.assertRaises(RentalNotFound):
            self.shop.remove_rental("R99")

    def test_get_active_rentals_only_returns_active_ones(self):
        active = self.rental
        inactive = Rental(
            "R2",
            self.vehicle,
            self.client,
            date.today() - timedelta(days=5),
            date.today() - timedelta(days=1),
            500,
            "basic",
        )

        self.shop.add_rental(active)
        self.shop.add_rental(inactive)

        self.assertEqual(self.shop.get_active_rentals(), [active])


class TestShopManagementCsv(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.rentals_path = os.path.join(self.temp_dir.name, "rentals.csv")
        self.vehicles_path = os.path.join(self.temp_dir.name, "vehicles.csv")
        self.clients_path = os.path.join(self.temp_dir.name, "clients.csv")
        self.workers_path = os.path.join(self.temp_dir.name, "admins.csv")
        self.shop = ShopManagement(
            self.rentals_path,
            self.vehicles_path,
            self.clients_path,
            self.workers_path,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_missing_csv_files_does_not_fail(self):
        self.shop.load_vehicles_csv()
        self.shop.load_clients_csv()
        self.shop.load_workers_csv()
        self.shop.load_rentals_csv(self.shop.find_vehicle, self.shop.find_client)

        self.assertEqual(self.shop.get_vehicles(), [])
        self.assertEqual(self.shop.get_clients(), [])
        self.assertEqual(self.shop.get_workers(), [])
        self.assertEqual(self.shop.get_rentals(), [])

    def test_save_and_load_all_csv(self):
        car = Car("Seat", "Red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        car.register_maintenance(date(2024, 1, 1), 12000)
        client = Client("Anna", date(2000, 1, 1), 1)
        client.add_vehicle(car)
        worker = Admin("Worker", date(1990, 1, 1), "mechanic", 2)
        rental = Rental("R1", car, client, date(2025, 1, 1), date(2025, 1, 10), 500, "medium", 100)

        self.shop.add_vehicle(car)
        self.shop.add_client(client)
        self.shop.add_worker(worker)
        self.shop.add_rental(rental)
        self.shop.save_all_csv()

        loaded_shop = ShopManagement(
            self.rentals_path,
            self.vehicles_path,
            self.clients_path,
            self.workers_path,
        )
        loaded_shop.load_all_csv()

        loaded_car = loaded_shop.find_vehicle("1234ABC")
        loaded_client = loaded_shop.find_client(1)
        loaded_worker = loaded_shop.find_worker(2)
        loaded_rental = loaded_shop.find_rental("R1")

        self.assertEqual(loaded_car.get_brand(), "Seat")
        self.assertEqual(loaded_car.get_last_maintenance_date(), date(2024, 1, 1))
        self.assertEqual(loaded_car.get_last_maintenance_mileage(), 12000)
        self.assertEqual(loaded_client.get_name(), "Anna")
        self.assertEqual(loaded_client.get_vehicles()[0].get_license_plate(), "1234ABC")
        self.assertEqual(loaded_worker.get_role(), "mechanic")
        self.assertEqual(loaded_rental.get_vehicle().get_license_plate(), "1234ABC")
        self.assertEqual(loaded_rental.get_user().get_id(), 1)
        self.assertEqual(loaded_rental.get_kms_done(), 100)
        self.assertEqual(loaded_rental.get_assurance(), "medium")

    def test_load_csv_files_with_blank_lines(self):
        with open(self.vehicles_path, "w") as f:
            f.write("type,brand,color,license_plate,model,matriculation_date,mileage,last_maintenance_date,last_maintenance_mileage\n")
            f.write("\n")
            f.write("Car,Seat,Red,1234ABC,Ibiza,2020-01-01,10000,,\n")

        with open(self.clients_path, "w") as f:
            f.write("id,name,date_of_birth,vehicles\n")
            f.write("\n")
            f.write("1,Anna,2000-01-01,1234ABC\n")

        with open(self.workers_path, "w") as f:
            f.write("id,name,date_of_birth,role\n")
            f.write("\n")
            f.write("2,Worker,1990-01-01,mechanic\n")

        with open(self.rentals_path, "w") as f:
            f.write("rental_id,license_plate,user_id,start,end,kms_allowed,kms_done,assurance\n")
            f.write("\n")
            f.write("R1,1234ABC,1,2025-01-01,2025-01-10,500,100,basic\n")

        self.shop.load_all_csv()

        self.assertEqual(len(self.shop.get_vehicles()), 1)
        self.assertEqual(len(self.shop.get_clients()), 1)
        self.assertEqual(len(self.shop.get_workers()), 1)
        self.assertEqual(len(self.shop.get_rentals()), 1)
        self.assertEqual(self.shop.find_rental("R1").get_kms_done(), 100)

    def test_save_individual_csv_files(self):
        car = Car("Seat", "Red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        client = Client("Anna", date(2000, 1, 1), 1)
        worker = Admin("Worker", date(1990, 1, 1), "mechanic", 2)
        rental = Rental("R1", car, client, date(2025, 1, 1), date(2025, 1, 10), 500, "basic")

        self.shop.add_vehicle(car)
        self.shop.add_client(client)
        self.shop.add_worker(worker)
        self.shop.add_rental(rental)

        self.shop.save_vehicles_csv()
        self.shop.save_clients_csv()
        self.shop.save_workers_csv()
        self.shop.save_rentals_csv()

        with open(self.vehicles_path, "r") as f:
            vehicles_text = f.read()
        with open(self.clients_path, "r") as f:
            clients_text = f.read()
        with open(self.workers_path, "r") as f:
            workers_text = f.read()
        with open(self.rentals_path, "r") as f:
            rentals_text = f.read()

        self.assertIn("Car,Seat,Red,1234ABC,Ibiza,2020-01-01,10000,,", vehicles_text)
        self.assertIn("1,Anna,2000-01-01,", clients_text)
        self.assertIn("2,Worker,1990-01-01,mechanic", workers_text)
        self.assertIn("R1,1234ABC,1,2025-01-01,2025-01-10,500,0,basic", rentals_text)


if __name__ == "__main__":
    unittest.main()