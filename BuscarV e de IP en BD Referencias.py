import tkinter as tk
import socket
import sqlite3

def get_ip():
    try:
        # Intenta obtener el nombre de host y la dirección IP
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        # Conexión a la base de datos SQLite
        conn = sqlite3.connect(r'\\172.27.34.29\Compartido\Catalogo_Referencias.db')
        cursor = conn.cursor()
        
        # Extrae los primeros 3 valores de la dirección IP
        ip_prefijo = '.'.join(ip_address.split('.')[:3])
        
        # Consulta la base de datos para encontrar una coincidencia con el prefijo de la dirección IP
        cursor.execute("SELECT ID, Unidad FROM DATOS_UNIDAD WHERE IP LIKE ?", (ip_prefijo + '%',))
        result = cursor.fetchone()
        
        if result:
            return ip_address, result[0], result[1]  # IP, ID, Unidad
        else:
            return ip_address, "No encontrado", "No encontrado"
        
    except (socket.gaierror, sqlite3.Error) as e:
        # Maneja el caso en el que falla obtener la dirección IP o la conexión a la base de datos
        print("Error:", e)
        return "Unknown", "No encontrado", "No encontrado"

# Crea la ventana principal
root = tk.Tk()
root.title("Dirección IP")

# Obtiene la dirección IP y la información de la base de datos
ip_address, id_unidad, unidad = get_ip()

# Crea etiquetas para mostrar la información
label_ip = tk.Label(root, text="Dirección IP: " + ip_address)
label_ip.grid(row=0, column=0, padx=10, pady=10)

label_id_unidad = tk.Label(root, text="ID Unidad: " + str(id_unidad))
label_id_unidad.grid(row=1, column=0, padx=10, pady=10)

label_unidad = tk.Label(root, text="Unidad: " + unidad)
label_unidad.grid(row=2, column=0, padx=10, pady=10)

# Ejecuta el ciclo de eventos principal de Tkinter
root.mainloop()
