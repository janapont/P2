from unittest import TestCase
from datetime import date
from admins import Admin
from custom_exceptions import InvalidRole

class TestAdmin(TestCase):
    def test_create_admin(self):
        admin = Admin("Laia Garcia", date(2007, 6, 20), "mechanic")
        self.assertEqual(admin.get_name(), "Laia Garcia")
        self.assertEqual(admin.get_date_of_birth(), date(2007, 6, 20))
        self.assertEqual(admin.get_role(), "mechanic")
        self.assertEqual(admin.get_type(), "admin")
        self.assertIsNotNone(admin.get_id())

    def test_invalid_role(self):
        with self.assertRaises(InvalidRole):
            Admin("Laia Garcia", date(2007, 6, 20), "driver")

    def test_role_empty(self):
        with self.assertRaises(InvalidRole):
            Admin("Laia Garcia", date(2007, 6, 20), "")

    def test_update_role(self):
        admin = Admin("Laia Garcia", date(2007, 6, 20), "mechanic")
        admin.update_role("administrator")
        self.assertEqual(admin.get_role(), "administrator")

