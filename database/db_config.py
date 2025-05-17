import sqlite3

def connect_db():
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groceries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    return conn

def add_item(conn, item, quantity):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groceries (item, quantity) VALUES (?, ?)", (item, quantity))
    conn.commit()

def remove_item(conn, item):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM groceries WHERE item = ?", (item,))
    conn.commit()

def get_items(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT item, quantity FROM groceries")
    return cursor.fetchall()

