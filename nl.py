import requests
from bs4 import BeautifulSoup as BS
from time import sleep
import os

HOST = 'https://scrapingclub.com'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

if not os.path.exists('images'):
    os.mkdir('images')
else:
    pass

def download(url):
    resp = requests.get(url, stream=True)
    r = open(r'images/' + url.split('/')[-1], 'wb')
    for value in resp.iter_content(1024*1024):
        r.write(value)
    r.close()

PAGINATION = input("How many pages You want me to pars?: ")
PAGINATION = int(PAGINATION.strip())

def get_url():

    for count in range(1, PAGINATION+1):
        print(f'Parsing of page № {count}')
        url = f'https://scrapingclub.com/exercise/list_basic/?page={count}'
        response = requests.get(url, headers=HEADERS)
        soup = BS(response.text, 'lxml') # html.parser
        data = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')

        for i in data:
            card_link = HOST + i.find('a').get('href')
            yield card_link


def array():
    sleeping_time = input('Enter pause between pages in seconds: ')
    sleeping_time = int(sleeping_time.strip())
    for link in get_url():

        respone = requests.get(link, headers=HEADERS)

        # Slowing down the process to hide that it is not a human
        sleep(sleeping_time)

        soup = BS(respone.text, 'lxml')
        data = soup.find('div', class_='card mt-4 my-4')

        name = data.find('h3', class_='card-title').text
        price = data.find('h4').text
        about = data.find('p', class_='card-text').text
        img = HOST + data.find('img', class_='card-img-top img-fluid').get('src')
        download(img)
        yield name, price, about, img
