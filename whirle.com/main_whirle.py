#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import fake_useragent
import time

FILE_PATH = ''
HOST = 'https://whirli.com/toys'
URL = 'https://whirli.com/toys/all?clearFilters=all'

fake_user = fake_useragent.UserAgent().random
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
              "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-agent": fake_user
}


def get_list_page_link_content(url):
    r = requests.get(url, headers=HEADERS)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        list_link_productions = []

        blocks = soup.find('div', 'v-layout--left').find_all('div', 'v-product-card')
        for i, block in enumerate(blocks):
            link = block.find('a', 'v-product-card__body').get('href')
            link = link[4:]
            name = block.find('a', 'v-product-card__body').find('p').text.strip()
            # tokens = block.find('a', 'v-product-card__body').find('span').find('p').text.strip()

            list_link_productions.append([i, name, link])
            # print(HOST + link)
            # print(name)
            # print(tokens)

            time.sleep(0.5)
            # break
    return list_link_productions


def get_page_count(url):
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')

        pagination = soup.find('div', 'v-pagination__wrapper')\
            .find('ul', 'v-list v-pagination__page-numbers u-hide-until-smallDesk v-list--bare')\
            .find_all('li', 'v-list__item v-pagination__page-number')
        list_page_count = [s.text.strip() for s in pagination]

    return int(list_page_count[-1])


def main(url):
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        try:
            page_count = get_page_count(url)
        except AttributeError:
            page_count = 0

        link_pattern = '{}/all?page={}'

        # Цикл по сбору ссылок товаров на страницах по выбранной категории
        for n in range(1, page_count + 1):
            link = link_pattern.format(HOST, n)
            print("Обрабатывается страница: {}".format(n))

            list_link_productions = get_list_page_link_content(link)
            # Напечатать список ссылок товаров по выбранной категории
            for number, link_production in enumerate(list_link_productions):
                print(number + 1, HOST[:-1] + link_production[2])

            # break


def parser_collection():
    r = requests.get(HOST)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')

        list_category_menu = [
            ['book-week', HOST + '/collection/book-week'],
            ['indoor toys', ''],
            ['', ''],
            ['', ''],
            ['', '']
        ]


if __name__ == '__main__':

    # dict_terminal_menu = [
    #     HOST + '/age/0-6-months',
    #     HOST + '/age/6-12-months',
    #     HOST + '/age/12-36-months',
    #     HOST + '/age/3-5-years',
    #     HOST + '/age/5-8-years-plus'
    # ]
    #
    # print("Меню:")
    # for i, j in enumerate(dict_terminal_menu):
    #     print('', i + 1, '-', j)
    # first_question = int(input('Введите пункт меню:\n-> '))
    # main(dict_terminal_menu[first_question - 1])
    # print()

    parser_collection()
