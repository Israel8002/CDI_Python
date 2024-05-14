from CTkMessagebox import CTkMessagebox
import customtkinter
import socket
import wmi
import psutil
import sqlite3
import os

class App:
    def __init__(self):
        self.direccion_ip = ""
        self.direccion_mac = ""
        self.nombre_equipo = ""
        self.nombre_usuario = ""
        self.nombre_dominio = ""
        self.nombre_marca = ""
        self.nombre_modelo = ""
        self.numero_serial = ""
        self.nombre_sistema_operativo = ""
        self.nombre_procesador = ""
        self.velocidad_procesador = ""
        self.ram_total = ""

        self.app = customtkinter.CTk()
        self.app.title("INVENTARIO DE EQUIPO")  # Agregar título a la ventana
        
        # Frame para Label1 y Label2
        frame1 = customtkinter.CTkFrame(self.app)
        frame1.pack(padx=5, pady=10)

        self.info_label1 = customtkinter.CTkLabel(frame1, text="", justify="left", font=("Helvetica", 12, "bold"))
        self.info_label1.pack(side="left")  # Alineado a la izquierda
        
        self.info_label2 = customtkinter.CTkLabel(frame1, text="", justify="right", font=("Helvetica", 12))
        self.info_label2.pack(side="right")  # Alineado a la derecha
        
        # Frame para Label3 y el botón
        frame2 = customtkinter.CTkFrame(self.app)
        frame2.pack(padx=5, pady=10)
        
        #POR SI SE REQUIERE AGREGAR UNA ETIQUETA ANTES DEL BOTON ENVIAR INFORMACION
        #self.info_label3 = customtkinter.CTkLabel(frame2, text="VERIFICA LA INFORMACIÓN", justify="center", font=("Helvetica", 12, "bold"))
        #self.info_label3.pack()  # Alineado al centro en la segunda línea

        self.button = customtkinter.CTkButton(frame2, text="ENVIAR", command=self.guardar_informacion)
        self.button.pack(padx=0, pady=0)  # Alineado debajo del Label3 en la misma línea

        # Mostrar información automáticamente al iniciar la aplicación
        self.mostrar_informacion()

    def mostrar_informacion(self):
        self.obtener_informacion_del_sistema()
        self.obtener_direccion_ip()
        self.obtener_direccion_mac()
        info_text = (
            f"NOMBRE DE EQUIPO:\n"
            f"NOMBRE DE USUARIO:\n"
            f"DOMINIO:\n"
            f"MARCA:\n"
            f"MODELO:\n"
            f"NÚMERO DE SERIE:\n"
            f"SISTEMA OPERATIVO:\n"
            f"PROCESADOR:\n"
            f"VELOCIDAD DEL PROCESADOR:\n"
            f"RAM TOTAL:\n"
            f"DIRECCIÓN IP DEL EQUIPO:\n"
            f"DIRECCIÓN MAC DE LA TARJETA DE RED:\n"
        )
        self.info_label1.configure(text=info_text)
        
        info_text2 = (
            f"{self.nombre_equipo}\n"
            f"{self.nombre_usuario}\n"
            f"{self.nombre_dominio}\n"
            f"{self.nombre_marca}\n"
            f"{self.nombre_modelo}\n"
            f"{self.numero_serial}\n"
            f"{self.nombre_sistema_operativo}\n"
            f"{self.nombre_procesador}\n"
            f"{self.velocidad_procesador}\n"
            f"{self.ram_total} GB\n"
            f"{self.direccion_ip}\n"
            f"{self.direccion_mac}\n"
        )
        self.info_label2.configure(text=info_text2)

    def guardar_informacion(self):
        try:
            # Comprobar si la base de datos ya existe
            db_path = r"\\172.27.34.29\Compartido\BD_Inventario.db"
            db_exists = os.path.exists(db_path)
            
            # Conectar a la base de datos
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Crear la tabla si la base de datos no existe
            if not db_exists:
                cursor.execute('''CREATE TABLE inventario (
                                id INTEGER PRIMARY KEY,
                                numero_serial TEXT, 
                                nombre_equipo TEXT,
                                nombre_usuario TEXT,
                                nombre_dominio TEXT,
                                nombre_marca TEXT,
                                nombre_modelo TEXT,
                                nombre_sistema_operativo TEXT,
                                nombre_procesador TEXT,
                                velocidad_procesador TEXT,
                                ram_total TEXT,
                                direccion_ip TEXT,
                                direccion_mac TEXT
                                )''')

            # Insertar los datos del equipo en la base de datos
            cursor.execute('''INSERT INTO inventario (numero_serial, nombre_equipo, nombre_usuario, nombre_dominio, nombre_marca, 
                            nombre_modelo, nombre_sistema_operativo, nombre_procesador, velocidad_procesador,
                            ram_total, direccion_ip, direccion_mac) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (self.numero_serial, self.nombre_equipo, self.nombre_usuario, self.nombre_dominio, self.nombre_marca,
                            self.nombre_modelo, self.nombre_sistema_operativo, self.nombre_procesador,
                            self.velocidad_procesador, self.ram_total, self.direccion_ip, self.direccion_mac))
            
            # Confirmar la transacción y cerrar la conexión
            conn.commit()
            conn.close()

            # Mostrar mensaje de éxito y cerrar aplicación
            msg = CTkMessagebox(title = f"Gracias {self.nombre_usuario}", message = "Los datos se han guardado en la base de datos remota.", option_1 = "Cerrar")
            if msg.get()=="Cerrar":
                self.app.destroy()
       
        except Exception as e:
            print("Error al guardar los datos:", str(e))

       
    def obtener_informacion_del_sistema(self):
        try:
            c = wmi.WMI()
            sistema = c.Win32_ComputerSystem()[0]
            self.nombre_equipo = sistema.Name
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
            print(str(e))

    def obtener_direccion_ip(self):
        try:
            nombre_host = socket.gethostname()
            self.direccion_ip = socket.gethostbyname(nombre_host)
            self.direccion_ip_temporal = self.direccion_ip.rsplit('.', 1)[0] + '.'
        except Exception as e:
            print("No se pudo obtener la dirección IP del equipo.")

    def obtener_direccion_mac(self):
        try:
            interfaces_red = psutil.net_if_addrs()
            for nombre, direcciones in interfaces_red.items():
                for direccion in direcciones:
                    if direccion.family == socket.AF_INET:
                        if psutil.net_if_stats()[nombre].isup:
                            stats = psutil.net_io_counters(pernic=True)[nombre]
                            if stats.bytes_sent > 0 or stats.bytes_recv > 0:
                                mac_address = next((addr for addr in direcciones if addr.family == psutil.AF_LINK), None).address
                                self.direccion_mac = mac_address
                                return self.direccion_mac
        except Exception as e:
            print("No se pudo obtener la dirección MAC de la tarjeta Ethernet.")

    def run(self):
        self.app.mainloop()
        

if __name__ == "__main__":
    app = App()
    app.run()


