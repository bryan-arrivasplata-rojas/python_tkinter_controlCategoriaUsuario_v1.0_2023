import sqlite3
from database.conn import database


def get(query):
    conn = database()
    cursor = conn.cursor()
    cursor.execute(query)#f"SELECT * FROM {tabla}"
    result = cursor.fetchall()
    conn.close()
    return result
# Consulta POST: Insertar un nuevo registro en una tabla
def insert(query):
    conn = database()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        result = cursor.lastrowid
    except sqlite3.OperationalError:
        result = 0
    except sqlite3.IntegrityError:
        result = -1
    conn.close()
    return result

# Consulta PUT: Actualizar un registro existente en una tabla
def update_delete(query):
    conn = database()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        result = cursor.rowcount
    except sqlite3.OperationalError:
        result = 0
    except sqlite3.IntegrityError:
        result = -1
    conn.close()
    return result