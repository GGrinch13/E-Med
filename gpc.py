import requests
from bs4 import BeautifulSoup


# meds list
drugs = []
# various categories
# categories = [29, 26, 4, 10, 5, 6, 8, 11, 17, 12, 15, 14, 16, 7, 30, 63, 25178, 25180, 13, 5724]
categories = [29]
# iterate through categories to search on all page in each category
for category in categories:
    for page in range(1, 3):
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
                    meds_price = product.find('div', attrs={'flex text-md laptop:text-3md font-semibold text-black'}).text.strip()
                    print(meds_name, meds_price)
                except:
                    pass

# for url in gpc_urls:
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         products = soup.find_all('div', attrs={'text-md font-medium text-blackLight mb-12 laptop:mb-16 h-38 leading-18 line-clamp-2'})
#         print(products)
#
#         # for product in products:
#         #     product_name = product.find('span', class_='tile__description').text.strip()
#         #     product_price = product.find('div', class_='tile__price').text.strip()
#         #     drugs.append((product_name, product_price))
#
#
#     else:
#         print("connection error")

