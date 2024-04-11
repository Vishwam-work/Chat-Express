import sqlite3
import random
import string



# Function to generate random order ID
def generate_order_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Function to generate random customer name
def generate_customer_name():
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah']
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown']
    return random.choice(first_names) + ' ' + random.choice(last_names)

# Function to generate random shipping date
def generate_shipping_date():
    year = random.randint(2022, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  
    return f'{year}-{month:02d}-{day:02d}'  


def generate_product_name():
    products = ['iPhone', 'Samsung Galaxy', 'Google Pixel', 'MacBook', 'Surface Pro']
    return random.choice(products)


conn = sqlite3.connect('data.db')



cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS orders
#              (order_id TEXT, customer_name TEXT, shipping_date DATE, product_name TEXT)''')


# for _ in range(10):
#     order_id = generate_order_id()
#     customer_name = generate_customer_name()
#     shipping_date = generate_shipping_date()
#     product_name = generate_product_name()
#     cursor.execute("INSERT INTO orders (order_id, customer_name, shipping_date, product_name) VALUES (?, ?, ?, ?)",
#                    (order_id, customer_name, shipping_date, product_name))
product_names = ["iPhone 13", "Samsung Galaxy S21", "Google Pixel 6", "MacBook Pro", "iPad Air", "Sony PlayStation 5", "Nintendo Switch", "Bose QuietComfort 45", "Dyson V11", "GoPro Hero 10"]
colors = ["Black", "White", "Silver", "Gold", "Space Gray", "Midnight Green", "Blue", "Red", "Pink", "Yellow"]
prices = [999.99, 899.99, 799.99, 1499.99, 599.99, 499.99, 299.99, 349.99, 599.99, 399.99]
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT,
                price REAL,
                color TEXT
            )''')

for _ in range(20):
    product_name = random.choice(product_names)
    price = random.choice(prices)
    color = random.choice(colors)
    cursor.execute("INSERT INTO products (product_name, price, color) VALUES (?, ?, ?)", (product_name, price, color))

# Step 4: Commit changes to the database
conn.commit()

# Step 5: Close the connection
conn.close()