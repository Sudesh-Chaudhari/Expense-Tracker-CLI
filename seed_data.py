import sqlite3

def seed_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Insert multiple rows at once
    expenses = [
        ("2025-09-21", "Transport", 1250, "Travelling expenses for medical emergency"),
        ("2025-09-20", "Food", 258, "Buy some fruits from the market"),
        ("2025-09-20", "Food", 500, "Cold drinks"),
        ("2025-09-27", "Other", 1208, "Mobile cover, Charger and screenguard"),
        ("2025-09-27", "Maintainance", 800, "Bike servicing charges"),
        ("2025-09-26", "Cloths", 550, "T-shirts and jeans"),
        ("2025-09-28", "Furniture", 5300, ""),
        ("2025-09-28", "Food", 10, "Chocolates"),
        ("2025-09-30", "Bills", 3000, "Electricity Bill"),
        ("2025-09-30", "Bills", 4500, "Gas Bill"),
        ("2025-09-30", "Maintainance", 3000, "Room Maintainance"),
        ("2025-10-01", "Cloths", 2380, "Jeans and Kurta's"),
        ("2025-09-30", "Furniture", 5000, "Home Decoration furniture"),
        ("2025-09-14", "Others", 4380, ""),
        ("2025-09-21", "Transport", 450, "Family function"),
        ("2025-09-12", "Medical", 1200, "Medicines"),
        ("2025-09-09", "Medical", 3500, "Liquids"),
        ("2025-09-10", "Medical", 610, "Normal Medicines"),
        ("2025-09-14", "Cloths", 1280, "Jeans"),
        ("2025-09-16", "Food", 4510, "Family Dinner"),
    ]

    cursor.executemany(
        "INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)", 
        expenses
    )

    conn.commit()
    conn.close()
    print("Seed data inserted successfully!")

if __name__ == "__main__":
    seed_database()
