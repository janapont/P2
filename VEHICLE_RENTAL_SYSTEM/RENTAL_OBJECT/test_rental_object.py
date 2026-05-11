"""Unit tests for the Rental class."""
import unittest
from datetime import date, timedelta

from RENTAL_OBJECT.rental_object import Rental
from VEHICLES.CAR.car import Car
from USERS.CLIENTS.clients import Client
from custom_exceptions import (
    InvalidRentalPeriod,
    InvalidKms,
    InvalidAssurance,
    RentalNotActive,
    KmsExceeded,
)


class TestRentalCreation(unittest.TestCase):

    def setUp(self):
        self.vehicle = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        self.user = Client("Anna", date(2000, 1, 1), 1)
        self.start_date = date.today() - timedelta(days=1)
        self.end_date = date.today() + timedelta(days=1)

    def test_create_valid_rental(self):
        rental = Rental("R1", self.vehicle, self.user, self.start_date, self.end_date, 500, "basic")

        self.assertEqual(rental.get_rental_id(), "R1")
        self.assertEqual(rental.get_vehicle(), self.vehicle)
        self.assertEqual(rental.get_user(), self.user)
        self.assertEqual(rental.get_start_date(), self.start_date)
        self.assertEqual(rental.get_end_date(), self.end_date)
        self.assertEqual(rental.get_kms_allowed(), 500)
        self.assertEqual(rental.get_kms_done(), 0)
        self.assertEqual(rental.get_assurance(), "basic")

    def test_create_valid_rental_with_kms_done(self):
        rental = Rental("R1", self.vehicle, self.user, self.start_date, self.end_date, 500, "medium", 100)

        self.assertEqual(rental.get_kms_done(), 100)
        self.assertEqual(rental.get_assurance(), "medium")

    def test_invalid_period_when_dates_are_not_date_objects(self):
        with self.assertRaises(InvalidRentalPeriod):
            Rental("R1", self.vehicle, self.user, "2025-01-01", self.end_date, 500, "basic")

    def test_invalid_period_when_end_date_is_before_start_date(self):
        with self.assertRaises(InvalidRentalPeriod):
            Rental("R1", self.vehicle, self.user, self.end_date, self.start_date, 500, "basic")

    def test_invalid_period_when_end_date_is_equal_to_start_date(self):
        with self.assertRaises(InvalidRentalPeriod):
            Rental("R1", self.vehicle, self.user, self.start_date, self.start_date, 500, "basic")

    def test_invalid_kms_allowed_zero(self):
        with self.assertRaises(InvalidKms):
            Rental("R1", self.vehicle, self.user, self.start_date, self.end_date, 0, "basic")

    def test_invalid_kms_allowed_negative(self):
        with self.assertRaises(InvalidKms):
            Rental("R1", self.vehicle, self.user, self.start_date, self.end_date, -1, "basic")

    def test_invalid_kms_allowed_non_int(self):
        with self.assertRaises(InvalidKms):
            Rental("R1", self.vehicle, self.user, self.start_date, self.end_date, "500", "basic")

    def test_invalid_kms_done_negative(self):
        with self.assertRaises(InvalidKms):
            Rental("R1", self.vehicle, self.user, self.start_date, self.end_date, 500, "basic", -1)

    def test_invalid_kms_done_non_int(self):
        with self.assertRaises(InvalidKms):
            Rental("R1", self.vehicle, self.user, self.start_date, self.end_date, 500, "basic", "100")

    def test_kms_done_cannot_exceed_kms_allowed(self):
        with self.assertRaises(KmsExceeded):
            Rental("R1", self.vehicle, self.user, self.start_date, self.end_date, 500, "basic", 501)

    def test_invalid_assurance(self):
        with self.assertRaises(InvalidAssurance):
            Rental("R1", self.vehicle, self.user, self.start_date, self.end_date, 500, "full")


class TestRentalActivity(unittest.TestCase):

    def setUp(self):
        self.vehicle = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        self.user = Client("Anna", date(2000, 1, 1), 1)

    def test_is_active_when_today_is_inside_period(self):
        rental = Rental(
            "R1",
            self.vehicle,
            self.user,
            date.today() - timedelta(days=1),
            date.today() + timedelta(days=1),
            500,
            "basic",
        )

        self.assertTrue(rental.is_active())

    def test_is_not_active_when_period_is_in_the_past(self):
        rental = Rental(
            "R1",
            self.vehicle,
            self.user,
            date.today() - timedelta(days=5),
            date.today() - timedelta(days=1),
            500,
            "basic",
        )

        self.assertFalse(rental.is_active())

    def test_is_not_active_when_period_is_in_the_future(self):
        rental = Rental(
            "R1",
            self.vehicle,
            self.user,
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=5),
            500,
            "basic",
        )

        self.assertFalse(rental.is_active())


class TestRentalKms(unittest.TestCase):

    def setUp(self):
        self.vehicle = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        self.user = Client("Anna", date(2000, 1, 1), 1)
        self.rental = Rental(
            "R1",
            self.vehicle,
            self.user,
            date.today() - timedelta(days=1),
            date.today() + timedelta(days=1),
            500,
            "basic",
        )

    def test_add_kms_to_active_rental(self):
        self.rental.add_kms(100)

        self.assertEqual(self.rental.get_kms_done(), 100)

    def test_add_kms_twice(self):
        self.rental.add_kms(100)
        self.rental.add_kms(50)

        self.assertEqual(self.rental.get_kms_done(), 150)

    def test_add_invalid_kms_zero(self):
        with self.assertRaises(InvalidKms):
            self.rental.add_kms(0)

    def test_add_invalid_kms_negative(self):
        with self.assertRaises(InvalidKms):
            self.rental.add_kms(-1)

    def test_add_invalid_kms_non_int(self):
        with self.assertRaises(InvalidKms):
            self.rental.add_kms("100")

    def test_add_kms_to_inactive_rental_raises(self):
        rental = Rental(
            "R1",
            self.vehicle,
            self.user,
            date.today() - timedelta(days=5),
            date.today() - timedelta(days=1),
            500,
            "basic",
        )

        with self.assertRaises(RentalNotActive):
            rental.add_kms(100)

    def test_add_kms_cannot_exceed_allowed_limit(self):
        self.rental.add_kms(400)

        with self.assertRaises(KmsExceeded):
            self.rental.add_kms(101)


class TestRentalAssurance(unittest.TestCase):

    def setUp(self):
        vehicle = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        user = Client("Anna", date(2000, 1, 1), 1)
        self.rental = Rental(
            "R1",
            vehicle,
            user,
            date.today() - timedelta(days=1),
            date.today() + timedelta(days=1),
            500,
            "basic",
        )

    def test_update_assurance(self):
        self.rental.update_assurance("premium")

        self.assertEqual(self.rental.get_assurance(), "premium")

    def test_update_assurance_invalid(self):
        with self.assertRaises(InvalidAssurance):
            self.rental.update_assurance("full")


class TestRentalCsv(unittest.TestCase):

    def test_to_csv_line(self):
        vehicle = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        user = Client("Anna", date(2000, 1, 1), 1)
        rental = Rental("R1", vehicle, user, date(2025, 1, 1), date(2025, 1, 10), 500, "medium", 100)

        self.assertEqual(rental.to_csv_line(), "R1,1234ABC,1,2025-01-01,2025-01-10,500,100,medium")


class TestRentalEncapsulation(unittest.TestCase):

    def test_private_attributes_not_accessible(self):
        vehicle = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 10000)
        user = Client("Anna", date(2000, 1, 1), 1)
        rental = Rental("R1", vehicle, user, date(2025, 1, 1), date(2025, 1, 10), 500, "basic")

        self.assertFalse(hasattr(rental, "rental_id"))
        self.assertFalse(hasattr(rental, "vehicle"))
        self.assertFalse(hasattr(rental, "user"))
        self.assertFalse(hasattr(rental, "kms_allowed"))
        self.assertFalse(hasattr(rental, "kms_done"))


if __name__ == "__main__":
    unittest.main()