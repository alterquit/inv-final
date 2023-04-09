import sqlite3

# Create a new SQLite database or connect to an existing one
conn = sqlite3.connect("inventory_management.db")
cursor = conn.cursor()

# Create the "product" table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_category TEXT NOT NULL,
    product_price REAL NOT NULL,
    stocks INTEGER NOT NULL
)
""")

# Create the "salestats" table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS salestats (
    transaction_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product (product_id)
)
""")

# Create the "user" table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    user_type TEXT NOT NULL
)
""")

# Commit the changes and close the connection
conn.commit()
conn.close()
