from unittest import TestCase
from datetime import date
from USERS.users import User
from custom_exceptions import InvalidName, InvalidDateOfBirth

class ConcreteUser(User):
    def get_type(self):
        return "concrete"

class TestUser(TestCase):
    def test_create_user(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        self.assertEqual(user.get_name(), "Ana Garcia")
        self.assertEqual(user.get_date_of_birth(), date(2007, 6, 20))
        self.assertIsNotNone(user.get_id())
        self.assertIsInstance(user.get_id(), int)

    def test_ids_unique(self):
        user1 = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        user2 = ConcreteUser("Sofia Perez", date(1985, 3, 20))
        self.assertNotEqual(user1.get_id(), user2.get_id())
    
    def test_id_increment(self):
        user1 = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        user2 = ConcreteUser("Sofia Perez", date(1985, 3, 20))
        self.assertEqual(user1.get_id() + 1, user2.get_id())

    def test_invalid_name_string(self):
        with self.assertRaises(InvalidName):
            ConcreteUser(123, date(2007, 6, 20))

    def test_invalid_name_empty(self):
        with self.assertRaises(InvalidName):
            ConcreteUser("   ", date(2007, 6, 20))

    def test_invalid_date_object(self):
        with self.assertRaises(InvalidDateOfBirth):
            ConcreteUser("Ana Garcia", "2007-06-20")

    def test_invalid_date_future(self):
        with self.assertRaises(InvalidDateOfBirth):
            ConcreteUser("Ana Garcia", date(2100, 1, 1))

    def test_invalid_user_id_negative(self):
        with self.assertRaises(ValueError):
            ConcreteUser("Ana Garcia", date(2007, 6, 20), -1)

    def test_invalid_user_id_string(self):
        with self.assertRaises(ValueError):
            ConcreteUser("Ana Garcia", date(2007, 6, 20), "1")

    def test_invalid_user_id_boolean(self):
        with self.assertRaises(ValueError):
            ConcreteUser("Ana Garcia", date(2007, 6, 20), True)

    def test_get_age(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        today = date.today()
        expected_age = today.year - 2007
        if today.month < 6:
            expected_age -= 1
        elif today.month == 6:
            if today.day < 20:
                expected_age -= 1
        self.assertEqual(user.get_age(), expected_age)
    
    def test_get_age_when_birthday_is_later_this_month(self):
        today = date.today()
        day = today.day + 1
        month = today.month
        year = today.year - 20

        if day > 28:
            day = 28
            if today.day >= 28:
                month = today.month + 1
                if month > 12:
                    month = 1
                    year = year + 1

        user = ConcreteUser("Ana Garcia", date(year, month, day))
        self.assertEqual(user.get_age(), 19)

    def test_update_name(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        user.update_name("Ana Gomez")
        self.assertEqual(user.get_name(), "Ana Gomez")

    def test_update_date_of_birth(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        user.update_date_of_birth(date(2010, 7, 3))
        self.assertEqual(user.get_date_of_birth(), date(2010, 7, 3))
    
    def test_get_type(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        self.assertEqual(user.get_type(), "concrete")

    def test_to_csv_line(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20), 50)
        self.assertEqual(user.to_csv_line(), "50,Ana Garcia,2007-06-20")

    def test_abstract_get_type_body_returns_none_when_called_directly(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        self.assertIsNone(User.get_type(user))