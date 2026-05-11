from datetime import date
from custom_exceptions import (
    InvalidRentalPeriod,
    InvalidKms,
    InvalidAssurance,
    RentalNotActive,
    KmsExceeded,
)

class Rental:
    def __init__(self, rental_id, vehicle, user, start_date, end_date, kms_allowed, assurance, kms_done=0):
        if not isinstance(start_date, date) or not isinstance(end_date, date) or end_date <= start_date:
            raise InvalidRentalPeriod()
        if not isinstance(kms_allowed, int) or kms_allowed <= 0:
            raise InvalidKms()
        if not isinstance(kms_done, int) or kms_done < 0:
            raise InvalidKms()
        if kms_done > kms_allowed:
            raise KmsExceeded()
        if assurance not in ("basic", "medium", "premium"):
            raise InvalidAssurance()

        self.__rental_id = rental_id
        self.__vehicle = vehicle
        self.__user = user
        self.__start_date = start_date
        self.__end_date = end_date
        self.__kms_allowed = kms_allowed
        self.__kms_done = kms_done
        self.__assurance = assurance

    def get_rental_id(self):
        return self.__rental_id

    def get_vehicle(self):
        return self.__vehicle

    def get_user(self):
        return self.__user

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date

    def get_kms_allowed(self):
        return self.__kms_allowed

    def get_kms_done(self):
        return self.__kms_done

    def get_assurance(self):
        return self.__assurance

    def is_active(self):
        today = date.today()
        if self.__start_date <= today <= self.__end_date:
            return True
        return False

    def add_kms(self, kms):
        if not isinstance(kms, int) or kms <= 0:
            raise InvalidKms()
        if not self.is_active():
            raise RentalNotActive()
        if self.__kms_done + kms > self.__kms_allowed:
            raise KmsExceeded()
        self.__kms_done = self.__kms_done + kms

    def update_assurance(self, new_assurance):
        if new_assurance not in ("basic", "medium", "premium"):
            raise InvalidAssurance()
        self.__assurance = new_assurance

    def to_csv_line(self):
        plate = self.__vehicle.get_license_plate()
        user_id = str(self.__user.get_id())
        start = str(self.__start_date)
        end = str(self.__end_date)
        line = self.__rental_id + "," + plate + "," + user_id + "," + start + "," + end + "," + str(self.__kms_allowed) + "," + str(self.__kms_done) + "," + self.__assurance
        return line
