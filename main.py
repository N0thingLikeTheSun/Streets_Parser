import requests
from bs4 import BeautifulSoup
import csv


HOST = 'https://postindex.pp.ua/'
URL = 'https://postindex.pp.ua/uk/district/YourDistrict/index.html'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}
FILE_NAME = 'YourDistrict.csv'


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params).text
    return r


streets = set()
html = get_html(URL)
soup = BeautifulSoup(html, 'html.parser')
items = soup.find_all('a', class_=False)
href = []
for item in items:
    if item.get('href').startswith('https://postindex.pp.ua/uk/district/YourDistrict/') \
            and not item.get('href').endswith('misto.html') \
            and not item.get('href').endswith('misto/YourDistrict.html') \
            and not item.get('href').endswith('index.html'):
        href.append(item.get('href'))
print('finish step 1')
href_2 = []
for item_2 in href:
    html_2 = get_html(item_2)
    soup_2 = BeautifulSoup(html_2, 'html.parser')
    items_2 = soup_2.find_all('a', class_=False)
    for item_3 in items_2:
        if item_3.get('href').startswith('https://postindex.pp.ua/uk/street/YourDistrict/') \
                and not item_3.get('href').endswith('misto.html') \
                and not item_3.get('href').endswith('misto/YourDistrict.html') \
                and not item_3.get('href').endswith('index.html'):
            href_2.append(item_3.get('href'))
print('finish step 2')
with open(FILE_NAME, 'w', newline='', encoding='utf-16') as file:
    writer = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item_4 in href_2:
        html_3 = get_html(item_4)
        soup_3 = BeautifulSoup(html_3, 'html.parser')
        items_3 = soup_3.find_all('td', class_=False)
        items_4 = soup_3.find_all('h2', class_=False)
        for item_5 in items_3:
            for item_6 in items_4:
                if item_6.get_text().startswith('Вулиці'):
                    item_7 = item_6.get_text().split(' ')
                    item_8 = ''
                    item_8 = ' '.join(item_7[1:])
                    if '(' in item_8:
                        item_9 = item_8.split('(')
                        item_10 = ' '.join(item_9[:-1])
                    else:
                        item_10 = item_8
                    if item_5.get_text().startswith('вулиця') or item_5.get_text().startswith(
                            'провулок') or item_5.get_text().startswith('проспект') or item_5.get_text().startswith(
                        'тупік') or item_5.get_text().startswith('проїзд') or item_5.get_text().startswith(
                        'бульвар') or item_5.get_text().startswith('в’їзд') or item_5.get_text().startswith(
                        'алея') or item_5.get_text().startswith('спуск') or item_5.get_text().startswith(
                        'проїзд') or item_5.get_text().startswith('площа') or item_5.get_text().startswith(
                        'жилий масив') or item_5.get_text().startswith('мікрорайон') or item_5.get_text().startswith(
                        'майдан') or item_5.get_text().startswith('шосе') or item_5.get_text().startswith('бульвар')  \
                            and not item_5.get_text().endswith('без назви'):
                        writer.writerow([item_5.get_text(), item_10])
print('finish step 3')

