from bs4 import BeautifulSoup
import requests
import sqlite3
import time

# meds list
drugs = []


def scrape_pharmadepot():

    # Connecting to DB
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
    # iterate through categories to search on all page in each category
    for page in range(1, 256):
        # various categories
        links = [f'https://www.pharmadepot.ge/ka/search/medication?category=111843&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/baby-toys?category=111857&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/baby-food?category=111841&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/mother-and-baby?category=111840&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/cosmetics?category=111842&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/decorative-cosmetics-and-fragrances?category=111851&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/hair-care?category=111839&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/oral-care?category=111849&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/gift-sets?category=111853&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/body-care?category=111846&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/care-products-for-women?category=111848&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/ptient-care-items?category=111844&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/medical-devices?category=111845&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/family-products?category=111850&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/care-products-for-men?category=111852&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/food?category=111847&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/optic?category=111855&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/carters?category=111858&page={page}',
                 f'https://www.pharmadepot.ge/ka/search/accessories?category=239983&page={page}']
        for link in links:
            # sleeping code to not overload webpage
            print("sleeping for 4 seconds..")
            time.sleep(4)
            response = requests.get(link)
            # check if request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Find Meds
                products = soup.find_all('a')
                # Iterate through meds
                for product in products:
                    print("Searching products..")
                    # Find product name and add into list
                    try:
                        meds_name = product.find('div', attrs={'text-md font-medium text-blackLight mb-12 laptop:mb-16 h-38 '
                                                               'leading-18 line-clamp-2'}).text.strip()
                    # Find product price and add into list
                        meds_price = product.find('div', attrs={'flex items-center'}).text.strip()
                        if meds_name not in drugs:
                            print("adding into DB")
                            drugs.append((meds_name, meds_price))
                        # Insert product information into the database
                        for med in drugs:
                            cursor.execute('INSERT OR IGNORE INTO products (title, price) VALUES (?, ?)', med)
                        conn.commit()
                    except:
                        pass
            else:
                print('Connection error')
    conn.commit()
    conn.close()


scrape_pharmadepot()



