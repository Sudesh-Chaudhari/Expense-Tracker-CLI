import init_db
from init_db import get_connection

# ---- Function: Add Expense ----
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (e.g., Food, Transport, Maintenance, Furniture, Clothes, Medical, Bills, Others): ")

    # Validate amount input
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a positive numeric value.")

    note = input("Enter note (optional): ")

    # Safe DB connection
    conn, cursor = get_connection()
    cursor.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)", (date, category, amount, note))

    # To delete first 3 records for testing purposes
    # cursor.execute("DELETE FROM expenses WHERE id IN (SELECT id FROM expenses ORDER BY id LIMIT 3)")
    
    conn.commit()
    conn.close()
    print("Expense added successfully.")


# ---- Function: View Expenses ----
def view_expenses():
    conn, cursor = get_connection()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    headers = ["ID", "Date", "Category", "Amount", "Note"]

    # Convert rows to string (and handle None as "")
    str_rows = [[str(item) if item is not None else "NULL" for item in row] for row in rows]

    # Calculate max width per column
    col_widths = []
    for i, header in enumerate(headers):
        max_data_len = max((len(r[i]) for r in str_rows), default=0)
        col_widths.append(max(len(header), max_data_len))

    # Print header
    header_row = "  ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))

    # Print rows
    for row in str_rows:
        row_text = "  ".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(headers)))
        print(row_text)

    conn.close()

# ---- Function: Delete Expenses ----
def delete_expenses():
    ids = input("Enter IDs of expenses to delete (comma-separated): ")
    id_list = [int(id.strip()) for id in ids.split(",")]

    conn, cursor = get_connection()

    cursor.execute(f"DELETE FROM expenses WHERE id IN ({','.join(['?']*len(id_list))})", id_list)

    conn.commit()
    conn.close()

    print("Selected expenses deleted successfully.")

# ---- Function: Update Expenses ----
def update_expenses():
    id = int(input("Enter the ID of the expense to update: "))

    conn, cursor = get_connection()

    cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))
    row = cursor.fetchone()

    if row:
        print(f"Current details: Date: {row[1]}, Category: {row[2]}, Amount: {row[3]}, Note: {row[4]}")
        date = input(f"Enter new date (YYYY-MM-DD) or press Enter to keep '{row[1]}': ") or row[1]
        category = input(f"Enter new category or press Enter to keep '{row[2]}': ") or row[2]
        amount_input = input(f"Enter new amount or press Enter to keep '{row[3]}': ")
        amount = float(amount_input) if amount_input else row[3]
        note = input(f"Enter new note or press Enter to keep '{row[4]}': ") or row[4]

        cursor.execute("""UPDATE expenses SET date = ?, category = ?, amount = ?, note = ? WHERE id = ?""", (date, category, amount, note, id))

        conn.commit()
        print("Expense updated successfully.")
    else:
        print("Expense with the given ID not found.")

    conn.close()

def view_reports():
    conn, cursor = get_connection()

    while True:
        print("\n--- Reports & Summaries ---")
        print("1. Total Expenses")
        print("2. Category-wise Totals")
        print("3. Monthly Totals")
        print("4. Highest & Lowest Expense")
        print("5. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            cursor.execute("SELECT SUM(amount) FROM expenses")
            total = cursor.fetchone()[0]
            print(f"\nTotal Expenses: {total if total else 0}")

        elif choice == "2":
            cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
            rows = cursor.fetchall()
            print("\nCategory-wise Totals:")
            for row in rows:
                print(f"{row[0]}: {row[1]}")

        elif choice == "3":
            cursor.execute("SELECT strftime('%Y-%m', date) as month, SUM(amount) FROM expenses GROUP BY month ORDER BY month")
            rows = cursor.fetchall()
            print("\nMonthly Totals:")
            for row in rows:
                print(f"{row[0]}: {row[1]}")

        elif choice == "4":
            cursor.execute("SELECT * FROM expenses ORDER BY amount DESC LIMIT 1")
            highest = cursor.fetchone()
            cursor.execute("SELECT * FROM expenses ORDER BY amount ASC LIMIT 1")
            lowest = cursor.fetchone()
            print("\nHighest Expense:", highest)
            print("Lowest Expense:", lowest)

        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

    conn.close()

def forecast_expenses():
    conn, cursor = get_connection()
    
    # Last 30 days total
    cursor.execute("""
        SELECT SUM(amount), COUNT(DISTINCT date)
        FROM expenses
        WHERE date >= DATE('now', '-30 days')
    """)
    result = cursor.fetchone()
    total_spent, days_count = result if result else (0, 0)

    if days_count == 0:
        print("Not enough data to forecast.")
        conn.close()
        return

    daily_avg = total_spent / days_count
    weekly_avg = daily_avg * 7
    monthly_avg = daily_avg * 30

    print("\n--- Expense Forecast (Basic) ---")
    print(f"Average Daily Spend    : ₹{daily_avg:.2f}")
    print(f"Projected Weekly Spend : ₹{weekly_avg:.2f}")
    print(f"Projected Monthly Spend: ₹{monthly_avg:.2f}")

    # Optional: Show last 7 days for context
    cursor.execute("""
        SELECT date, SUM(amount) 
        FROM expenses 
        WHERE date >= DATE('now', '-7 days') 
        GROUP BY date
        ORDER BY date
    """)
    last_week = cursor.fetchall()
    if last_week:
        print("\nLast 7 Days Spend:")
        for row in last_week:
            print(f"{row[0]}: ₹{row[1]}")
    conn.close()


def main():

    print("\n----------- Welcome to the Expense Tracker! -----------")
    
    try:
        while True:
            print("\n----- Expense Tracker Menu -----")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Delete Expenses")
            print("4. Update Expenses")
            print("5. Reports & Summaries")
            print("6. Forecast Expenses")
            print("7. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                add_expense()
            elif choice == "2":
                view_expenses()
            elif choice == "3":
                delete_expenses()
            elif choice == "4":
                update_expenses()
            elif choice == "5":
                view_reports()
            elif choice == "6":
                forecast_expenses()
            elif choice == "7":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    init_db.initialize_database()
    print("Application started after database initialization.\n")
    main()