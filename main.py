from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv
from fastapi.responses import FileResponse
load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "hello"}
def get_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))
@app.get("/products")
def get_products(category: str = None,cursor:str=None,limit:int=20):
    conditions = []
    params = []
    if category != None:
        conditions.append("category = %s")
        params.append(category)
    if cursor != None:
        s = cursor.split("_")
        last_created_at = s[0]
        last_id = int(s[1])
        conditions.append("(created_at, id) < (%s, %s)")
        params.append(last_created_at)
        params.append(last_id)
    if conditions: 
        where_clause = "WHERE " + " AND ".join(conditions)
       
    else:
        where_clause = ""
    query = f"SELECT id, name, category, price, created_at, updated_at FROM products {where_clause} ORDER BY created_at DESC, id DESC LIMIT %s"
    params.append(limit)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.close()
    products_list=[]
    for row in  results:
        product={ }
        product['id']=row[0]
        product['name']=row[1]
        product['category']=row[2]
        product['price']=row[3]
        product['created_at'] = row[4].isoformat()
        product['updated_at'] = row[5].isoformat() if row[5] else None
        products_list.append(product)
    if len(products_list) < limit:
        next_cursor = None
    else:
        last_product = products_list[-1]
        next_cursor = f"{last_product['created_at']}_{last_product['id']}"  
    return {"products": products_list, "next_cursor": next_cursor}
@app.get("/ui")
def serve_ui():
    return FileResponse("index.html")

