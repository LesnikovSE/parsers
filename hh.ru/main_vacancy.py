#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import fake_useragent


HOST = 'https://hh.ru/'
URL = 'https://hh.ru/search/resume'
FAKE_USER = fake_useragent.FakeUserAgent().random
HEADERS = {
    'Accept': 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': FAKE_USER
}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r
    else:
        print("Error")


# def get_vacancy_list(url):
#     r = get_html(url)

def get_filter_menu(url):
    r = get_html(URL)
    soup = BeautifulSoup(r.text, 'lxml')
    list_filter_menu = []

    # Регион
    blocks = soup.find_all('div', 'row-content')
    blocks = blocks[1].find('div', 'novafilters').find_all('div', 'novafilters-group-wrapper')
    # Blocks...
    # условия поиска = 0
    # регион = 1
    # профоблать = 2
    # уровень дохода = 3
    # опыт работы = 4
    # пол = 5
    # возраст = 6
    # ключевые навыки = 7
    # исключения = 8
    # тип занятости = 9
    # график работы = 10
    # Гражданство, Знание языков, Разрешение на работу, Категория прав = 11
    # сбросить все фильтры = 12
    list_filter_menu.append(
        [blocks[1].find('div', {'data-qa': 'serp__novafilter-group-title'}).text.strip(),
         [i.text for i in blocks[1].find('ul', 'novafilters-list').find_all('li')]]
    )

    return list_filter_menu

if __name__ == '__main__':
    # list_vacancy = get_vacancy_list(URL_RESUME)
    # print(list_vacancy)
    list_filter_menu = get_filter_menu(URL)
    print(list_filter_menu)

