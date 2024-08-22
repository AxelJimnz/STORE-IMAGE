import sqlite3

# Crear conexión con la base de datos
conn = sqlite3.connect('image_app.db')
cursor = conn.cursor()

# Crear tabla de usuarios
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                  )''')

# Crear tabla para las imágenes
cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_name TEXT NOT NULL,
                    image_path TEXT NOT NULL
                  )''')

conn.commit()
conn.close()