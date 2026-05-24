# CREATING A PROJECT : english to sql , user tells what it wants and the ai gives the sql query in return 

# first we create a database 

import sqlite3
import random
from datetime import datetime, timedelta

# Create / overwrite the database
conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

# Drop existing tables (clean slate)
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS restaurants")

# === Create tables ===
cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    loyalty_tier TEXT,
    signup_date TEXT
)
""")

cursor.execute("""
CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    brand TEXT,
    city TEXT,
    rating REAL
)
""")

cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    restaurant_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
)
""")

# === Insert sample data ===

# Customers
customers = [
    (1, "Tanmay Saluja", "Delhi", "Gold", "2024-01-15"),
    (2, "Rohan Mehta", "Mumbai", "Silver", "2024-03-22"),
    (3, "Priya Sharma", "Bangalore", "Platinum", "2023-11-08"),
    (4, "Arjun Patel", "Delhi", "Gold", "2024-05-10"),
    (5, "Sneha Kapoor", "Mumbai", "Silver", "2024-07-19"),
    (6, "Vikram Singh", "Hyderabad", "Bronze", "2025-01-05"),
    (7, "Anjali Reddy", "Bangalore", "Gold", "2024-09-12"),
    (8, "Rahul Verma", "Pune", "Silver", "2025-02-14"),
    (9, "Kavya Nair", "Chennai", "Platinum", "2023-12-30"),
    (10, "Aditya Joshi", "Delhi", "Bronze", "2025-04-01"),
]
cursor.executemany(
    "INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customers
)

# Restaurants
restaurants = [
    (1, "KFC", "Delhi", 4.3),
    (2, "Pizza Hut", "Delhi", 4.1),
    (3, "Taco Bell", "Delhi", 4.4),
    (4, "KFC", "Mumbai", 4.2),
    (5, "Pizza Hut", "Mumbai", 4.0),
    (6, "KFC", "Bangalore", 4.5),
    (7, "Taco Bell", "Bangalore", 4.3),
    (8, "Pizza Hut", "Hyderabad", 4.1),
    (9, "KFC", "Chennai", 4.4),
    (10, "Pizza Hut", "Pune", 4.2),
]
cursor.executemany(
    "INSERT INTO restaurants VALUES (?, ?, ?, ?)", restaurants
)

# Orders (random — 50 orders)
random.seed(42)
base_date = datetime(2025, 1, 1)
orders = []
for i in range(1, 51):
    customer_id = random.randint(1, 10)
    restaurant_id = random.randint(1, 10)
    days_offset = random.randint(0, 120)
    order_date = (base_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
    total_amount = round(random.uniform(150, 1200), 2)
    orders.append((i, customer_id, restaurant_id, order_date, total_amount))

cursor.executemany(
    "INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders
)

conn.commit()
conn.close()

print("Database created successfully!")
print("Tables: customers (10 rows), restaurants (10 rows), orders (50 rows)")