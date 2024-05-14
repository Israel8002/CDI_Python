import tkinter as tk
from tkinter import ttk
import sqlite3

def display_data():
    try:
        # Conexión a la base de datos remota (SQLite)
        conn = sqlite3.connect('//172.27.34.29/Compartido/Referencias.db')
        cursor = conn.cursor()

        # Consulta para seleccionar todos los datos de la tabla Referencias
        cursor.execute('''SELECT * FROM Referencias''')
        rows = cursor.fetchall()

        # Crear ventana principal
        root = tk.Tk()
        root.title("Datos de la Base de Datos")

        # Crear un Treeview (tabla) para mostrar los datos
        tree = ttk.Treeview(root)
        tree["columns"] = ("1", "2", "3")

        # Configurar columnas
        tree.column("#0", width=0, stretch=tk.NO)  # Columna invisible
        tree.column("1", anchor=tk.CENTER, width=100)
        tree.column("2", anchor=tk.CENTER, width=100)
        tree.column("3", anchor=tk.CENTER, width=100)

        # Encabezados de columnas
        tree.heading("1", text="IP")
        tree.heading("2", text="REFERENCIA")
        tree.heading("3", text="UNIDAD")

        # Insertar datos en la tabla
        for row in rows:
            tree.insert("", tk.END, values=row)

        # Mostrar tabla
        tree.pack(expand=tk.YES, fill=tk.BOTH)

        # Cerrar la conexión a la base de datos
        conn.close()

        # Ejecutar el bucle principal de Tkinter
        root.mainloop()
    except sqlite3.Error as e:
        print("Error al mostrar datos:", e)

# Llamar a la función para mostrar los datos
display_data()
