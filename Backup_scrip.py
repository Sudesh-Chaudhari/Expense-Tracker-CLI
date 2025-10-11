import sqlite3

def backup_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    try:
        cursor.execute("DROP TABLE IF EXISTS expenses_backup")
        cursor.execute("CREATE TABLE expenses_backup AS SELECT * FROM expenses")
        conn.commit()
        print("Backup created as 'expenses_backup'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    backup_expenses()
