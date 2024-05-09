
#Descripción: Realtek USB GbE Family Controller
#Dirección física: C4-CB-E1-0D-8E-79


import socket
import subprocess

def obtener_direccion_ip():
    try:
        # Obtener el nombre del host
        nombre_host = socket.gethostname()
        # Obtener la dirección IP asociada al nombre del host
        direccion_ip = socket.gethostbyname(nombre_host)
        return direccion_ip
    except Exception as e:
        print("Error al obtener la dirección IP:", e)
        return None

def obtener_mac_address():
    try:
        # Ejecutar el comando wmic nicconfig get description,macaddress y capturar la salida
        resultado = subprocess.check_output(['wmic', 'nicconfig', 'get', 'description,macaddress'], universal_newlines=True)
        # Dividir la salida en líneas
        lineas = resultado.strip().split('\n')
        # Ignorar la primera línea (encabezado)
        lineas = lineas[1:]
        for linea in lineas:
            # Si la descripción de la tarjeta contiene 'Ethernet'
            if 'Ethernet' in linea:
                # Separar la descripción y la dirección MAC
                descripcion, mac_address = linea.strip().split(None, 1)
                return mac_address.strip()
    except Exception as e:
        print("Error al obtener la dirección MAC:", e)
        return None

# Ejemplo de uso
if __name__ == "__main__":
    # Obtener la dirección IP
    direccion_ip = obtener_direccion_ip()
    if direccion_ip:
        print("La dirección IP del equipo es:", direccion_ip)
    else:
        print("No se pudo obtener la dirección IP del equipo.")
    
    # Obtener la dirección MAC
    mac_address = obtener_mac_address()
    if mac_address:
        # Imprimir solo la dirección MAC
        print("La dirección MAC de la tarjeta Ethernet es:", mac_address.split()[-1])
    else:
        print("No se pudo obtener la dirección MAC de la tarjeta Ethernet.")
