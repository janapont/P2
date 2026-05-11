import unittest
from datetime import date, timedelta

from VEHICLES.vehicle import Vehicle, vehicle_from_csv_line
from custom_exceptions import (
    InvalidLicensePlateError,
    InvalidMatriculationDateError,
    InvalidMileageError,
    MileageCannotDecreaseError,
    InvalidBrandError,
    InvalidColorError,
    InvalidModelError,
    )

class _DummyVehicle(Vehicle):
    def calculate_ITV(self):
        return date.today()

    def maintenance_schedule(self):
        return date.today()


class TestVehicleCreation(unittest.TestCase):

    def test_create_valid_vehicle(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        self.assertEqual(v.get_brand(), "Seat")
        self.assertEqual(v.get_color(), "red")
        self.assertEqual(v.get_license_plate(), "1234ABC")
        self.assertEqual(v.get_model(), "Ibiza")
        self.assertEqual(v.get_matriculation_date(), date(2020, 1, 1))
        self.assertEqual(v.get_mileage(), 10000)
        self.assertIsNone(v.get_last_maintenance_date())
        self.assertIsNone(v.get_last_maintenance_mileage())

    def test_invalid_license_plate_too_short(self):
        with self.assertRaises(InvalidLicensePlateError):
            _DummyVehicle("Seat", "red", "123ABC", "Ibiza", date(2020, 1, 1), 0)

    def test_invalid_license_plate_too_long(self):
        with self.assertRaises(InvalidLicensePlateError):
            _DummyVehicle("Seat", "red", "12345ABC", "Ibiza", date(2020, 1, 1), 0)

    def test_invalid_license_plate_lowercase(self):
        with self.assertRaises(InvalidLicensePlateError):
            _DummyVehicle("Seat", "red", "1234abc", "Ibiza", date(2020, 1, 1), 0)

    def test_invalid_license_plate_letters_in_numbers(self):
        with self.assertRaises(InvalidLicensePlateError):
            _DummyVehicle("Seat", "red", "12A4ABC", "Ibiza", date(2020, 1, 1), 0)

    def test_invalid_license_plate_numbers_in_letters(self):
        with self.assertRaises(InvalidLicensePlateError):
            _DummyVehicle("Seat", "red", "1234A1C", "Ibiza", date(2020, 1, 1), 0)

    def test_invalid_license_plate_not_string(self):
        with self.assertRaises(InvalidLicensePlateError):
            _DummyVehicle("Seat", "red", 1234, "Ibiza", date(2020, 1, 1), 0)

    def test_invalid_future_matriculation_date(self):
        future = date.today() + timedelta(days=1)
        with self.assertRaises(InvalidMatriculationDateError):
            _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", future, 0)

    def test_invalid_matriculation_date_not_date(self):
        with self.assertRaises(InvalidMatriculationDateError):
            _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", "2020-01-01", 0)

    def test_today_matriculation_date_is_valid(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date.today(), 0)
        self.assertEqual(v.get_matriculation_date(), date.today())

    def test_invalid_negative_mileage(self):
        with self.assertRaises(InvalidMileageError):
            _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), -1)

    def test_invalid_non_int_mileage(self):
        with self.assertRaises(InvalidMileageError):
            _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), "100")

    def test_invalid_float_mileage(self):
        with self.assertRaises(InvalidMileageError):
            _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 100.5)

    def test_invalid_boolean_mileage(self):
        with self.assertRaises(InvalidMileageError):
            _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), True)

    def test_zero_mileage_is_valid(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 0)
        self.assertEqual(v.get_mileage(), 0)

    def test_invalid_brand_empty(self):
        with self.assertRaises(InvalidBrandError):
            _DummyVehicle("", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 0)

    def test_invalid_color_empty(self):
        with self.assertRaises(InvalidColorError):
            _DummyVehicle("Seat", "", "1234ABC", "Ibiza", date(2020, 1, 1), 0)

    def test_invalid_model_empty(self):
        with self.assertRaises(InvalidModelError):
            _DummyVehicle("Seat", "red", "1234ABC", "", date(2020, 1, 1), 0)
            
class TestVehicleUpdateInfo(unittest.TestCase):

    def setUp(self):
        self.v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)

    def test_update_brand(self):
        self.v.update_info(brand="Audi")
        self.assertEqual(self.v.get_brand(), "Audi")

    def test_update_color(self):
        self.v.update_info(color="blue")
        self.assertEqual(self.v.get_color(), "blue")

    def test_update_model(self):
        self.v.update_info(model="Leon")
        self.assertEqual(self.v.get_model(), "Leon")

    def test_update_mileage_increase(self):
        self.v.update_info(mileage=15000)
        self.assertEqual(self.v.get_mileage(), 15000)

    def test_update_mileage_same_value(self):
        self.v.update_info(mileage=10000)
        self.assertEqual(self.v.get_mileage(), 10000)

    def test_update_mileage_decrease_raises(self):
        with self.assertRaises(MileageCannotDecreaseError):
            self.v.update_info(mileage=5000)

    def test_update_mileage_negative_raises(self):
        with self.assertRaises(InvalidMileageError):
            self.v.update_info(mileage=-1)

    def test_update_mileage_non_int_raises(self):
        with self.assertRaises(InvalidMileageError):
            self.v.update_info(mileage="20000")

    def test_update_nothing_keeps_values(self):
        self.v.update_info()
        self.assertEqual(self.v.get_brand(), "Seat")
        self.assertEqual(self.v.get_color(), "red")
        self.assertEqual(self.v.get_model(), "Ibiza")
        self.assertEqual(self.v.get_mileage(), 10000)

    def test_update_multiple_fields(self):
        self.v.update_info(brand="Audi", color="black", model="A3", mileage=12000)
        self.assertEqual(self.v.get_brand(), "Audi")
        self.assertEqual(self.v.get_color(), "black")
        self.assertEqual(self.v.get_model(), "A3")
        self.assertEqual(self.v.get_mileage(), 12000)


class TestVehicleAge(unittest.TestCase):

    def test_age_zero_when_matriculated_today(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date.today(), 0)
        self.assertEqual(v.get_age_years(), 0)

    def test_age_birthday_not_yet_reached(self):
        today = date.today()
        future_in_year = today + timedelta(days=1)
        try:
            matric = future_in_year.replace(year=today.year - 5)
        except ValueError:
            matric = date(today.year - 5, future_in_year.month, 28)
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", matric, 0)
        self.assertEqual(v.get_age_years(), 4)

    def test_age_birthday_already_passed(self):
        today = date.today()
        past_in_year = today - timedelta(days=1)
        try:
            matric = past_in_year.replace(year=today.year - 5)
        except ValueError:
            matric = date(today.year - 5, past_in_year.month, 28)
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", matric, 0)
        self.assertEqual(v.get_age_years(), 5)


class TestVehicleMaintenanceRegistration(unittest.TestCase):

    def test_register_maintenance_updates_fields(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 30000)
        v.register_maintenance(date(2024, 6, 1), 25000)
        self.assertEqual(v.get_last_maintenance_date(), date(2024, 6, 1))
        self.assertEqual(v.get_last_maintenance_mileage(), 25000)

    def test_register_maintenance_overwrites(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 40000)
        v.register_maintenance(date(2024, 6, 1), 25000)
        v.register_maintenance(date(2025, 6, 1), 35000)
        self.assertEqual(v.get_last_maintenance_date(), date(2025, 6, 1))
        self.assertEqual(v.get_last_maintenance_mileage(), 35000)

    def test_register_maintenance_date_before_matriculation_raises(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)

        with self.assertRaises(InvalidMatriculationDateError):
            v.register_maintenance(date(2019, 1, 1), 1000)

    def test_register_maintenance_future_date_raises(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)

        with self.assertRaises(InvalidMatriculationDateError):
            v.register_maintenance(date.today() + timedelta(days=1), 1000)

    def test_register_maintenance_invalid_km_raises(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)

        with self.assertRaises(InvalidMileageError):
            v.register_maintenance(date(2024, 1, 1), 20000)


class TestVehicleHelpers(unittest.TestCase):

    def setUp(self):
        self.v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 0)

    def test_add_years_normal(self):
        self.assertEqual(self.v._add_years(date(2020, 5, 15), 3), date(2023, 5, 15))

    def test_add_years_leap_day(self):
        self.assertEqual(self.v._add_years(date(2020, 2, 29), 1), date(2021, 2, 28))

    def test_add_months_normal(self):
        self.assertEqual(self.v._add_months(date(2020, 1, 15), 3), date(2020, 4, 15))

    def test_add_months_year_change(self):
        self.assertEqual(self.v._add_months(date(2020, 11, 15), 3), date(2021, 2, 15))

    def test_add_months_day_does_not_exist(self):
        self.assertEqual(self.v._add_months(date(2021, 1, 31), 1), date(2021, 2, 28))


class TestVehicleEncapsulation(unittest.TestCase):

    def test_private_attributes_not_accessible(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 0)
        self.assertFalse(hasattr(v, "brand"))
        self.assertFalse(hasattr(v, "license_plate"))
        self.assertFalse(hasattr(v, "mileage"))


class TestVehicleAbstract(unittest.TestCase):

    def test_cannot_instantiate_abstract_vehicle(self):
        with self.assertRaises(TypeError):
            Vehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 0)

    def test_abstract_method_bodies_return_none_when_called_directly(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 0)

        self.assertIsNone(Vehicle.calculate_ITV(v))
        self.assertIsNone(Vehicle.maintenance_schedule(v))


class TestVehicleCsvFunctions(unittest.TestCase):

    def test_to_csv_line_without_maintenance(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)

        self.assertEqual(v.to_csv_line(), "_DummyVehicle,Seat,red,1234ABC,Ibiza,2020-01-01,10000,,")

    def test_to_csv_line_with_maintenance(self):
        v = _DummyVehicle("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        v.register_maintenance(date(2024, 1, 1), 9000)

        self.assertEqual(v.to_csv_line(), "_DummyVehicle,Seat,red,1234ABC,Ibiza,2020-01-01,10000,2024-01-01,9000")

    def test_vehicle_from_csv_line_car(self):
        vehicle = vehicle_from_csv_line("Car,Seat,red,1234ABC,Ibiza,2020-01-01,10000,,")

        self.assertEqual(vehicle.get_license_plate(), "1234ABC")
        self.assertEqual(vehicle.__class__.__name__, "Car")

    def test_vehicle_from_csv_line_motorbike(self):
        vehicle = vehicle_from_csv_line("Motorbike,Honda,black,5678DEF,Forza,2020-01-01,5000,,")

        self.assertEqual(vehicle.get_license_plate(), "5678DEF")
        self.assertEqual(vehicle.__class__.__name__, "Motorbike")

    def test_vehicle_from_csv_line_truck(self):
        vehicle = vehicle_from_csv_line("Truck,Volvo,white,9012GHI,FH,2020-01-01,50000,,")

        self.assertEqual(vehicle.get_license_plate(), "9012GHI")
        self.assertEqual(vehicle.__class__.__name__, "Truck")

    def test_vehicle_from_csv_line_invalid_type(self):
        with self.assertRaises(ValueError):
            vehicle_from_csv_line("Bike,Honda,black,5678DEF,Forza,2020-01-01,5000,,")