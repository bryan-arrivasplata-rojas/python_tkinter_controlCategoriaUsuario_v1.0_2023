import sqlite3

# Crear una conexión a la base de datos
conn = sqlite3.connect('database/sqlite3.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Crear la tabla "rol"
cursor.execute("""
    CREATE TABLE IF NOT EXISTS rol (
        id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
""")

# Crear la tabla de usuarios
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        id_perfil INTEGER NOT NULL,
        id_rol INTEGER NOT NULL,
        FOREIGN KEY (id_perfil) REFERENCES perfil (id_perfil),
        FOREIGN KEY (id_rol) REFERENCES rol (id_rol)
    )
""")

# Crear la tabla de perfiles
cursor.execute("""
    CREATE TABLE IF NOT EXISTS perfil (
        id_perfil INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        direccion TEXT,
        telefono TEXT
    )
""")

# Crear la tabla de categorías de producto
cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria_producto (
        id_categoria_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        id_usuario INTEGER NOT NULL UNIQUE,
        FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
    )
""")

# Crear la tabla de productos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS producto (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        id_categoria_producto INTEGER NOT NULL,
        FOREIGN KEY (id_categoria_producto) REFERENCES categoria_producto (id_categoria_producto)
    )
""")

# Guardar los cambios y cerrar la conexión
conn.commit()

# Tabla "rol"
roles = ["administrador", "usuario"]
for nombre_rol in roles:
    cursor.execute("INSERT INTO rol (nombre) VALUES (?)", (nombre_rol,))
conn.commit()

# Tabla "perfil"
perfiles = [
    {"nombre": "Juan", "apellido": "Pérez", "direccion": "Calle 123", "telefono": "1234567890"},
    {"nombre": "María", "apellido": "López", "direccion": "Avenida 456", "telefono": "9876543210"},
    {"nombre": "Pedro", "apellido": "Gómez", "direccion": "Plaza 789", "telefono": "4567891230"},
    {"nombre": "Julio", "apellido": "Fernandez", "direccion": "Plaza 789", "telefono": "123456789"},
    {"nombre": "Bryan", "apellido": "Arrivasplata", "direccion": "Plaza 789", "telefono": "997767771"}
]
for perfil in perfiles:
    cursor.execute("INSERT INTO perfil (nombre, apellido, direccion, telefono) VALUES (?, ?, ?, ?)",
                   (perfil["nombre"], perfil["apellido"], perfil["direccion"], perfil["telefono"]))
conn.commit()

# Tabla "usuario"
usuarios = [
    {"usuario": "user1", "password": "pass1", "id_perfil": 1, "id_rol": 2},
    {"usuario": "user2", "password": "pass2", "id_perfil": 2, "id_rol": 2},
    {"usuario": "user3", "password": "pass3", "id_perfil": 3, "id_rol": 2},
    {"usuario": "user4", "password": "pass4", "id_perfil": 4, "id_rol": 2},
    {"usuario": "admin", "password": "admin", "id_perfil": 5, "id_rol": 1}
]
for usuario in usuarios:
    cursor.execute("INSERT INTO usuario (usuario, password, id_perfil, id_rol) VALUES (?, ?, ?, ?)",
                   (usuario["usuario"], usuario["password"], usuario["id_perfil"], usuario["id_rol"]))
conn.commit()

# Tabla "categoria_producto"
categorias = [{"nombre_categoria":"Electrónica","id_usuario":1},
            {"nombre_categoria":"Ropa","id_usuario":2},
            {"nombre_categoria":"Hogar","id_usuario":3}]
for categoria in categorias:
    cursor.execute("INSERT INTO categoria_producto (nombre,id_usuario) VALUES (?,?)", (categoria['nombre_categoria'],categoria['id_usuario'],))
conn.commit()

# Tabla "producto"
productos = [
    {"nombre": "Televisor", "id_categoria_producto": 1},
    {"nombre": "Camiseta", "id_categoria_producto": 2},
    {"nombre": "Sartén", "id_categoria_producto": 3},
    {"nombre": "Laptop", "id_categoria_producto": 1},
    {"nombre": "Pantalón", "id_categoria_producto": 2},
    {"nombre": "Vaso", "id_categoria_producto": 3},
    {"nombre": "Smartphone", "id_categoria_producto": 1},
    {"nombre": "Chaqueta", "id_categoria_producto": 2},
    {"nombre": "Cuchillo", "id_categoria_producto": 3},
    {"nombre": "Tablet", "id_categoria_producto": 1},
    {"nombre": "Zapatos", "id_categoria_producto": 2},
    {"nombre": "Taza", "id_categoria_producto": 3},
    {"nombre": "Monitor", "id_categoria_producto": 1},
    {"nombre": "Camisa", "id_categoria_producto": 2},
    {"nombre": "Plato", "id_categoria_producto": 3},
    {"nombre": "Impresora", "id_categoria_producto": 1},
    {"nombre": "Shorts", "id_categoria_producto": 2},
    {"nombre": "Cubiertos", "id_categoria_producto": 3},
    {"nombre": "Proyector", "id_categoria_producto": 1},
    {"nombre": "Vestido", "id_categoria_producto": 2},
    {"nombre": "Tenedor", "id_categoria_producto": 3},
    {"nombre": "Altavoz", "id_categoria_producto": 1},
    {"nombre": "Bolso", "id_categoria_producto": 2},
]
for producto in productos:
    cursor.execute("INSERT INTO producto (nombre, id_categoria_producto) VALUES (?, ?)",
                   (producto["nombre"], producto["id_categoria_producto"]))
conn.commit()

conn.close()