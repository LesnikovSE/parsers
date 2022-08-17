import requests
import csv
import time
from bs4 import BeautifulSoup

FILE = 'cars.csv'
HOST = 'https://auto.ria.com/newauto/'
URL = 'https://auto.ria.com/newauto/marka-lexus/'
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/88.0.4324.182 Safari/537.36",
    "accept": "*/*"
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html.text, 'lxml')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html.text, 'lxml')
    posts = soup.find_all('div', class_='proposition')

    cars = []

    for post in posts:

        inf = post.find('div', class_='proposition_information').find_all(class_='size13')
        lst_inf = [i.text for i in inf]

        cars.append({
            "marka": post.find('div', class_='proposition_title').find('h3').text,
            "model": post.find('div', class_='proposition_equip').get_text(),
            "fuel": lst_inf[0],
            "korobka": lst_inf[1],
            "privod": lst_inf[2],
            "link": HOST + post.find('a').get('href')
            })

        time.sleep(0.5)

    return cars


def write_csv(items, path):
    with open(path, "w", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Модель', 'Топливо', 'Коробка передач', 'Привод', 'Ссылка'])
        for item in items:
            writer.writerow([item['marka'], item['model'], item['fuel'], item['korobka'], item['privod'], item['link']])


def parse():
    html = get_html(URL)

    if html.status_code == 200:
        cars = []

        pages_count = get_pages_count(html)
        for page in range(1, pages_count + 1):
            print(f"page {page} processing ...")

            html = get_html(URL, params={'page': page})
            html.encoding = 'utf-8'
            cars.extend(get_content(html))
            print("Ok")

        write_csv(cars, FILE)

        print(f"Add {len(cars)} auto")
    else:
        print("Error")


if __name__ == '__main__':
    parse()
