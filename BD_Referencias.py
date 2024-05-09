import sqlite3

def create_database():
    # Conexión a la base de datos remota (SQLite)
    conn = sqlite3.connect('//172.27.34.29/Compartido/Catalogo_Referencias.db')
    cursor = conn.cursor()

    # Creación de la tabla Referencias
    cursor.execute('''CREATE TABLE IF NOT EXISTS DATOS_UNIDAD (
                        IP TEXT,
                        ID TEXT,
                        UNIDAD TEXT
                        
                    )''')

    # Guardar y cerrar la conexión
    conn.commit()
    conn.close()

# Llamar a la función para crear la base de datos
create_database()
