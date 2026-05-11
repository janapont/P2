""" considerar des d'aqui:
brand: string no vacío
color: string no vacío
model: string no vacío
brand = brand.strip()
color = color.strip()
model = model.strip()
license_plate = license_plate.strip().upper()

mileage = int(mileage_input)

maintenance date sea una fecha válida
maintenance km sea un int positivo
maintenance km no sea mayor que el mileage actual, salvo que antes actualicéis el mileage
maintenance km no sea negativo

En el main, los vehículos siempre se añaden primero desde ShopManagement.
Después, si son vehículos de un cliente, se registran también en ese cliente.

orden carga:
1. Cargar vehicles.csv
2. Cargar clients.csv
3. Cargar admins.csv
4. Cargar rentals.csv

guardar todo el sistema:shop.save_all_csv()
"""


import os
from datetime import date

from SHOP_MANAGEMENT.shop_management import ShopManagement
from VEHICLES.CAR.car import Car
from VEHICLES.MOTORBIKE.motorbike import Motorbike
from VEHICLES.TRUCK.truck import Truck
from USERS.CLIENTS.clients import Client
from USERS.ADMINS.admins import Admin
from RENTAL_OBJECT.rental_object import Rental


ROLES = ["mechanic", "rental manager", "administrator"]
ASSURANCES = ["basic", "medium", "premium"]
VEHICLE_TYPES = {
    "1": Car,
    "2": Motorbike,
    "3": Truck,
}


def prepare_environment():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    os.makedirs("DATABASE", exist_ok=True)


def ask_text(message, optional=False):
    while True:
        value = input(message).strip()
        if optional and value == "":
            return None
        if value == "":
            print("This field cannot be empty.")
        elif "," in value:
            print("Commas are not allowed because data is saved in CSV files.")
        else:
            return value


def ask_license_plate(message="License plate: ", optional=False):
    value = ask_text(message, optional)
    if value is None:
        return None
    return value.upper()


def ask_int(message, min_value=None, max_value=None, optional=False):
    while True:
        value = input(message).strip()
        if optional and value == "":
            return None
        try:
            number = int(value)
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if min_value is not None and number < min_value:
            print(f"The number must be at least {min_value}.")
        elif max_value is not None and number > max_value:
            print(f"The number cannot be higher than {max_value}.")
        else:
            return number


def ask_date(message, optional=False):
    while True:
        value = input(message).strip()
        if optional and value == "":
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            print("Please enter the date in YYYY-MM-DD format.")


def ask_option(message, valid_options):
    while True:
        value = input(message).strip()
        if value in valid_options:
            return value
        print("Invalid option.")


def ask_role(optional=False):
    print("Roles:")
    for i, role in enumerate(ROLES, start=1):
        print(f"{i}. {role}")

    valid_options = [str(i) for i in range(1, len(ROLES) + 1)]
    if optional:
        valid_options.append("")

    option = ask_option("Choose role: ", valid_options)
    if option == "":
        return None
    return ROLES[int(option) - 1]


def ask_assurance(optional=False):
    print("Assurance types:")
    for i, assurance in enumerate(ASSURANCES, start=1):
        print(f"{i}. {assurance}")

    valid_options = [str(i) for i in range(1, len(ASSURANCES) + 1)]
    if optional:
        valid_options.append("")

    option = ask_option("Choose assurance: ", valid_options)
    if option == "":
        return None
    return ASSURANCES[int(option) - 1]


def format_date(value):
    if value is None:
        return "-"
    return value.isoformat()


def print_vehicle(vehicle):
    print(
        f"{vehicle.__class__.__name__} | "
        f"{vehicle.get_license_plate()} | "
        f"{vehicle.get_brand()} {vehicle.get_model()} | "
        f"{vehicle.get_color()} | "
        f"matriculation: {vehicle.get_matriculation_date()} | "
        f"kms: {vehicle.get_mileage()} | "
        f"last maintenance: {format_date(vehicle.get_last_maintenance_date())}, "
        f"{vehicle.get_last_maintenance_mileage() if vehicle.get_last_maintenance_mileage() is not None else '-'} kms"
    )


def print_client(client):
    plates = []
    for vehicle in client.get_vehicles():
        plates.append(vehicle.get_license_plate())
    vehicles_text = "|".join(plates) if plates else "-"
    print(
        f"Client | id: {client.get_id()} | "
        f"name: {client.get_name()} | "
        f"birth: {client.get_date_of_birth()} | "
        f"age: {client.get_age()} | "
        f"vehicles: {vehicles_text}"
    )


def print_worker(worker):
    print(
        f"Admin | id: {worker.get_id()} | "
        f"name: {worker.get_name()} | "
        f"birth: {worker.get_date_of_birth()} | "
        f"age: {worker.get_age()} | "
        f"role: {worker.get_role()}"
    )


def print_rental(rental):
    print(
        f"Rental | id: {rental.get_rental_id()} | "
        f"vehicle: {rental.get_vehicle().get_license_plate()} | "
        f"user id: {rental.get_user().get_id()} | "
        f"start: {rental.get_start_date()} | "
        f"end: {rental.get_end_date()} | "
        f"kms: {rental.get_kms_done()}/{rental.get_kms_allowed()} | "
        f"assurance: {rental.get_assurance()} | "
        f"active: {rental.is_active()}"
    )


def save_after_action(shop, action):
    try:
        action()
        shop.save_all_csv()
        print("Operation completed and saved.")
    except Exception as error:
        print(f"Error: {error.__class__.__name__}. {error}")


def run_query(action):
    try:
        action()
    except Exception as error:
        print(f"Error: {error.__class__.__name__}. {error}")


def add_vehicle(shop):
    print("Vehicle type:")
    print("1. Car")
    print("2. Motorbike")
    print("3. Truck")
    option = ask_option("Choose vehicle type: ", ["1", "2", "3"])

    brand = ask_text("Brand: ")
    color = ask_text("Color: ")
    license_plate = ask_license_plate()
    model = ask_text("Model: ")
    matriculation_date = ask_date("Matriculation date (YYYY-MM-DD): ")
    mileage = ask_int("Mileage: ", min_value=0)

    vehicle_class = VEHICLE_TYPES[option]
    vehicle = vehicle_class(brand, color, license_plate, model, matriculation_date, mileage)
    shop.add_vehicle(vehicle)


def show_vehicles(shop):
    vehicles = shop.get_vehicles()
    if len(vehicles) == 0:
        print("There are no vehicles.")
        return
    for vehicle in vehicles:
        print_vehicle(vehicle)


def find_vehicle(shop):
    vehicle = shop.find_vehicle(ask_license_plate())
    print_vehicle(vehicle)


def update_vehicle(shop):
    license_plate = ask_license_plate()
    brand = ask_text("New brand (leave empty to keep current): ", optional=True)
    color = ask_text("New color (leave empty to keep current): ", optional=True)
    model = ask_text("New model (leave empty to keep current): ", optional=True)
    mileage = ask_int("New mileage (leave empty to keep current): ", min_value=0, optional=True)
    shop.update_vehicle_info(license_plate, brand=brand, color=color, model=model, mileage=mileage)


def register_maintenance(shop):
    license_plate = ask_license_plate()
    vehicle = shop.find_vehicle(license_plate)
    maintenance_date = ask_date("Maintenance date (YYYY-MM-DD): ")
    maintenance_mileage = ask_int("Maintenance mileage: ", min_value=0, max_value=vehicle.get_mileage())
    shop.register_vehicle_maintenance(license_plate, maintenance_date, maintenance_mileage)


def show_vehicle_itv_and_maintenance(shop):
    vehicle = shop.find_vehicle(ask_license_plate())
    print_vehicle(vehicle)
    print(f"Next ITV: {vehicle.calculate_ITV()}")
    print(f"Next maintenance: {vehicle.maintenance_schedule()}")


def vehicle_menu(shop):
    while True:
        print("\nVEHICLES")
        print("1. Add vehicle")
        print("2. Show all vehicles")
        print("3. Find vehicle")
        print("4. Update vehicle information")
        print("5. Register maintenance")
        print("6. Show next ITV and maintenance")
        print("0. Back")
        option = input("Choose an option: ").strip()

        if option == "1":
            save_after_action(shop, lambda: add_vehicle(shop))
        elif option == "2":
            run_query(lambda: show_vehicles(shop))
        elif option == "3":
            run_query(lambda: find_vehicle(shop))
        elif option == "4":
            save_after_action(shop, lambda: update_vehicle(shop))
        elif option == "5":
            save_after_action(shop, lambda: register_maintenance(shop))
        elif option == "6":
            run_query(lambda: show_vehicle_itv_and_maintenance(shop))
        elif option == "0":
            return
        else:
            print("Invalid option.")


def add_client(shop):
    name = ask_text("Name: ")
    birth_date = ask_date("Date of birth (YYYY-MM-DD): ")
    user_id = ask_int("Client ID (leave empty to generate automatically): ", min_value=1, optional=True)
    client = Client(name, birth_date, user_id)
    shop.add_client(client)
    print(f"Client ID: {client.get_id()}")


def show_clients(shop):
    clients = shop.get_clients()
    if len(clients) == 0:
        print("There are no clients.")
        return
    for client in clients:
        print_client(client)


def find_client(shop):
    client = shop.find_client(ask_int("Client ID: ", min_value=1))
    print_client(client)


def update_client(shop):
    client_id = ask_int("Client ID: ", min_value=1)
    name = ask_text("New name (leave empty to keep current): ", optional=True)
    birth_date = ask_date("New date of birth (leave empty to keep current): ", optional=True)
    shop.update_client_info(client_id, name=name, date_of_birth=birth_date)


def register_vehicle_to_client(shop):
    client_id = ask_int("Client ID: ", min_value=1)
    license_plate = ask_license_plate()
    shop.register_vehicle_to_client(client_id, license_plate)


def remove_vehicle_from_client(shop):
    client_id = ask_int("Client ID: ", min_value=1)
    license_plate = ask_license_plate()
    shop.remove_vehicle_from_client(client_id, license_plate)


def update_client_vehicle_kms(shop):
    client_id = ask_int("Client ID: ", min_value=1)
    license_plate = ask_license_plate()
    kms = ask_int("New mileage: ", min_value=0)
    shop.update_client_vehicle_kms(client_id, license_plate, kms)


def show_client_vehicle_dates(shop):
    client_id = ask_int("Client ID: ", min_value=1)
    license_plate = ask_license_plate()
    next_itv = shop.get_client_vehicle_next_itv(client_id, license_plate)
    next_maintenance = shop.get_client_vehicle_next_maintenance(client_id, license_plate)
    print(f"Next ITV: {next_itv}")
    print(f"Next maintenance: {next_maintenance}")


def client_menu(shop):
    while True:
        print("\nCLIENTS")
        print("1. Add client")
        print("2. Show all clients")
        print("3. Find client")
        print("4. Update client information")
        print("5. Register existing vehicle to client")
        print("6. Remove vehicle from client")
        print("7. Update kms of client's vehicle")
        print("8. Show ITV and maintenance for client's vehicle")
        print("0. Back")
        option = input("Choose an option: ").strip()

        if option == "1":
            save_after_action(shop, lambda: add_client(shop))
        elif option == "2":
            run_query(lambda: show_clients(shop))
        elif option == "3":
            run_query(lambda: find_client(shop))
        elif option == "4":
            save_after_action(shop, lambda: update_client(shop))
        elif option == "5":
            save_after_action(shop, lambda: register_vehicle_to_client(shop))
        elif option == "6":
            save_after_action(shop, lambda: remove_vehicle_from_client(shop))
        elif option == "7":
            save_after_action(shop, lambda: update_client_vehicle_kms(shop))
        elif option == "8":
            run_query(lambda: show_client_vehicle_dates(shop))
        elif option == "0":
            return
        else:
            print("Invalid option.")


def add_worker(shop):
    name = ask_text("Name: ")
    birth_date = ask_date("Date of birth (YYYY-MM-DD): ")
    role = ask_role()
    user_id = ask_int("Worker ID (leave empty to generate automatically): ", min_value=1, optional=True)
    worker = Admin(name, birth_date, role, user_id)
    shop.add_worker(worker)
    print(f"Worker ID: {worker.get_id()}")


def show_workers(shop):
    workers = shop.get_workers()
    if len(workers) == 0:
        print("There are no workers.")
        return
    for worker in workers:
        print_worker(worker)


def find_worker(shop):
    worker = shop.find_worker(ask_int("Worker ID: ", min_value=1))
    print_worker(worker)


def update_worker(shop):
    worker_id = ask_int("Worker ID: ", min_value=1)
    name = ask_text("New name (leave empty to keep current): ", optional=True)
    birth_date = ask_date("New date of birth (leave empty to keep current): ", optional=True)
    role = ask_role(optional=True)
    shop.update_worker_info(worker_id, name=name, date_of_birth=birth_date, role=role)


def worker_menu(shop):
    while True:
        print("\nWORKERS / ADMINS")
        print("1. Add worker/admin")
        print("2. Show all workers/admins")
        print("3. Find worker/admin")
        print("4. Update worker/admin information")
        print("0. Back")
        option = input("Choose an option: ").strip()

        if option == "1":
            save_after_action(shop, lambda: add_worker(shop))
        elif option == "2":
            run_query(lambda: show_workers(shop))
        elif option == "3":
            run_query(lambda: find_worker(shop))
        elif option == "4":
            save_after_action(shop, lambda: update_worker(shop))
        elif option == "0":
            return
        else:
            print("Invalid option.")


def create_rental(shop):
    rental_id = ask_text("Rental ID: ")
    license_plate = ask_license_plate()
    client_id = ask_int("Client ID: ", min_value=1)
    start_date = ask_date("Start date (YYYY-MM-DD): ")
    end_date = ask_date("End date (YYYY-MM-DD): ")
    kms_allowed = ask_int("Kms allowed: ", min_value=1)
    assurance = ask_assurance()

    vehicle = shop.find_vehicle(license_plate)
    client = shop.find_client(client_id)
    rental = Rental(rental_id, vehicle, client, start_date, end_date, kms_allowed, assurance)
    shop.add_rental(rental)


def show_rentals(shop):
    rentals = shop.get_rentals()
    if len(rentals) == 0:
        print("There are no rentals.")
        return
    for rental in rentals:
        print_rental(rental)


def show_active_rentals(shop):
    rentals = shop.get_active_rentals()
    if len(rentals) == 0:
        print("There are no active rentals.")
        return
    for rental in rentals:
        print_rental(rental)


def find_rental(shop):
    rental = shop.find_rental(ask_text("Rental ID: "))
    print_rental(rental)


def add_kms_to_rental(shop):
    rental_id = ask_text("Rental ID: ")
    kms = ask_int("Kms to add: ", min_value=1)
    shop.add_kms_to_rental(rental_id, kms)


def update_rental_assurance(shop):
    rental_id = ask_text("Rental ID: ")
    assurance = ask_assurance()
    shop.update_rental_assurance(rental_id, assurance)


def remove_rental(shop):
    rental_id = ask_text("Rental ID: ")
    shop.remove_rental(rental_id)


def rental_menu(shop):
    while True:
        print("\nRENTALS")
        print("1. Create rental")
        print("2. Show all rentals")
        print("3. Show active rentals")
        print("4. Find rental")
        print("5. Add kms to rental")
        print("6. Update rental assurance")
        print("7. Remove rental")
        print("0. Back")
        option = input("Choose an option: ").strip()

        if option == "1":
            save_after_action(shop, lambda: create_rental(shop))
        elif option == "2":
            run_query(lambda: show_rentals(shop))
        elif option == "3":
            run_query(lambda: show_active_rentals(shop))
        elif option == "4":
            run_query(lambda: find_rental(shop))
        elif option == "5":
            save_after_action(shop, lambda: add_kms_to_rental(shop))
        elif option == "6":
            save_after_action(shop, lambda: update_rental_assurance(shop))
        elif option == "7":
            save_after_action(shop, lambda: remove_rental(shop))
        elif option == "0":
            return
        else:
            print("Invalid option.")


def show_summary(shop):
    print("\nSYSTEM SUMMARY")
    print(f"Vehicles: {len(shop.get_vehicles())}")
    print(f"Clients: {len(shop.get_clients())}")
    print(f"Workers/admins: {len(shop.get_workers())}")
    print(f"Rentals: {len(shop.get_rentals())}")
    print(f"Active rentals: {len(shop.get_active_rentals())}")


def show_main_menu():
    print("\nVEHICLE RENTAL SYSTEM")
    print("1. Vehicle operations")
    print("2. Client operations")
    print("3. Worker/Admin operations")
    print("4. Rental operations")
    print("5. System summary")
    print("6. Save")
    print("0. Save and exit")


def main():
    prepare_environment()
    shop = ShopManagement()

    try:
        shop.load_all_csv()
        print("Data loaded successfully.")
    except Exception as error:
        print(f"Error loading CSV files: {error.__class__.__name__}. {error}")

    while True:
        show_main_menu()
        option = input("Choose an option: ").strip()

        if option == "1":
            vehicle_menu(shop)
        elif option == "2":
            client_menu(shop)
        elif option == "3":
            worker_menu(shop)
        elif option == "4":
            rental_menu(shop)
        elif option == "5":
            run_query(lambda: show_summary(shop))
        elif option == "6":
            save_after_action(shop, lambda: None)
        elif option == "0":
            try:
                shop.save_all_csv()
                print("Data saved. Goodbye.")
            except Exception as error:
                print(f"Error saving CSV files: {error.__class__.__name__}. {error}")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
