import requests
from bs4 import BeautifulSoup
import time
import sqlite3

# meds list

drugs = []
# various categories
categories = [29, 26, 4, 10, 5, 6, 8, 11, 17, 12, 15, 14, 16, 7, 30, 63, 25178, 25180, 13, 5724]
# iterate through categories to search on all page in each category
for category in categories:
    for page in range(1, 254):
        url = f'https://gpc.ge/ka/search/?category={category}&{page}'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('a')
            for product in products:
                try:
                    meds_name = product.find('div',
                                             attrs={'text-md font-medium text-blackLight mb-12 laptop:mb-16 h-38 '
                                                    'leading-18 line-clamp-2'}).text.strip()
                    meds_price = product.find('div', attrs={'flex items-center'}).text.strip()
                    drugs.append((meds_name, meds_price))
                except:
                    pass
            # Extract and save into DB
            conn = sqlite3.connect('gpc_products.db')
            cursor = conn.cursor()

            # Create a table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE,
                    price TEXT
                )
            ''')
            # Insert product information into the database
            for med in drugs:
                cursor.execute('INSERT OR IGNORE INTO products (title, price) VALUES (?, ?)', med)
            # Commit changes and close the connection
            conn.commit()
            conn.close()
            time.sleep(0.8)
    else:
        print("connection error")

