import time
from bs4 import BeautifulSoup
import requests
import sqlite3


# Make loop for iterate on all pages
for category in range(1, 234):
    for page in range(1, 26):
        # URLs of websites
        Aversi_url = f'https://www.aversi.ge/ka/medikamentebi/{category}?page={page}'

        response = requests.get(Aversi_url)

        # check if request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # find Meds
            products = soup.find_all('div', class_='product')
            # Add into list
            drugs = []
            for product in products:
                med_name = product.find('h5', class_='product-title').text.strip()
                med_price = product.find('span', class_='amount text-theme-colored').text.strip()
                drugs.append((med_name, med_price))

            # Extract and save into DB
            conn = sqlite3.connect('aversi_products.db')
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
            time.sleep(1)
        else:
            print('An error has occurred.')
