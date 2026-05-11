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