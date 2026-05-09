from unittest import TestCase
from datetime import date
from clients import Client
from vehicles.car import Car
from custom_exceptions import VehicleAlreadyRegistered, VehicleNotFound

# ESPERAR A TENIR LA FILE DE VEHICLES.PY

class TestClient(TestCase):
    def test_create_client(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        self.assertEqual(client.get_name(), "Luis Garcia")
        self.assertEqual(client.get_date_of_birth(), date(2007, 6, 20))
        self.assertEqual(client.get_type(), "client")
        self.assertIsNotNone(client.get_id())

    def test_initial_vehicles_empty(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        self.assertEqual(client.get_vehicles(), [])

    def test_add_vehicle(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        car = Car("Toyota", "Red", "1234ABC", "Corolla", date(2020, 1, 1), 0)
        client.add_vehicle(car)
        self.assertEqual(len(client.get_vehicles()), 1)

    def test_add_duplicate_vehicle(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        car = Car("Toyota", "Red", "1234ABC", "Corolla", date(2020, 1, 1), 0)
        client.add_vehicle(car)
        with self.assertRaises(VehicleAlreadyRegistered):
            client.add_vehicle(car)

    def test_remove_vehicle(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        car = Car("Toyota", "Red", "1234ABC", "Corolla", date(2020, 1, 1), 0)
        client.add_vehicle(car)
        client.remove_vehicle(car)
        self.assertEqual(len(client.get_vehicles()), 0)

    def test_remove_vehicle_not_found(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        car = Car("Toyota", "Red", "1234ABC", "Corolla", date(2020, 1, 1,), 0)
        with self.assertRaises(VehicleNotFound):
            client.remove_vehicle(car)

    def test_update_vehicle_kms(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        car = Car("Toyota", "Red", "1234ABC", "Corolla", date(2020, 1, 1), 0)
        client.add_vehicle(car)
        client.update_vehicle_kms("1234ABC", 5000)
        self.assertEqual(car.get_mileage(), 5000)

    def test_update_vehicle_kms_not_found(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        with self.assertRaises(VehicleNotFound):
            client.update_vehicle_kms("9999ABC", 5000)

    def test_get_next_itv(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        car = Car("Toyota", "Red", "1234ABC", "Corolla", date(2020, 1, 1,), 0)
        client.add_vehicle(car)
        result = client.get_next_itv("1234ABC")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, date)

    def test_get_next_itv_not_found(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        with self.assertRaises(VehicleNotFound):
            client.get_next_itv("9999ABC")

    def test_get_next_maintenance(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        car = Car("Toyota", "Red", "1234ABC", "Corolla", date(2020, 1, 1,), 0)
        client.add_vehicle(car)
        result = client.get_next_maintenance("1234ABC")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, date)

    def test_get_next_maintenance_not_found(self):
        client = Client("Luis Garcia", date(2007, 6, 20))
        with self.assertRaises(VehicleNotFound):
            client.get_next_maintenance("9999ABC") 