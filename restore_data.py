import sqlite3

def restore_from_backup():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Clear the main table (optional, if you want a fresh restore)
    cursor.execute("DELETE FROM expenses")

    # Copy data back from backup
    cursor.execute('''
        INSERT INTO expenses (date, category, amount, note)
        SELECT date, category, amount, note FROM expenses_backup
    ''')

    conn.commit()
    conn.close()
    print("Restore complete! Data copied from 'expenses_backup' to 'expenses'.")
    

if __name__ == "__main__":
    restore_from_backup()
