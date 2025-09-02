import os
import sys
import sqlite3

if getattr(sys, "frozen", False):
    DB_DIR = os.path.dirname(sys.executable)
else:
    DB_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(DB_DIR, "flights.db")

ALLOWED_COLUMNS = {"name", "flight_number", "departure", "destination", "date", "seat_number"}

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,          -- store as 'YYYY-MM-DD'
                seat_number TEXT NOT NULL
            )
        """)

def ensure_db():
    with get_connection() as _:
        pass
    create_table()

ensure_db()

def add_reservation(name, flight_number, departure, destination, date, seat_number):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, flight_number, departure, destination, date, seat_number))

def get_reservations():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, flight_number, departure, destination, date, seat_number
            FROM reservations
            ORDER BY id DESC
        """)
        return cur.fetchall()

def update_reservations(res_id, old_res, new_res):
    """
    Update a specific column (old_res) with a new value (new_res) for the given res_id.
    Example: update_reservations(3, "seat_number", "12A")
    """
    if old_res not in ALLOWED_COLUMNS:
        raise ValueError(f"Invalid column name: {old_res}")

    with get_connection() as conn:
        cur = conn.cursor()
        sql = f"UPDATE reservations SET {old_res} = ? WHERE id = ?"
        cur.execute(sql, (new_res, res_id))

def delete_reservation(res_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM reservations WHERE id = ?", (res_id,))

