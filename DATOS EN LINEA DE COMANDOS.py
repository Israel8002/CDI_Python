# Importar las librerías necesarias
import socket
import uuid
import os
import platform
import subprocess
import psutil

# Obtener el nombre de host de la máquina local
hostname = socket.gethostname()

# Obtener el nombre de usuario
username = os.getlogin()

# Obtener el dominio (si está en un dominio)
domain = os.environ.get('USERDOMAIN')

# Obtener la dirección IP asociada al nombre de host
ip_address = socket.gethostbyname(hostname)

# Obtener la dirección MAC del dispositivo
mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])

# Obtener el número de serie del equipo (solo para sistemas Windows)
if platform.system() == "Windows":
    serial_number = subprocess.check_output(['wmic', 'bios', 'get', 'serialnumber']).decode().strip().split('\n')[1].strip()
else:
    serial_number = "N/A"

# Obtener la marca y el modelo del equipo
if platform.system() == "Windows":
    manufacturer = subprocess.check_output(['wmic', 'computersystem', 'get', 'manufacturer']).decode().strip().split('\n')[1].strip()
    model = subprocess.check_output(['wmic', 'computersystem', 'get', 'model']).decode().strip().split('\n')[1].strip()
else:
    manufacturer = "N/A"
    model = "N/A"

# Obtener el sistema operativo y la versión
operating_system = platform.system() + " " + platform.release()

# Obtener el nombre del procesador y la velocidad (en MHz)
processor_name = platform.processor()
processor_speed_mhz = psutil.cpu_freq().current

# Obtener la cantidad total de RAM instalada (en GB)
total_ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)

# Imprimir la información recolectada
print("Nombre del equipo:", hostname)
print("Nombre de usuario:", username)
print("Dominio:", domain if domain else "No está en un dominio")
print("Dirección IP:", ip_address)
print("Dirección MAC:", mac_address)
print("Número de serie del equipo:", serial_number)
print("Marca del equipo:", manufacturer)
print("Modelo del equipo:", model)
print("Sistema Operativo:", operating_system)
print("Nombre del Procesador:", processor_name)
print("Velocidad del Procesador:", processor_speed_mhz, "MHz")
print("RAM Total:", total_ram_gb, "GB")
