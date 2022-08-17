#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import fake_useragent

URL = 'https://www.chess.com/ratings?page=1'

FAKE_USER = fake_useragent.FakeUserAgent().random
HEADERS = {'Accept': '',
           'User-Agent': FAKE_USER}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r
    else:
        print("Ошибка в запросе к странице \n{}".format(url))


def get_page_count(r):
    # request = get_html(url)
    soup = BeautifulSoup(r.text, 'lxml')
    link_temp = 'https://www.chess.com/ratings?page={}'
    list_page_link =[]

    pagination = soup.find('div', 'section-content-component')\
        .find('div', 'index-pagination').find('nav')\
        .find_all('a', 'form-button-component pagination-button-component')
    pagination = [s.text.strip() for s in pagination]

    for i in range(1, int(pagination[-1]) + 1):
        list_page_link.append(link_temp.format(i))

    return list_page_link


def get_info(url):
    r = get_html(url)

    soup = BeautifulSoup(r.text, 'lxml')
    last_update = soup.find('div', 'section-content-component').find('p').text.strip()
    trs = soup.find('table', 'table-component').find_all('tr')

    list_chess_rating_all = []
    for tr in trs[1:]:
        tds = tr.find_all('td')

        list_chess_rating_all.clear()
        for td in tds:
            text = td.text.strip()
            list_chess_rating_all.append(text)
        list_chess_rating_all[1] = list_chess_rating_all[1].replace('\n', '').split()
        print(list_chess_rating_all)
        # break

    return list_chess_rating_all


if __name__ == '__main__':
    list_page_link = get_page_count(get_html(URL))

    for link in list_page_link:
        get_info(link)

        # break
