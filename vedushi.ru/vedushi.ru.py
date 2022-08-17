#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
import time

# from selenium import webdriver
# from selenium.webdriver.common.by import By


HOST = 'https://vedushi.ru'
URL = 'https://vedushi.ru/?price50000-999999'
FAKE_USER = fake_useragent.UserAgent()


# def create_html_file_selenium(url):
#
# 	  # add click in link_filter "50000-..."
#
#     driver = webdriver.Chrome()
#     driver.get(url)
#
#     i = 0
#     while i < 550:
#         driver.execute_script("window.scrollBy(0,500)", "")
#         time.sleep(0.3)
#         i += 1
#         # print(i)
#
#     # div.top = 844
#     all_sections = driver.find_elements(By.TAG_NAME, "div.top>a")
#     print(len(all_sections))
# 
#     with open('html.html', 'w') as file:
#         file.write(driver.page_source)


def create_main_page():
    f = open('html.html', 'r')
    soup = bs(f, 'lxml')
    blocks = soup.select('section> div.top')

    list_main_link = []
    for block in blocks:
        link = block.find('a').get("href")
        list_main_link.append(link)
    return list_main_link


def get_html(link):
    r = requests.get(link)
    if r.ok:
        return r.text
    else:
        print("NO request")


def get_info(lst: list):
    dict_output = {}
    print(len(lst))
    i = 1
    for link in (lst):
        print(i)
        r = get_html(HOST + link)
        soup = bs(r, 'lxml')
        try:
            block_1 = soup.select_one('div.mainContent')
            name = block_1.find('h1').text.strip()
            list_description = block_1.select('p')
            description_temp = [s.get_text(strip=True).replace('&nbsp;', ' ') for s in list_description]
            description = ' '.join([*description_temp])
            description = description.replace(" ", ' ')
        except:
            name = ''
            description = ''
        try:
            block_2 = soup.select_one('div.block.main-info')
            exam = block_2.find("img")["alt"]
            stars = block_2.select_one('div.rating> div')['style'].split(':')[-1][:-1]
            price = block_2.select_one('div.price').text.strip()
        except:
            exam = ''
            stars = ''
            price = ''
        try:
            block_3 = soup.select_one('div.block.contacts')
            true_contact = block_3.find('p').text.strip()
            soc_list = block_3.select('.socials> a')
            socials_link = {}
            for item in soc_list:
                name_item = item.text.strip()
                link_item = item['href']
                socials_link[name_item] = link_item
        except:
            true_contact = ''
            socials_link = {}
        try:
            block_4 = soup.select_one('div.block.info')
            discount = block_4.find('table').get_text(strip=True)
        except:
            discount = ''

        try:
            # get phone number
            block_5 = soup.find('form', id='add_reply')
            artist_id = block_5.find('input', {'name': 'artist_id'})
            headers = {'user-agent': FAKE_USER.random}
            payload = {'artist_id': int(artist_id['value'])}
            r = requests.post("https://vedushi.ru/inc/ajax/contacts_click.php", headers=headers, json=payload)
            phone = r.json()['phone'][13:-22]
        except:
            phone = ''

        dict_output[name] = {
            'phone': phone,
            'exam': exam,
            'price': price,
            'stars': stars,
            'discount': discount,
            'true_contact': true_contact,
            'social_link': socials_link,
            'description': description,
            'url': HOST + link
        }
        time.sleep(0.5)
        i += 1
    return dict_output


if __name__ == "__main__":
    list_main_page = create_main_page()
    dict_main = get_info(list_main_page)

    with open('output.output', 'w') as f:
        json.dump(dict_main, f, ensure_ascii=False)
