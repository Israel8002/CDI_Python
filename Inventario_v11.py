import tkinter as tk
import tkinter.messagebox as messagebox
import wmi
import os
import sqlite3
import socket
import subprocess

class InformacionSistema:
    def __init__(self):
        # Inicialización de variables para almacenar la información del sistema
        self.nombre_equipo = None
        self.nombre_usuario = None
        self.nombre_dominio = None
        self.nombre_marca = None
        self.nombre_modelo = None
        self.numero_serial = None
        self.nombre_sistema_operativo = None
        self.nombre_procesador = None
        self.velocidad_procesador = None
        self.ram_total = None
        self.direccion_ip = None
        self.direccion_mac = None

    def obtener_informacion_del_sistema(self):
        try:
            # Usando el módulo wmi para obtener información del sistema
            c = wmi.WMI()
            sistema = c.Win32_ComputerSystem()[0]
            self.nombre_equipo = sistema.Name
            
            # Obtener solo el nombre de usuario sin el dominio
            usuario_completo = sistema.UserName
            if "\\" in usuario_completo:
                self.nombre_usuario = usuario_completo.split("\\")[1]
            else:
                self.nombre_usuario = usuario_completo
            
            self.nombre_dominio = sistema.Domain
            self.nombre_marca = sistema.Manufacturer
            self.nombre_modelo = sistema.Model

            bios = c.Win32_BIOS()[0]
            self.numero_serial = bios.SerialNumber

            info_sistema = c.Win32_OperatingSystem()[0]
            self.nombre_sistema_operativo = info_sistema.Caption

            procesador = c.Win32_Processor()[0]
            self.nombre_procesador = procesador.Name
            self.velocidad_procesador = procesador.MaxClockSpeed

            memoria = c.Win32_ComputerSystem()[0]
            self.ram_total = round(int(memoria.TotalPhysicalMemory) / (1024 ** 3), 2)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def obtener_direccion_ip(self):
        try:
            # Obtener el nombre del host
            nombre_host = socket.gethostname()
            # Obtener la dirección IP asociada al nombre del host
            self.direccion_ip = socket.gethostbyname(nombre_host)

            # Guardar la IP temporalmente sin el último octeto
            self.direccion_ip_temporal = self.direccion_ip.rsplit('.', 1)[0] + '.'

        except Exception as e:
            messagebox.showerror("Error", "No se pudo obtener la dirección IP del equipo.")

    def obtener_direccion_mac(self):
        try:
            # Ejecutar el comando wmic nicconfig get description,macaddress y capturar la salida
            resultado = subprocess.run(['wmic', 'nicconfig', 'get', 'description,macaddress'], capture_output=True, text=True)
            # Dividir la salida en líneas
            lineas = resultado.stdout.strip().split('\n')
            # Ignorar la primera línea (encabezado)
            lineas = lineas[1:]
            for linea in lineas:
                # Si la descripción de la tarjeta contiene 'Ethernet'
                if 'Ethernet' in linea:
                    # Separar la descripción y la dirección MAC
                    descripcion, direccion_mac = linea.strip().split(None, 1)
                    # Devolver solo la dirección MAC
                    self.direccion_mac = direccion_mac.strip()
                    # Solo devolver la dirección MAC sin la descripción
                    return self.direccion_mac
        except Exception as e:
            messagebox.showerror("Error", "No se pudo obtener la dirección MAC de la tarjeta Ethernet.")

class Aplicacion(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Inventario CDI - LSC Israel Díaz")
        self.informacion_sistema = InformacionSistema()
        self.crear_widgets()
        # Obtener la información del sistema al inicializar la aplicación
        self.informacion_sistema.obtener_informacion_del_sistema()
        self.informacion_sistema.obtener_direccion_ip()
        self.informacion_sistema.obtener_direccion_mac()
        self.actualizar_grid()
        self.centra_ventana()

    def crear_widgets(self):
        # Crear widgets de la interfaz gráfica
        self.grid = tk.LabelFrame(self, text="Datos de Inventario")
        self.grid.pack(padx=10, pady=10)
        
        self.etiquetas = ["ID Unidad:", "Nombre Unidad:", "Nombre de host:", "Nombre de usuario:", "Dominio:", "Marca:", "Modelo", "Número de serie:", "Nombre del SO:", "Nombre del procesador:",
                          "Velocidad del procesador:", "RAM total:", "Dirección IP:", "Dirección MAC:"]
        self.etiquetas_datos = {}

        for i, etiqueta in enumerate(self.etiquetas, start=1):
            etiqueta_widget = tk.Label(self.grid, text=etiqueta)
            etiqueta_widget.grid(row=i, column=0, sticky="w", padx=5, pady=5)

            dato_widget = tk.Label(self.grid, text="")
            dato_widget.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.etiquetas_datos[etiqueta] = dato_widget

        boton_enviar = tk.Button(self, text="Enviar Datos", command=self.enviar_datos)
        boton_enviar.pack(pady=10)

    def actualizar_grid(self):
        # Actualizar la interfaz gráfica con la información del sistema
        self.informacion_sistema.obtener_informacion_del_sistema()
        self.informacion_sistema.obtener_direccion_ip()
        self.informacion_sistema.obtener_direccion_mac()

        datos = {
            "Nombre de host:": self.informacion_sistema.nombre_equipo,
            "Nombre de usuario:": self.informacion_sistema.nombre_usuario,
            "Dominio:": self.informacion_sistema.nombre_dominio,
            "Marca:": self.informacion_sistema.nombre_marca,
            "Modelo": self.informacion_sistema.nombre_modelo,
            "Número de serie:": self.informacion_sistema.numero_serial,
            "Nombre del SO:": self.informacion_sistema.nombre_sistema_operativo,
            "Nombre del procesador:": self.informacion_sistema.nombre_procesador,
            "Velocidad del procesador:": f"{self.informacion_sistema.velocidad_procesador} MHz",
            "RAM total:": f"{self.informacion_sistema.ram_total} GB",
            "Dirección IP:": self.informacion_sistema.direccion_ip,
            "Dirección MAC:": self.informacion_sistema.direccion_mac,
            "ID Unidad:": "",  # Esto se actualizará después de la validación de IP
            "Nombre Unidad:": ""  # Esto se actualizará después de la validación de IP
        }

        for etiqueta, dato in datos.items():
            self.etiquetas_datos[etiqueta].config(text=dato)

        id_unidad, nombre_unidad = self.buscar_en_bd(self.informacion_sistema.direccion_ip_temporal)
        self.etiquetas_datos["ID Unidad:"].config(text=id_unidad)
        self.etiquetas_datos["Nombre Unidad:"].config(text=nombre_unidad)

    def buscar_en_bd(self, ip_temporal):
        # Conexión a la base de datos
        ruta_db = r"\\172.27.34.29\Compartido\Catalogo_Referencias.db"
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()

        # Ejecutar la consulta para encontrar la IP temporal en la base de datos
        cursor.execute("SELECT ID, UNIDAD FROM DATOS_UNIDAD WHERE IP LIKE ?", (ip_temporal + '%',))
        resultado = cursor.fetchone()

        # Cerrar conexión
        conn.close()

        if resultado:
            return resultado
        else:
            return ("No encontrado", "No encontrado")

    def enviar_datos(self):
        # Guardar los datos en una base de datos al hacer clic en el botón "Enviar Datos"
        ruta_db = r"\\172.27.34.29\Compartido\InventarioCDI.db"
        if not os.path.exists(ruta_db):
            conn = sqlite3.connect(ruta_db)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS InformacionSistema (
                                NumeroSerial TEXT,     
                                NombreEquipo TEXT,
                                NombreUsuario TEXT,
                                NombreDominio TEXT,
                                NombreMarca TEXT,
                                NombreModelo TEXT,
                                NombreSistemaOperativo TEXT,
                                NombreProcesador TEXT,
                                VelocidadProcesador TEXT,
                                RAMTotal TEXT,
                                DireccionIP TEXT,
                                DireccionMAC TEXT,
                                IDUnidad TEXT,
                                NombreUnidad TEXT)''')
        else:
            conn = sqlite3.connect(ruta_db)
            cursor = conn.cursor()

        try:
            cursor.execute('''INSERT INTO InformacionSistema VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (self.informacion_sistema.numero_serial, self.informacion_sistema.nombre_equipo, self.informacion_sistema.nombre_usuario, self.informacion_sistema.nombre_dominio, self.informacion_sistema.nombre_marca, 
                            self.informacion_sistema.nombre_modelo, self.informacion_sistema.nombre_sistema_operativo, self.informacion_sistema.nombre_procesador,
                            f"{self.informacion_sistema.velocidad_procesador} MHz", f"{self.informacion_sistema.ram_total} GB",
                            self.informacion_sistema.direccion_ip, self.informacion_sistema.direccion_mac,
                            self.etiquetas_datos["ID Unidad:"]["text"], self.etiquetas_datos["Nombre Unidad:"]["text"]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "¡Los datos se guardaron correctamente!")
            self.quit()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def centra_ventana(self):
        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Definir el margen superior
        margen_superior = 50

        # Calcular las coordenadas para centrar la ventana en la parte superior de la pantalla
        x = (ancho_pantalla - self.winfo_reqwidth()) / 2
        y = margen_superior

        # Actualizar la posición de la ventana
        self.geometry("+%d+%d" % (x, y))

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
