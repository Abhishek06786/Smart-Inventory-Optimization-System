import sqlite3
import pandas as pd
import random

DATABASE = "inventory.db"

# -----------------------------
# SQLite Connection
# -----------------------------
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    stock INTEGER NOT NULL,
    price REAL NOT NULL
)
""")

# Clear old data
cursor.execute("DELETE FROM products")

products = [
    "Laptop", "Mouse", "Keyboard", "Monitor", "Printer",
    "Rice", "Sugar", "Milk", "Oil", "Soap",
    "Shampoo", "Phone", "Headphones", "Bottle",
    "Notebook", "Pen", "Chair", "Table", "Bag", "Shoes"
]

categories = {
    "Laptop": "Electronics",
    "Mouse": "Electronics",
    "Keyboard": "Electronics",
    "Monitor": "Electronics",
    "Printer": "Electronics",
    "Phone": "Electronics",
    "Headphones": "Electronics",

    "Rice": "Grocery",
    "Sugar": "Grocery",
    "Milk": "Grocery",
    "Oil": "Grocery",

    "Soap": "Personal Care",
    "Shampoo": "Personal Care",

    "Bottle": "Accessories",

    "Notebook": "Stationery",
    "Pen": "Stationery",

    "Chair": "Furniture",
    "Table": "Furniture",

    "Bag": "Fashion",
    "Shoes": "Fashion"
}

data = []

for i in range(5000):

    product = random.choice(products)

    category = categories[product]

    price = random.randint(20, 50000)

    stock = random.randint(0, 300)

    daily_sales = random.randint(1, 30)

    lead_time = random.randint(1, 15)

    demand = daily_sales * lead_time + random.randint(-5, 5)

    if demand < 0:
        demand = 0

    # CSV Data
    data.append([
        product,
        category,
        price,
        stock,
        daily_sales,
        lead_time,
        demand
    ])

    # Database Insert
    cursor.execute("""
    INSERT INTO products
    (product_name, category, stock, price)
    VALUES (?, ?, ?, ?)
    """, (
        product,
        category,
        stock,
        price
    ))

# Save Database
conn.commit()
conn.close()

# Save CSV
df = pd.DataFrame(
    data,
    columns=[
        "product_name",
        "category",
        "price",
        "stock",
        "daily_sales",
        "lead_time",
        "demand"
    ]
)

df.to_csv("data/sales_data.csv", index=False)

print("====================================")
print("Dataset Created Successfully")
print("5000 Products Added To Database")
print("CSV Saved -> data/sales_data.csv")
print("====================================")
print(df.head())