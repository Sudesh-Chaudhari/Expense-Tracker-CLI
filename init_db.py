import sqlite3

DB_NAME = "expenses.db"

def get_connection():
    """Return a new database connection and cursor."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor

def initialize_database():
    conn, cursor = get_connection()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("\nDatabase initialized successfully.\n")
