import sqlite3

def database():
    return sqlite3.connect("database/sqlite3.db")