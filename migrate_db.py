import sqlite3

def migrate_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # 1. Backup existing data
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses_backup AS SELECT * FROM expenses")

    # 2. Drop the old expenses table
    cursor.execute("DROP TABLE IF EXISTS expenses")

    # 3. Recreate with correct schema
    cursor.execute('''
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            note TEXT
        )
    ''')

    # 4. Copy data back (without old id values)
    cursor.execute('''
        INSERT INTO expenses (date, category, amount, note)
        SELECT date, category, amount, note FROM expenses_backup
    ''')

    conn.commit()
    conn.close()
    print("Migration complete. 'id' is now auto-incremented properly.")

if __name__ == "__main__":
    migrate_database()
