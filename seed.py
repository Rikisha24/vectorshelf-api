import random
from datetime import datetime, timedelta
import psycopg2
import io
import csv
category_names = {
    "Electronics": ["Wireless Mouse", "Bluetooth Headphones", "Smart Watch", "Smart Bulb", "Wireless Charger"],
    "Clothing": ["Classic Jacket", "Cotton T-Shirt", "Denim Jeans", "Casual Shoes"],
    "Books": ["Mystery Novel", "Cookbook", "Science Fiction Novel", "Biography"],
    "Toys": ["Building Blocks", "Remote Control Car", "Puzzle Set", "Action Figure"],
    "Home": ["Ceramic Mug", "Stainless Water Bottle", "LED Lamp", "Throw Pillow"],
    "Sports": ["Running Shoes", "Yoga Mat", "Sports Shoes", "Water Bottle"],
    "Beauty": ["Face Cream", "Lipstick", "Shampoo", "Perfume"],
    "Groceries": ["Organic Honey", "Green Tea", "Olive Oil", "Pasta Pack"]
}
price_ranges = {
    "Electronics": (500, 50000),
    "Clothing": (300, 5000),
    "Books": (100, 1500),
    "Toys": (200, 3000),
    "Home": (150, 4000),
    "Sports": (300, 8000),
    "Beauty": (50, 2000),
    "Groceries": (20, 1000)
}

categories = list(category_names.keys())
rows=[]
for i in range(200000):
   category=random.choice(categories)
   name=random.choice(category_names[category])
   min_price,max_price=price_ranges[category]
   row={
   'name':name,
   'category':category,
   'price':round(random.uniform(min_price,max_price),2),
   'created_at':datetime.now() - timedelta(days=random.randint(0, 365)),
   'updated_at':None
   }
   row['updated_at']=row['created_at']
   rows.append(row)
buffer = io.StringIO()
writer = csv.writer(buffer)

for row in rows:
    writer.writerow([row['name'], row['category'], row['price'], row['created_at'], row['updated_at']])

buffer.seek(0)

conn = psycopg2.connect("postgresql://neondb_owner:npg_YnsWlO5gj8Za@ep-lively-fire-atdtt695.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require")
cur=conn.cursor()
cur.copy_expert(
    "COPY products (name, category, price, created_at, updated_at) FROM STDIN WITH CSV",
    buffer
)
conn.commit()
cur.close()
conn.close()



         
    