import psutil
import socket

def verificar_conexion_internet():
    interfaces_red = psutil.net_if_addrs()
    for nombre, direcciones in interfaces_red.items():
        for direccion in direcciones:
            if direccion.family == socket.AF_INET:  # Verifica si es una dirección IPv4
                if psutil.net_if_stats()[nombre].isup:  # Verifica si la interfaz está activa
                    stats = psutil.net_io_counters(pernic=True)[nombre]
                    if stats.bytes_sent > 0 or stats.bytes_recv > 0:  # Verifica si la interfaz ha enviado o recibido bytes
                        ip_address = direccion.address
                        mac_address = next((addr for addr in direcciones if addr.family == psutil.AF_LINK), None).address
                        print(f"La interfaz {nombre} está conectada a internet.")
                        print(f"Dirección MAC de la interfaz: {mac_address}")
                        print(f"Dirección IP de la interfaz: {ip_address}")
                        return True
    print("No se encontraron interfaces conectadas a internet.")
    return False

# Uso
verificar_conexion_internet()
