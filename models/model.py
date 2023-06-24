import sqlite3
from database.conn import database


def get(query):
    conn = database()
    cursor = conn.cursor()
    cursor.execute(query)#f"SELECT * FROM {tabla}"
    registros = cursor.fetchall()
    conn.close()
    return registros
# Consulta POST: Insertar un nuevo registro en una tabla
def insert(query):
    try:
        conn = database()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
        return cursor.lastrowid
    except Exception as e:
        conn.close()
        return 0

# Consulta PUT: Actualizar un registro existente en una tabla
def update_delete(query):
    conn = database()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    return cursor.rowcount