import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    # Connect to DB
    conn = sqlite3.connect("gpc_products_1.db")
    cursor = conn.cursor()
    gpc_products = cursor.execute("SELECT title, price FROM products").fetchall()
    conn.close()
    conn = sqlite3.connect("aversi_products.db")
    cursor = conn.cursor()
    aversi_products = cursor.execute("SELECT title, price FROM products").fetchall()
    conn.close()
    conn = sqlite3.connect("pharmadepot_products.db")
    cursor = conn.cursor()
    pharmadepot_products = cursor.execute("SELECT title, price FROM products").fetchall()
    conn.close()
    # Give products from DB to Web
    return render_template('index.html', gpc_products=gpc_products, aversi_products=aversi_products, pharmadepot_products=pharmadepot_products), 200

if __name__ == '__main__':
    app.run(debug=True)



#  დასამატებელია lazy loadin რაც ეკრანზეა მარტო ის რო ჩატვირთოს
# ან დასამატებელია გვერდები, 1,2,3.. და ასე

