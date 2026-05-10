import unittest
from datetime import date

from custom_exceptions import VehicleAlreadyRegistered
from SHOP_MANAGEMENT.shop_management import ShopManagement

from VEHICLES.CAR.car import Car
from VEHICLES.MOTORBIKE.motorbike import Motorbike
from VEHICLES.TRUCK.truck import Truck


class TestShopManagementDuplicateLicensePlates(unittest.TestCase):

    def setUp(self):
        self.shop = ShopManagement()

    def test_add_vehicle_with_unique_license_plate(self):
        car = Car("Seat","Red","1234ABC","Ibiza",date(2020, 1, 1),10000)

        self.shop.add_vehicle(car)

        self.assertIn(car, self.shop.get_vehicles())

    def test_cannot_add_two_cars_with_same_license_plate(self):
        car1 = Car("Seat","Red","1234ABC","Ibiza",date(2020, 1, 1),10000)

        car2 = Car("Audi","Blue","1234ABC","A3",date(2021, 1, 1),5000)

        self.shop.add_vehicle(car1)

        with self.assertRaises(VehicleAlreadyRegistered):
            self.shop.add_vehicle(car2)

    def test_cannot_add_different_vehicle_types_with_same_license_plate(self):
        car = Car("Seat","Red","1234ABC","Ibiza",date(2020, 1, 1),10000)

        motorbike = Motorbike("Yamaha","Black","1234ABC","MT07",date(2021, 1, 1),3000)

        self.shop.add_vehicle(car)

        with self.assertRaises(VehicleAlreadyRegistered):
            self.shop.add_vehicle(motorbike)

    def test_can_add_different_vehicles_with_different_license_plates(self):
        car = Car("Seat","Red","1234ABC","Ibiza",date(2020, 1, 1),10000)

        motorbike = Motorbike("Yamaha","Black","5678DEF","MT07",date(2021, 1, 1),3000)

        truck = Truck("Volvo","White","9012GHI","FH",date(2018, 1, 1),50000)

        self.shop.add_vehicle(car)
        self.shop.add_vehicle(motorbike)
        self.shop.add_vehicle(truck)

        self.assertIn(car, self.shop.get_vehicles())
        self.assertIn(motorbike, self.shop.get_vehicles())
        self.assertIn(truck, self.shop.get_vehicles())
        self.assertEqual(len(self.shop.get_vehicles()), 3)


if __name__ == "__main__":
    unittest.main()
