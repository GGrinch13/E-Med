from bs4 import BeautifulSoup
import requests
import sqlite3
import time

# meds list
drugs = []

def scrape_psp():

    # # Connecting to DB
    # conn = sqlite3.connect('psp_products.db')
    # cursor = conn.cursor()
    # # Create a table if it doesn't exist
    # cursor.execute('''
    #
    #     CREATE TABLE IF NOT EXISTS products (
    #
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #
    #         title TEXT UNIQUE,
    #
    #         price TEXT
    #
    #     )
    #
    # ''')
    link = 'https://psp.ge/მედიკამენტები.html?page=1'
    response = requests.get(link)
    if response.status_code == 200:
        print("status code 200")
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        products = soup.find_all('div', class_='product')
        for product in products:
            print(product.text.strip())


scrape_psp()
