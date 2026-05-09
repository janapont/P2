from users import User
from custom_exceptions import InvalidRole

ROLES = ["mechanic", "rental manager", "administrator"]

class Admin(User):
    def __init__(self, name, date_of_birth, role):
        super().__init__(name, date_of_birth)
        self.validate_role(role)
        self.__role = role

    def validate_role(self, role):
        if role not in ROLES:
            raise InvalidRole(f"Role must be one of: {ROLES}")

    def get_type(self):
        return "admin"

    def get_role(self):
        return self.__role

    def update_role(self, role):
        self.validate_role(role)
        self.__role = role