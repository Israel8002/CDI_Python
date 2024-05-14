import socket
import uuid
import os
import platform
import subprocess
import psutil
import tkinter as tk

def obtener_informacion():
    # Función para obtener la información del sistema

    # Función para obtener la información del sistema
    def obtener_datos_actualizados():
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

        # Actualizar los datos en las cajas de texto
        txt_hostname.delete(0, tk.END)
        txt_hostname.insert(0, hostname)

        txt_username.delete(0, tk.END)
        txt_username.insert(0, username)

        txt_domain.delete(0, tk.END)
        txt_domain.insert(0, domain)

        txt_ip_address.delete(0, tk.END)
        txt_ip_address.insert(0, ip_address)

        txt_mac_address.delete(0, tk.END)
        txt_mac_address.insert(0, mac_address)

        txt_serial_number.delete(0, tk.END)
        txt_serial_number.insert(0, serial_number)

        txt_manufacturer.delete(0, tk.END)
        txt_manufacturer.insert(0, manufacturer)

        txt_model.delete(0, tk.END)
        txt_model.insert(0, model)

        txt_operating_system.delete(0, tk.END)
        txt_operating_system.insert(0, operating_system)

        txt_processor_name.delete(0, tk.END)
        txt_processor_name.insert(0, processor_name)

        txt_processor_speed_mhz.delete(0, tk.END)
        txt_processor_speed_mhz.insert(0, processor_speed_mhz)

        txt_total_ram_gb.delete(0, tk.END)
        txt_total_ram_gb.insert(0, total_ram_gb)

    # Mostrar la información en la interfaz gráfica
    root = tk.Tk()
    root.title("Información del Sistema")

    tk.Label(root, text="Nombre del equipo:").grid(row=0, column=0)
    txt_hostname = tk.Entry(root)
    txt_hostname.grid(row=0, column=1)

    tk.Label(root, text="Nombre de usuario:").grid(row=1, column=0)
    txt_username = tk.Entry(root)
    txt_username.grid(row=1, column=1)

    tk.Label(root, text="Dominio:").grid(row=2, column=0)
    txt_domain = tk.Entry(root)
    txt_domain.grid(row=2, column=1)

    tk.Label(root, text="Dirección IP:").grid(row=3, column=0)
    txt_ip_address = tk.Entry(root)
    txt_ip_address.grid(row=3, column=1)

    tk.Label(root, text="Dirección MAC:").grid(row=4, column=0)
    txt_mac_address = tk.Entry(root)
    txt_mac_address.grid(row=4, column=1)

    tk.Label(root, text="Número de serie del equipo:").grid(row=5, column=0)
    txt_serial_number = tk.Entry(root)
    txt_serial_number.grid(row=5, column=1)

    tk.Label(root, text="Marca del equipo:").grid(row=6, column=0)
    txt_manufacturer = tk.Entry(root)
    txt_manufacturer.grid(row=6, column=1)

    tk.Label(root, text="Modelo del equipo:").grid(row=7, column=0)
    txt_model = tk.Entry(root)
    txt_model.grid(row=7, column=1)

    tk.Label(root, text="Sistema Operativo:").grid(row=8, column=0)
    txt_operating_system = tk.Entry(root)
    txt_operating_system.grid(row=8, column=1)

    tk.Label(root, text="Nombre del Procesador:").grid(row=9, column=0)
    txt_processor_name = tk.Entry(root)
    txt_processor_name.grid(row=9, column=1)

    tk.Label(root, text="Velocidad del Procesador (MHz):").grid(row=10, column=0)
    txt_processor_speed_mhz = tk.Entry(root)
    txt_processor_speed_mhz.grid(row=10, column=1)

    tk.Label(root, text="RAM Total (GB):").grid(row=11, column=0)
    txt_total_ram_gb = tk.Entry(root)
    txt_total_ram_gb.grid(row=11, column=1)

    # Agregar un botón para obtener los datos
    btn_obtener_datos = tk.Button(root, text="Obtener Datos", command=obtener_datos_actualizados)
    btn_obtener_datos.grid(row=12, columnspan=2)

    obtener_datos_actualizados()  # Llamar a la función para mostrar los datos iniciales

    root.mainloop()

obtener_informacion()