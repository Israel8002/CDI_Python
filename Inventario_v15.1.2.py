from CTkMessagebox import CTkMessagebox
import customtkinter
import socket
import wmi
import psutil
import sqlite3
import os
import datetime 

class App:
    def __init__(self):
        self.etiquetas_datos = {}
        self.direccion_ip = ""
        self.direccion_mac = ""
        self.nombre_equipo = ""
        self.nombre_usuario = ""
        self.nombre_dominio = ""
        self.nombre_marca = ""
        self.nombre_modelo = ""
        self.numero_serial = ""
        self.nombre_sistema_operativo = ""
        self.arquitectura_sistema_operativo = ""
        self.nombre_procesador = ""
        self.velocidad_procesador = ""
        self.ram_total = ""
        self.modelo_disco_duro = ""
        self.capacidad_disco_duro = ""
        self.id_unidad = ""  
        self.nombre_unidad = ""  

        self.app = customtkinter.CTk()
        self.app.title("INVENTARIO DE EQUIPO")
        self.app.overrideredirect(True)
        
        frame0 = customtkinter.CTkFrame(self.app, corner_radius=30, fg_color=None)
        frame0.pack(padx=0, pady=0)
        
        #self.info_label3 = customtkinter.CTkLabel(frame0, text="", justify="center", font=("Abadi", 14, "bold"), text_color="red")
        self.info_label3 = customtkinter.CTkLabel(frame0, text="", justify="center", font=("Abadi", 14, "bold"))
        self.info_label3.pack(side="bottom")        
        
        #FRAME UNO --- DATOS OBTENIDOS ---
        frame1 = customtkinter.CTkFrame(self.app, corner_radius=30)
        frame1.pack(padx=0, pady=0)
        
        self.info_label1 = customtkinter.CTkLabel(frame1, text="", justify="left", font=("Abadi", 12, "bold"))
        self.info_label1.pack(side="left")

        self.info_label2 = customtkinter.CTkLabel(frame1, text="", justify="right", font=("Abadi", 12))
        self.info_label2.pack(side="right")
        
        #FRAME DOS --- BOTON ---
        frame2 = customtkinter.CTkFrame(self.app)
        frame2.pack(padx=10, pady=10)

        self.button = customtkinter.CTkButton(frame2, text="ENVIAR", command=self.guardar_informacion)
        self.button.pack(padx=0, pady=0)

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
            f"TIPO DE SISTEMA:\n"
            f"PROCESADOR:\n"
            f"VELOCIDAD DEL PROCESADOR:\n"
            f"RAM TOTAL:\n"
            f"ALMACENAMIENTO:\n"
            f"CAPACIDAD:\n"
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
            f"{self.arquitectura_sistema_operativo}\n"
            f"{self.nombre_procesador}\n"
            f"{self.velocidad_procesador}\n"
            f"{self.ram_total} GB\n"
            f"{self.modelo_disco_duro}\n"
            f"{self.capacidad_disco_duro}\n"
            f"{self.direccion_ip}\n"
            f"{self.direccion_mac}\n"
        )
        self.info_label2.configure(text=info_text2)

        info_text3 = (
            f"{self.id_unidad}"
            f"{self.nombre_unidad}"
        )
        

        # Buscar en la base de datos y mostrar resultados
        resultado_bd = self.buscar_en_bd(self.direccion_ip_temporal)
        if resultado_bd:
            id_unidad, nombre_unidad = resultado_bd
            self.id_unidad = id_unidad
            self.nombre_unidad = nombre_unidad
            info_text3 += f"Ref.{self.id_unidad}"
            info_text3 += f" - {self.nombre_unidad}"
            self.info_label3.configure(text=info_text3)
        else:
            
            msg = CTkMessagebox(title = f"Revisar {self.nombre_usuario}", message = "No se encontró información en la base de datos para esta dirección IP.", option_1 = "Cerrar")
            if msg.get()=="Cerrar":
                self.app.destroy()

    def buscar_en_bd(self, ip_temporal):
        ruta_db = r"\\172.27.34.29\Compartido\Catalogo_Referencias.db"
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()
        cursor.execute("SELECT ID, UNIDAD FROM DATOS_UNIDAD WHERE IP LIKE ?", (ip_temporal + '%',))
        resultado = cursor.fetchone()
        conn.close()

        return resultado
        
    def guardar_informacion(self):
        try:
            ruta_db = r"\\172.27.34.29\Compartido\BDInventario.db"
            if not os.path.exists(ruta_db):
                conn = sqlite3.connect(ruta_db)
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS Inventario (
                                numero_serial TEXT,
                                id_unidad TEXT,
                                nombre_unidad TEXT,
                                nombre_equipo TEXT,
                                nombre_usuario TEXT,
                                nombre_dominio TEXT,
                                nombre_marca TEXT,
                                nombre_modelo TEXT,
                                nombre_sistema_operativo TEXT,
                                nombre_tipo_sistema TEXT,
                                nombre_procesador TEXT,
                                velocidad_procesador TEXT,
                                ram_total TEXT,
                                disco_duro TEXT,
                                capacidad_disco TEXT,
                                direccion_ip TEXT,
                                direccion_mac TEXT,
                                fecha_actual TEXT
                                )''')
            else:
                conn = sqlite3.connect(ruta_db)
                cursor = conn.cursor()

                cursor.execute('''INSERT INTO Inventario VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
               (self.numero_serial,self.id_unidad, self.nombre_unidad, 
                self.nombre_equipo, self.nombre_usuario, self.nombre_dominio, self.nombre_marca,
                self.nombre_modelo, self.nombre_sistema_operativo, self.arquitectura_sistema_operativo, self.nombre_procesador,
                self.velocidad_procesador, self.ram_total, self.modelo_disco_duro, self.capacidad_disco_duro, self.direccion_ip, self.direccion_mac,
                self.fecha_actual))

                conn.commit()
                conn.close()

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
            disco_duro = c.Win32_DiskDrive()[0]
            self.modelo_disco_duro = disco_duro.Model
            self.capacidad_disco_duro = round(int(disco_duro.Size) / (1024 ** 3), 2)
            self.arquitectura_sistema_operativo = info_sistema.OSArchitecture
# El resto de tu código permanece igual

           # Obtener la fecha del sistema
            self.fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
