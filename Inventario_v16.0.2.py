import socket
import wmi
import psutil
import sqlite3
import os
import datetime

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
        self.arquitectura_sistema_operativo = ""
        self.nombre_procesador = ""
        self.velocidad_procesador = ""
        self.ram_total = ""
        self.modelo_disco_duro = ""
        self.capacidad_disco_duro = ""
        self.id_unidad = ""  
        self.nombre_unidad = ""
        self.numeros_serie_monitores = []
        self.tipo_dispositivo = ""

    def mostrar_informacion(self):
        self.obtener_informacion_del_sistema()
        self.obtener_direccion_ip()
        self.obtener_direccion_mac()
        self.obtener_numero_serie_monitor()
        self.tipo_dispositivo = self.es_laptop_o_pc()
        
        # Buscar en la base de datos y mostrar resultados de Ref y Unidad
        resultado_bd = self.buscar_en_bd(self.direccion_ip_temporal)
        if resultado_bd:
            id_unidad, nombre_unidad = resultado_bd
            self.id_unidad = id_unidad
            self.nombre_unidad = nombre_unidad
            print(f"Ref.{self.id_unidad} - {self.nombre_unidad}")
        else:
            print(f"No se encontró información en la base de datos para la dirección IP {self.direccion_ip}.")

        info_text = (
            f"NÚMERO DE SERIE: {self.numero_serial}\n"
            f"TIPO DE DISPOSITIVO: {self.tipo_dispositivo}\n"
            f"MARCA: {self.nombre_marca}\n"
            f"MODELO: {self.nombre_modelo}\n"
            f"NÚMEROS DE SERIE DE MONITOR(ES): {', '.join(self.numeros_serie_monitores)}\n"
            f"SISTEMA OPERATIVO: {self.nombre_sistema_operativo}\n"
            f"TIPO DE SISTEMA: {self.arquitectura_sistema_operativo}\n"
            f"PROCESADOR: {self.nombre_procesador}\n"
            f"VELOCIDAD DEL PROCESADOR: {self.velocidad_procesador} MHz\n"
            f"RAM TOTAL: {self.ram_total} GB\n"
            f"ALMACENAMIENTO: {self.modelo_disco_duro}\n"
            f"CAPACIDAD: {self.capacidad_disco_duro} GB\n"
            f"DIRECCIÓN IP DEL EQUIPO: {self.direccion_ip}\n"
            f"DIRECCIÓN MAC DE LA TARJETA DE RED: {self.direccion_mac}\n"
            f"NOMBRE DE EQUIPO: {self.nombre_equipo}\n"
            f"NOMBRE DE USUARIO: {self.nombre_usuario}\n"
            f"DOMINIO: {self.nombre_dominio}"
        )
        print(info_text)



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
                cursor.execute('''CREATE TABLE IF NOT EXISTS CDInventario (
                                numero_serial TEXT,
                                tipo_dispositivo TEXT,
                                id_unidad TEXT,
                                nombre_unidad TEXT,
                                nombre_equipo TEXT,
                                nombre_usuario TEXT,
                                nombre_dominio TEXT,
                                nombre_marca TEXT,
                                nombre_modelo TEXT,
                                numeros_serie_monitores TEXT, 
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

            cursor.execute('''INSERT INTO CDInventario VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (self.numero_serial, self.tipo_dispositivo, self.id_unidad, self.nombre_unidad, self.nombre_equipo, self.nombre_usuario, self.nombre_dominio, 
                self.nombre_marca, self.nombre_modelo, ', '.join(self.numeros_serie_monitores), self.nombre_sistema_operativo, self.arquitectura_sistema_operativo, self.nombre_procesador,
                self.velocidad_procesador, self.ram_total, self.modelo_disco_duro, self.capacidad_disco_duro, self.direccion_ip, self.direccion_mac,
                self.fecha_actual))

            conn.commit()
            conn.close()

            print(f"Gracias {self.nombre_usuario}, los datos se han guardado en la base de datos remota.")
        
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

    def obtener_numero_serie_monitor(self):
        try:
            w = wmi.WMI(namespace='root\\wmi')
            monitores = w.WmiMonitorID()
            self.numeros_serie_monitores = []
            for monitor in monitores:
                serial = "".join([chr(char) for char in monitor.SerialNumberID if char > 0])
                self.numeros_serie_monitores.append(serial)
        except Exception as e:
            print("No se pudo obtener el número de serie del monitor:", str(e))

    def es_laptop_o_pc(self):
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery is not None:
                return "Laptop"
        return "PC"

if __name__ == "__main__":
    app = App()
    app.mostrar_informacion()
    app.guardar_informacion()
