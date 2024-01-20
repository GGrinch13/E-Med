import time
from bs4 import BeautifulSoup
import requests
import sqlite3

# meds list
drugs = []


def scrape_aversi():

    # Connecting to DB
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
    # Make loop for iterate on all pages
    for category in range(1, 234):
        for page in range(1, 26):
            # URLs of websites
            Aversi_url = f'https://www.aversi.ge/ka/medikamentebi/{category}?page={page}'
            # sleeping code to not overload webpage
            print("sleeping for 4 seconds..")
            time.sleep(4)
            response = requests.get(Aversi_url)
            # check if request was successful
            if response.status_code == 200:
                print("status code 200")
                soup = BeautifulSoup(response.text, 'html.parser')

                # find Meds
                products = soup.find_all('div', class_='product')
                # Add into list

                for product in products:
                    print("searching products..")
                    med_name = product.find('h5', class_='product-title').text.strip()
                    med_price = product.find('span', class_='amount text-theme-colored').text.strip()
                    if med_name not in drugs:
                        print("Adding into DB")
                        drugs.append((med_name, med_price))

                    # Insert product information into the database
                    for med in drugs:
                        cursor.execute('INSERT OR IGNORE INTO products (title, price) VALUES (?, ?)', med)
                    # Commit changes
                    conn.commit()
            else:
                print('Connection error')
    # save db and close it
    conn.commit()
    conn.close()


scrape_aversi()
