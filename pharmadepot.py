from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import sqlite3
import time

# Make loop for iterate on all pages
retries = 7
drugs = []

for attempt in range(retries):
        for page in range(1, 256):
            # URLs of websites
            Pharmadepot_url = f'https://www.pharmadepot.ge/ka/search/medication?category=111843&page={page}'
            response = requests.get(Pharmadepot_url, stream=True)

            # check if request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find Meds
                products = soup.find_all('a')

                # Find products
                for product in products:
                    # Find product name and add into list
                    try:
                        meds_name = product.find('div', attrs={'text-md font-medium text-blackLight mb-12 laptop:mb-16 h-38 '
                                                               'leading-18 line-clamp-2'}).text.strip()
                    # Find product price and add into list
                        meds_price = product.find('div', attrs={'flex items-center'}).text.strip()
                        drugs.append((meds_name, meds_price))
                    except:
                        pass
                # Extract and save into DB
                conn = sqlite3.connect('pharmadepot_products.db')
                cursor = conn.cursor()

                # Create a table if it doesn't exist
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT UNIQUE,
                        price TEXT
                    )
                ''')
                print(drugs)

                # Insert product information into the database
                for med in drugs:
                    cursor.execute('INSERT OR IGNORE INTO products (title, price) VALUES (?, ?)', med)

                # Commit changes and close the connection
                conn.commit()
                conn.close()
                time.sleep(2)
            else:
                print('An error has occurred.')


