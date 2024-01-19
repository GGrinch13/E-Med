import requests
from bs4 import BeautifulSoup
import time
import sqlite3

# meds list

drugs = []

def scrape_gpc():

    # iterate through categories to search on all page in each category
        for page in range(1, 254):
            # various categories
            links = [f'https://gpc.ge/ka/category/medicaments?category=26&page={page}',
                     f'https://gpc.ge/ka/category/mother-and-baby?category=29&page={page}',
                     f'https://gpc.ge/ka/category/baby-food?category=4&page={page}',
                     f'https://gpc.ge/ka/category/body-care?category=10&page={page}',
                     f'https://gpc.ge/ka/category/cosmetics?category=5&page={page}',
                     f'https://gpc.ge/ka/category/hair-care?category=6&page={page}',
                     f'https://gpc.ge/ka/category/oral-care?category=8&page={page}',
                     f'https://gpc.ge/ka/category/care-products-for-women?category=11&page={page}',
                     f'https://gpc.ge/ka/category/care-products-for-men?category=17&page={page}',
                     f'https://gpc.ge/ka/category/ptient-care-items?category=12&page={page}',
                     f'https://gpc.ge/ka/category/food?category=14&page={page}',
                     f'https://gpc.ge/ka/category/acessories?category=16&page={page}',
                     f'https://gpc.ge/ka/category/gift-sets?category=7&page={page}',
                     f'https://gpc.ge/ka/category/decorative-cosmetics-and-fragrances?category=30&page={page}',
                     f'https://gpc.ge/ka/category/optic?category=63&page={page}',
                     f'https://gpc.ge/ka/category/carters?category=25178&page={page}',
                     f'https://gpc.ge/ka/category/sloggi?category=25180&page={page}',
                     f'https://gpc.ge/ka/category/family-products?category=13&page={page}',
                     f'https://gpc.ge/ka/category/baby-toys?category=5724&page={page}']

            for link in links:
                print("time.sleep.5")
                time.sleep(5)
                response = requests.get(link)
                if response.status_code == 200:
                    print("status code 200")
                    soup = BeautifulSoup(response.content, 'html.parser')
                    products = soup.find_all('a')
                    for product in products:
                        print("searching products..")
                        try:
                            meds_name = product.find('div',
                                                     attrs={'text-md font-medium text-blackLight mb-12 laptop:mb-16 h-38 '
    
                                                            'leading-18 line-clamp-2'}).text.strip()

                            meds_price = product.find('div', attrs={'flex items-center'}).text.strip()
                            if meds_name not in drugs:
                                print("adding into db")
                                drugs.append((meds_name, meds_price))
                                # Extract and save into DB
                                conn = sqlite3.connect('gpc_products_1.db')
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
                        except:
                            pass
                else:
                    print("connection error")
        return
scrape_gpc()
