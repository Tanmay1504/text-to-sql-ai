# CREATING A PROJECT : english to sql , user tells what it wants and the ai gives the sql query in return 

# first we create a database 

import sqlite3
import random
from datetime import datetime, timedelta

random.seed(42)

conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

# === Drop existing tables (clean slate, correct order due to FKs) ===
for table in ["customer_feedback", "order_items", "orders", "menu_items",
              "promotions", "employees", "restaurants", "customers"]:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# ========== CREATE TABLES ==========

cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT,
    loyalty_tier TEXT,
    signup_date TEXT,
    total_lifetime_spend REAL DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    brand TEXT,
    city TEXT,
    address TEXT,
    rating REAL,
    opened_date TEXT
)
""")

cursor.execute("""
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT,
    restaurant_id INTEGER,
    hire_date TEXT,
    monthly_salary REAL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
)
""")

cursor.execute("""
CREATE TABLE menu_items (
    item_id INTEGER PRIMARY KEY,
    brand TEXT,
    item_name TEXT,
    category TEXT,
    price REAL,
    is_vegetarian INTEGER
)
""")

cursor.execute("""
CREATE TABLE promotions (
    promo_id INTEGER PRIMARY KEY,
    promo_name TEXT,
    brand TEXT,
    discount_percent INTEGER,
    start_date TEXT,
    end_date TEXT
)
""")

cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    restaurant_id INTEGER,
    employee_id INTEGER,
    promo_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    payment_method TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (promo_id) REFERENCES promotions(promo_id)
)
""")

cursor.execute("""
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    item_price REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
)
""")

cursor.execute("""
CREATE TABLE customer_feedback (
    feedback_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    customer_id INTEGER,
    rating INTEGER,
    comment TEXT,
    feedback_date TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

# ========== INSERT DATA ==========

# --- Customers (50) ---
first_names = ["Tanmay", "Rohan", "Priya", "Arjun", "Sneha", "Vikram", "Anjali",
               "Rahul", "Kavya", "Aditya", "Ishita", "Karan", "Meera", "Nikhil",
               "Pooja", "Rajesh", "Shruti", "Varun", "Divya", "Akash", "Neha",
               "Suresh", "Tanya", "Ravi", "Aarti", "Manish", "Ritu", "Sahil",
               "Komal", "Deepak", "Sara", "Yash", "Megha", "Aman", "Riya",
               "Harsh", "Pia", "Ankit", "Nisha", "Gaurav", "Tara", "Vivek",
               "Anika", "Sameer", "Lavanya", "Rohit", "Aditi", "Karthik", "Disha", "Ishaan"]
last_names = ["Saluja", "Mehta", "Sharma", "Patel", "Kapoor", "Singh", "Reddy",
              "Verma", "Nair", "Joshi", "Gupta", "Kumar", "Iyer", "Chopra"]
cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune", "Chennai", "Kolkata", "Gurgaon", "Noida", "Jaipur"]
tiers = ["Platinum", "Gold", "Silver", "Bronze"]
tier_weights = [1, 2, 3, 4]

customers_data = []
for i in range(1, 51):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = name.lower().replace(" ", ".") + f"{i}@example.com"
    city = random.choice(cities)
    tier = random.choices(tiers, weights=tier_weights)[0]
    signup = (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 900))).strftime("%Y-%m-%d")
    customers_data.append((i, name, email, city, tier, signup, 0.0))

cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?)", customers_data)

# --- Restaurants (25) ---
brands = ["KFC", "Pizza Hut", "Taco Bell"]
streets = ["MG Road", "Park Street", "Brigade Road", "Linking Road", "FC Road",
           "Connaught Place", "Banjara Hills", "Anna Nagar", "Salt Lake", "Vaishali"]

restaurants_data = []
for i in range(1, 26):
    brand = random.choice(brands)
    city = random.choice(cities)
    address = f"{random.randint(1, 200)} {random.choice(streets)}, {city}"
    rating = round(random.uniform(3.8, 4.8), 1)
    opened = (datetime(2018, 1, 1) + timedelta(days=random.randint(0, 2000))).strftime("%Y-%m-%d")
    restaurants_data.append((i, brand, city, address, rating, opened))

cursor.executemany("INSERT INTO restaurants VALUES (?, ?, ?, ?, ?, ?)", restaurants_data)

# --- Employees (30) ---
roles = ["Manager", "Cashier", "Cook", "Delivery", "Cleaner"]
role_salaries = {"Manager": (45000, 70000), "Cashier": (18000, 25000),
                 "Cook": (22000, 35000), "Delivery": (16000, 22000),
                 "Cleaner": (12000, 18000)}

employees_data = []
for i in range(1, 31):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    role = random.choice(roles)
    rest_id = random.randint(1, 25)
    hire = (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))).strftime("%Y-%m-%d")
    salary = round(random.uniform(*role_salaries[role]), 2)
    employees_data.append((i, name, role, rest_id, hire, salary))

cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", employees_data)

# --- Menu items (40) ---
menu = [
    # KFC
    ("KFC", "Zinger Burger", "Burger", 199, 0),
    ("KFC", "Chicken Bucket (8 pc)", "Chicken", 699, 0),
    ("KFC", "Hot Wings (6 pc)", "Chicken", 249, 0),
    ("KFC", "Veg Zinger", "Burger", 179, 1),
    ("KFC", "Popcorn Chicken", "Chicken", 159, 0),
    ("KFC", "Krushers Chocolate", "Beverage", 129, 1),
    ("KFC", "Fries (Large)", "Sides", 99, 1),
    ("KFC", "Chicken Rice Bowl", "Rice", 229, 0),
    ("KFC", "Boneless Strips (5 pc)", "Chicken", 279, 0),
    ("KFC", "Coleslaw", "Sides", 79, 1),
    ("KFC", "Pepsi", "Beverage", 60, 1),
    ("KFC", "Soft Serve", "Dessert", 49, 1),
    # Pizza Hut
    ("Pizza Hut", "Pepperoni Pizza (Medium)", "Pizza", 499, 0),
    ("Pizza Hut", "Margherita Pizza (Medium)", "Pizza", 349, 1),
    ("Pizza Hut", "Veggie Supreme (Large)", "Pizza", 599, 1),
    ("Pizza Hut", "Chicken Tikka Pizza (Large)", "Pizza", 649, 0),
    ("Pizza Hut", "Garlic Bread", "Sides", 149, 1),
    ("Pizza Hut", "Cheesy Bites Pizza", "Pizza", 549, 1),
    ("Pizza Hut", "Pasta Alfredo", "Pasta", 279, 1),
    ("Pizza Hut", "Chicken Wings", "Sides", 299, 0),
    ("Pizza Hut", "Choco Lava Cake", "Dessert", 99, 1),
    ("Pizza Hut", "Pepsi (Large)", "Beverage", 80, 1),
    ("Pizza Hut", "BBQ Chicken Pizza", "Pizza", 619, 0),
    ("Pizza Hut", "Veg Pasta", "Pasta", 249, 1),
    # Taco Bell
    ("Taco Bell", "Crunchy Taco", "Taco", 99, 0),
    ("Taco Bell", "Veg Crunchy Taco", "Taco", 89, 1),
    ("Taco Bell", "Chicken Burrito", "Burrito", 199, 0),
    ("Taco Bell", "Veg Burrito", "Burrito", 179, 1),
    ("Taco Bell", "Quesadilla Chicken", "Quesadilla", 229, 0),
    ("Taco Bell", "Quesadilla Veg", "Quesadilla", 209, 1),
    ("Taco Bell", "Nachos Supreme", "Sides", 169, 1),
    ("Taco Bell", "Cheesy Fries", "Sides", 129, 1),
    ("Taco Bell", "Mexican Rice Bowl", "Rice", 219, 1),
    ("Taco Bell", "Churros", "Dessert", 99, 1),
    ("Taco Bell", "Mountain Dew", "Beverage", 70, 1),
    ("Taco Bell", "Crunchwrap Supreme", "Wrap", 249, 0),
    ("Taco Bell", "Doritos Locos Taco", "Taco", 119, 0),
    ("Taco Bell", "Cheesy Burrito", "Burrito", 189, 1),
    ("Taco Bell", "Cinnamon Twists", "Dessert", 79, 1),
    ("Taco Bell", "Iced Tea", "Beverage", 60, 1),
]
menu_items_data = [(i + 1,) + item for i, item in enumerate(menu)]
cursor.executemany("INSERT INTO menu_items VALUES (?, ?, ?, ?, ?, ?)", menu_items_data)

# --- Promotions (15) ---
promo_names = ["Summer Splash", "Monsoon Madness", "Bucket Bonanza", "Pizza Party",
               "Taco Tuesday", "Weekend Feast", "Diwali Special", "New Year Blast",
               "Family Combo", "Student Discount", "Lunch Hour Deal", "Late Night",
               "Buy 1 Get 1", "Loyalty Reward", "First Order"]
promotions_data = []
for i, pname in enumerate(promo_names, 1):
    brand = random.choice(brands + ["All"])
    discount = random.choice([10, 15, 20, 25, 30, 40, 50])
    start = (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 200))).strftime("%Y-%m-%d")
    end_date = (datetime.strptime(start, "%Y-%m-%d") + timedelta(days=random.randint(7, 60))).strftime("%Y-%m-%d")
    promotions_data.append((i, pname, brand, discount, start, end_date))

cursor.executemany("INSERT INTO promotions VALUES (?, ?, ?, ?, ?, ?)", promotions_data)

# --- Orders (500) ---
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Wallet"]
base_date = datetime(2025, 1, 1)
orders_data = []
order_items_data = []
customer_spend = {i: 0.0 for i in range(1, 51)}
order_item_counter = 1

for order_id in range(1, 501):
    cust_id = random.randint(1, 50)
    rest_id = random.randint(1, 25)
    rest_brand = restaurants_data[rest_id - 1][1]
    # employee must work at this restaurant — fallback to any if none
    emp_options = [e[0] for e in employees_data if e[3] == rest_id]
    emp_id = random.choice(emp_options) if emp_options else random.randint(1, 30)
    promo_id = random.choice([None, None, None, random.randint(1, 15)])  # 25% with promo
    order_date = (base_date + timedelta(days=random.randint(0, 140))).strftime("%Y-%m-%d")
    payment = random.choice(payment_methods)

    # Generate 1-5 order items per order, matching the brand
    brand_items = [m for m in menu_items_data if m[1] == rest_brand]
    num_items = random.randint(1, 5)
    total = 0
    for _ in range(num_items):
        item = random.choice(brand_items)
        qty = random.randint(1, 3)
        price = item[4]
        total += price * qty
        order_items_data.append((order_item_counter, order_id, item[0], qty, price))
        order_item_counter += 1

    # Apply promo discount if present
    if promo_id:
        discount = promotions_data[promo_id - 1][3]
        total = total * (1 - discount / 100)

    total = round(total, 2)
    customer_spend[cust_id] += total
    orders_data.append((order_id, cust_id, rest_id, emp_id, promo_id, order_date, total, payment))

cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)", orders_data)
cursor.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", order_items_data)

# Update customer lifetime spend
for cust_id, spend in customer_spend.items():
    cursor.execute("UPDATE customers SET total_lifetime_spend = ? WHERE customer_id = ?",
                   (round(spend, 2), cust_id))

# --- Customer feedback (150) ---
positive_comments = ["Amazing food!", "Loved it", "Best in town", "Fast delivery",
                     "Hot and fresh", "Will order again", "Excellent service",
                     "Tasty and worth it", "Great quality", "Perfect portion"]
negative_comments = ["Cold food", "Late delivery", "Wrong order", "Stale food",
                     "Rude staff", "Not worth the price", "Missing items"]
neutral_comments = ["Average", "Okay-ish", "Could be better", "Decent",
                    "Nothing special", "Met expectations"]

feedback_data = []
sampled_orders = random.sample(range(1, 501), 150)
for fb_id, ord_id in enumerate(sampled_orders, 1):
    cust_id = orders_data[ord_id - 1][1]
    rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 35, 30])[0]
    if rating >= 4:
        comment = random.choice(positive_comments)
    elif rating == 3:
        comment = random.choice(neutral_comments)
    else:
        comment = random.choice(negative_comments)
    fb_date = orders_data[ord_id - 1][5]
    feedback_data.append((fb_id, ord_id, cust_id, rating, comment, fb_date))

cursor.executemany("INSERT INTO customer_feedback VALUES (?, ?, ?, ?, ?, ?)", feedback_data)

conn.commit()
conn.close()

print("✅ Database created successfully!")
print(f"📊 customers: 50 rows")
print(f"📊 restaurants: 25 rows")
print(f"📊 employees: 30 rows")
print(f"📊 menu_items: 40 rows")
print(f"📊 promotions: 15 rows")
print(f"📊 orders: 500 rows")
print(f"📊 order_items: ~{len(order_items_data)} rows")
print(f"📊 customer_feedback: 150 rows")