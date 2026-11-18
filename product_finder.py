import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# Create a products table
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        rating REAL,
        in_stock INTEGER DEFAULT 1
    )
""")

# Insert sample data — a small electronics store
products = [
    ("Wireless Mouse", "Accessories", 29.99, 4.5, 1),
    ("Mechanical Keyboard", "Accessories", 89.99, 4.8, 1),
    ("USB-C Hub", "Accessories", 34.99, 4.2, 0),
    ("27-inch Monitor", "Displays", 299.99, 4.6, 1),
    ("24-inch Monitor", "Displays", 179.99, 4.3, 1),
    ("Webcam HD", "Accessories", 49.99, 3.9, 1),
    ("Noise-Canceling Headphones", "Audio", 199.99, 4.7, 1),
    ("Bluetooth Speaker", "Audio", 59.99, 4.1, 0),
    ("Laptop Stand", "Accessories", 39.99, 4.4, 1),
    ("External SSD 1TB", "Storage", 89.99, 4.6, 1),
    ("External SSD 2TB", "Storage", 149.99, 4.5, 1),
    ("Flash Drive 64GB", "Storage", 12.99, 4.0, 1),
]

cursor.executemany("""
    INSERT INTO products (name, category, price, rating, in_stock) 
    VALUES (?, ?, ?, ?, ?)
""", products)
connection.commit()

print("=== Out Of Stock ===")
cursor.execute("SELECT name, category FROM products WHERE in_stock = 0")
for row in cursor.fetchall():
    print(f"  {row[1]}: {row[0]}")


print("\n=== High-Rated Products Under $100 ===")

cursor.execute("""
    SELECT name, rating, price
    FROM products
    WHERE rating >= 4.5
      AND price < 100
""")

for row in cursor.fetchall():
    print(f"{row[0]} | Rating: {row[1]} | Price: ${row[2]:.2f}")

print("\n=== Top 3 Most Expensive Accessories ===")

cursor.execute("""
    SELECT name, price
    FROM products
    WHERE category = 'Accessories'
    ORDER BY price DESC
    LIMIT 3
""")

for row in cursor.fetchall():
    print(f"{row[0]} - ${row[1]:.2f}")


print("\n=== Products With Monitor in the Name ===")
cursor.execute("SELECT * FROM products WHERE name LIKE '%Monitor%'")
for row in cursor.fetchall():
    print(row)


print("\n=== In-Stock Products Not in Accessories ===")

cursor.execute("""
    SELECT name, category, price
    FROM products
    WHERE category <> 'Accessories'
      AND in_stock = 1
    ORDER BY category, price
""")

for name, category, price in cursor.fetchall():
    print(f"{category}: {name} - ${price:.2f}")

connection.close()
