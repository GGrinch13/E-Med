import requests
from bs4 import BeautifulSoup

gpc_urls = ['https://gpc.ge/ka/search/mother-and-baby?category=29',
            'https://gpc.ge/ka/search/medicaments?category=26',
            'https://gpc.ge/ka/search/baby-food?category=4',
            'https://gpc.ge/ka/search/body-care?category=10',
            'https://gpc.ge/ka/search/cosmetics?category=5',
            'https://gpc.ge/ka/search/hair-care?category=6',
            'https://gpc.ge/ka/search/oral-care?category=8',
            'https://gpc.ge/ka/search/care-products-for-women?category=11',
            'https://gpc.ge/ka/search/care-products-for-men?category=17',
            'https://gpc.ge/ka/search/ptient-care-items?category=12',
            'https://gpc.ge/ka/search/medical-devices?category=15',
            'https://gpc.ge/ka/search/food?category=14',
            'https://gpc.ge/ka/search/acessories?category=16',
            'https://gpc.ge/ka/search/gift-sets?category=7',
            'https://gpc.ge/ka/search/decorative-cosmetics-and-fragrances?category=30',
            'https://gpc.ge/ka/search/optic?category=63',
            'https://gpc.ge/ka/search/carters?category=25178',
            'https://gpc.ge/ka/search/sloggi?category=25180',
            'https://gpc.ge/ka/search/family-products?category=13',
            'https://gpc.ge/ka/search/baby-toys?category=5724'
    ,



]
drugs = []
for url in gpc_urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', class_='tile')

        for product in products:
            product_name = product.find('span', class_='tile__description').text.strip()
            product_price = product.find('div', class_='tile__price').text.strip()
            drugs.append((product_name, product_price))


    else:
        print("connection error")

