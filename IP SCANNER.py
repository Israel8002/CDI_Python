import tkinter as tk
from tkinter import scrolledtext
import scapy.all as scapy
import socket
import getpass

def obtener_prefijo_ip_local():
    # Obteniendo la dirección IP local
    ip_local = socket.gethostbyname(socket.gethostname())
    # Separando la dirección IP en octetos
    octetos = ip_local.split('.')
    # Concatenando los primeros tres octetos con .0/24
    prefijo_ip = '.'.join(octetos[:3]) + ".0/24"
    return prefijo_ip

def obtener_nombre_host(ip):
    try:
        nombre_host = socket.gethostbyaddr(ip)[0]
        # Eliminar el texto ".occ.imss.gob.mx" del nombre de host si está presente
        nombre_host = nombre_host.replace(".occ.imss.gob.mx", "")
    except socket.herror:
        nombre_host = "N/D"
    return nombre_host

def obtener_nombre_usuario():
    return getpass.getuser()

def escanear(ip):
    solicitud_arp = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    solicitud_broadcast = broadcast/solicitud_arp
    lista_respuestas = scapy.srp(solicitud_broadcast, timeout=1, verbose=False)[0]
    
    lista_clientes = []
    for elemento in lista_respuestas:
        cliente_dict = {"ip": elemento[1].psrc, "mac": elemento[1].hwsrc, "nombre_host": obtener_nombre_host(elemento[1].psrc)}
        lista_clientes.append(cliente_dict)
    return lista_clientes

def imprimir_resultado():
    ip_objetivo = entry.get()
    if ip_objetivo:
        resultado_escaneo = escanear(ip_objetivo)
        texto_resultado.delete(1.0, tk.END)
        texto_resultado.insert(tk.END, "Dirección IP\t\tDirección MAC\t\tNombre de Host\n")
        texto_resultado.insert(tk.END, "---------------------------------------------------------\n")
        for cliente in resultado_escaneo:
            texto_resultado.insert(tk.END, f"{cliente['ip'].upper()}\t\t{cliente['mac'].upper()}\t\t{cliente['nombre_host'].upper()}\n")
    else:
        texto_resultado.delete(1.0, tk.END)
        texto_resultado.insert(tk.END, "Por favor, introduce una dirección IP válida.")

# Ventana principal
root = tk.Tk()
root.title("Escáner de IP")

# Marco para entrada y botón
marco_entrada = tk.Frame(root)
marco_entrada.pack(pady=10)

# Entrada para rango de IP
entry = tk.Entry(marco_entrada, width=40)
entry.insert(0, obtener_prefijo_ip_local())
entry.pack(side=tk.LEFT)

# Botón de escaneo
boton_escanear = tk.Button(marco_entrada, text="Escanear", command=imprimir_resultado)
boton_escanear.pack(side=tk.LEFT, padx=10)

# Marco para mostrar resultados
marco_resultado = tk.Frame(root)
marco_resultado.pack(pady=10)

# Scrollable text area for displaying results
texto_resultado = scrolledtext.ScrolledText(marco_resultado, width=60, height=20)
texto_resultado.pack()

root.mainloop()