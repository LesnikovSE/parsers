import requests
from bs4 import BeautifulSoup
import time

HOST = 'https://www.ebay.com/'
URL = 'https://www.ebay.com/n/all-categories'
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
}

list_main_menu = []


def crawler_link_menu():
    r = requests.get(HOST)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')

        # Парсинг ссылок главного меню

        li_s = soup.find('div', 'hl-cat-nav').find_all('li', 'hl-cat-nav__js-tab')
        flag = 1
        for li in li_s:
            list_main_menu.append({
                flag: [li.find('a').text, li.find('a').get('href')]
            })

            flag += 1
            time.sleep(0.5)

    return list_main_menu


if __name__ == '__main__':
    crawler_link_menu()
