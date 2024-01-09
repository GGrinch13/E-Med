import requests
from bs4 import BeautifulSoup

gpc_url = 'https://mygpc.ge/ka/search/medicaments?category=26'
response = requests.get(gpc_url)
if response.status_code == 200:
    print("yes")
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('a')
    drugs = []
    for product in products:
        print(product.find('div'))

        try:
            meds_name = product.find('div', attrs={' text-md font-medium text-blackLight mb-12 laptop:mb-16 h-38 leading-18 line-clamp-2'}).text.strip()
            print(meds_name)
        except:
            print("eeeee")
            pass

else:
    print("connection error")