import sqlite3

def reset_expenses_ids():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    try:
        # 1. Create a temporary table without ID
        cursor.execute("""
            CREATE TABLE temp_expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL,
                note TEXT
            )
        """)

        # 2. Copy data into the new table
        cursor.execute("""
            INSERT INTO temp_expenses (date, category, amount, note)
            SELECT date, category, amount, note FROM expenses
        """)

        # 3. Drop the old table
        cursor.execute("DROP TABLE expenses")

        # 4. Rename temp table to original name
        cursor.execute("ALTER TABLE temp_expenses RENAME TO expenses")

        conn.commit()
        print("IDs reset successfully, starting again from 1.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    reset_expenses_ids()
