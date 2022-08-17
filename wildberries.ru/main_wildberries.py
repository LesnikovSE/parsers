#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import fake_useragent
from bs4 import BeautifulSoup
import math
import time
import random

HOST = 'https://www.wildberries.ru'
URL = ''
FAKE_USER = fake_useragent.FakeUserAgent().random
HEADERS = {
    'Accept': '*/*',
    'User-Agent': FAKE_USER
}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r
    else:
        print("Ошибка в запросе страницы")


def get_main_menu():
    """
    Собрать ссылки главного меню страницы "HOST"
    :return: list_main_menu[{name: link}, {...}]
    """

    r = get_html(HOST)
    soup = BeautifulSoup(r.text, 'lxml')

    main_menu = soup.find('div', id='top-menu-inner') \
        .find('ul', 'topmenus').find_all('li', 'topmenus-item')

    list_main_menu = []
    for li in main_menu:
        list_main_menu.append({
            li.find('a').text.strip(): HOST + li.find('a').get('href')})

    return list_main_menu


def get_list_category_menu(url):
    r = get_html(url)

    #for i in list_main_menu:
    #   for name, url in i.items():
    #         r = get_html(url)
    soup = BeautifulSoup(r.text, 'lxml')

    category_menu = soup.find('div', 'left').find('ul', 'maincatalog-list-2')\
        .find_all('li')

    list_category_menu = []
    for second_menu in category_menu:
            list_category_menu.append({
                second_menu.find('a').text.strip(): HOST + second_menu.find('a').get('href')})
        # break

    return list_category_menu


def get_list_category_productions_link(url):
    """
    Собираем ссылки и названия товаров по выбранной категории
    :param url: list_category_menu[i]
    :return: list_category_productions[{name: url}]
    """
    r = get_html(url)
    soup = BeautifulSoup(r.text, 'lxml')
    list_category_productions_link = []
    blocks = soup.find('div', 'catalog-content').find('div', 'catalog_main_table') \
        .find_all('div', 'dtList')

    for i, block in enumerate(blocks):
        list_category_productions_link.append({
            i + 1: HOST + block.find('div', 'dtList-inner').find('a').get('href')
        })
    return list_category_productions_link


def get_product_info(url):
    r = get_html(url)
    soup = BeautifulSoup(r.text, 'lxml')

    # list_production_info = []

    blocks = soup.find('div', 'product-content-v1').find_all('div', 'card-row')

    name = blocks[0].find('div', 'brand-and-name').find('span', 'name').text
    print('Название:', name.strip())

    brand = blocks[0].find('div', 'brand-and-name').find('span', 'brand').text.strip()
    print('Бренд:', brand)

    article = blocks[0].find('div', 'second-horizontal').find('span').text.strip()
    print('Артикль:', article)

    try:
        list_color = []
        colors = blocks[0].find('div', 'colors-preview i-sw-colorpicker') \
            .find('ul', 'swiper-wrapper').find_all('li')

        for color in colors:
            list_color.append(color.find('img').get('title'))
        print('Цвет:', ', '.join(list_color))
    except:
        print('Цвет:', 'None')

    try:
        size = blocks[0].find('div', 'size-list j-size-list').find_all('span')
        size = [i.text.strip() for i in size]
        print('Размер:', ', '.join(size))
    except:
        print('Размер:', 'None')

    # обработка 2 блока со страницы (Состав и тд.)
    composition = blocks[1].find('div', 'card-add-info').find('span').text.strip()
    print('Состав:', composition, '\n')

    description = blocks[1].find('div', 'j-description collapsable-content description-text') \
        .text.strip()
    print('Описание:', description[:100] + '...\n')  # .split('".'))

    params = blocks[1].find('div', 'params').find_all('div', 'pp')
    print('Характеристики:')
    list_parameters = []
    for param in params:
        span_text = [s.text.strip() for s in param.find_all('span')]
        list_parameters.append({
            span_text[0]: span_text[1]})
    for p in list_parameters:
        for k, v in p.items():
            print(k, ':', v)
    print()


def get_page_count(url):
    r = get_html(url)
    soup = BeautifulSoup(r.text, 'lxml')
    # берем количество товара по категории
    # делим на 50 и округляем в большую сторону.
    # получается количество страниц
    print()
    #page_count = soup.select('#body-layout > div > div > span')
    page_count = soup.find('div', id='body-layout').find('span', 'goods-count j-goods-count').text.strip()

    # pagination = soup.find('div', 'pager i-pager').find_all('a', 'pagination-item')
    # pagination = pagination[-1].text
    #
    # print('temp link', temp_link.format())
    # get_page_count(temp_link)

    return page_count


if __name__ == '__main__':

    list_main_menu = get_main_menu()

    # print(list_main_menu)
    print('Главное меню:')
    m = 0
    for i in list_main_menu:
        m += 1
        for k, v in i.items():
            print(' ', m, ' - ', k)
            # print(*i.items())
        # break
    question_1 = int(input('Введите номер:\n-> ')) - 1
    s = '{}'.format(*list_main_menu[question_1])

    print('Меню категории: {}'.format(s))
    url = list_main_menu[question_1].get(s)
    list_category_menu = get_list_category_menu(url)

    m = 0
    for i in list_category_menu:
        m += 1
        for k, v in i.items():
            print(' ', m, ' - ', k)
        # break
    question_2 = int(input('Введите номер:\n-> ')) - 1
    s = '{}'.format(*list_category_menu[question_2])
    print('Начинается обработка категории: {}'.format(s))

    url = list_category_menu[question_2].get(s)
    print(url)


    # list_cat_prods_link = get_list_category_productions_link(url)

    page_count = get_page_count(url)
    page_count = page_count.split(' т')[0].split()
    page_count = int(''.join(page_count))
    page_count = math.ceil(page_count / 50)

    print('Количество страниц к обработке:', str(page_count))
    q_page = int(input('Введите количество страниц для парсинга:\n-> '))
    flag = 0
    z = 1
    # дописать формирование списка с учетом пагинации
    list_cat_prods_link = get_list_category_productions_link(url)

    for page in range(0, page_count):
        print('Страница №{}'.format(page))
        list_cat_prods_link = get_list_category_productions_link(url)
        for cpl in list_cat_prods_link:
            for k, v in cpl.items():
                print('Товар №{}'.format(z))
                print(v)
                get_product_info(v)
                z += 1
                # time.sleep(random.randint(0.5))

        if flag > q_page:
            break

        flag += 1


    # print(list_cat_prod_link)
    #
    # print(get_product_info(list_cat_prod_link[0])) # Парсинг товара (единица)
    #
    # # url = 'https://www.wildberries.ru/catalog/17203592/detail.aspx?targetUrl=GP'
    # # get_product_info(url)