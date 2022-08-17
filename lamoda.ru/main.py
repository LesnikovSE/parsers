from bs4 import BeautifulSoup
import requests
import os
# import time
# import random

HOST = 'https://www.lamoda.ru/'
URL = ''
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
}


def get_links(url):
    request = requests.get(url, headers=HEADERS)

    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        menu_gender = soup.find('div', 'logo-line-wrapper width-wrapper').find_all('a')

        list_gender = []
        for i in menu_gender[2:]:
            list_gender.append([i.get_text().strip(), i.get('href')[1:]])

        script_menu_1 = int(input('Введите номер:\n 1 - Женское\n 2 - Мужское\n 3 - Детское\n-> '))

        list_main_menu = []
        list_left_menu = []

        os.system('cls' if os.name == 'nt' else 'clear')

        # Женщины
        if script_menu_1 == 1:
            request = requests.get(HOST + list_gender[0][1], headers=HEADERS)

            if request.status_code == 200:
                soup = BeautifulSoup(request.text, 'html.parser')
                main_menu = soup.find('div', 'd-header-top-menu-wrapper').find_all('a')

                # Ссылки главного меню
                for i in main_menu:
                    list_main_menu.append([
                        i.text.strip(),
                        HOST + i.get('href')[1:]
                    ])

                list_main_menu = list_main_menu[2:]     # !!! Заменить состав листа

                # Второй пункт скрипта (консоль)
                print('Введите номер:')
                for i, j in enumerate(list_main_menu):
                    print('', i + 1, '-', j[0])

                script_menu_2 = int(input('-> ')) - 1

                # Левое меню
                link = list_main_menu[script_menu_2]
                print('Раздел:', link[0], '\n')

                page = requests.get(link[1], headers=HEADERS)
                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, 'html.parser')
                    left_menu = soup.find('div', 'catalog-navigation-wrap').find_all('li', 'cat-nav-item dt102_li2')

                    # Третий пункт скрипта (консоль)
                    script_menu_3 = int(input('Введите номер\n-> '))
                    if script_menu_3 == 1:
                        quantity_productions(soup)

                    elif script_menu_3 == 2:
                        ...
                    elif script_menu_3 == 3:
                        ...
                    elif script_menu_3 == 4:
                        ...
                    elif script_menu_3 == 5:
                        ...
                    elif script_menu_3 == 6:
                        ...
                    elif script_menu_3 == 7:
                        ...
                    elif script_menu_3 == 8:
                        ...
                    elif script_menu_3 == 9:
                        ...
                    elif script_menu_3 == 10:
                        ...

                else:
                    print("Ошибка в запросе к странице")

            #             # Лист содержит все ссылки бокового меню выбранной категории товара
            #             for menu_1 in left_menu:
            #                 # Общее количество единиц товаров по категори
            #                 name_menu = menu_1.find_all('a', 'link cat-nav_a')
            #
            #                 for i in name_menu:
            #                     list_left_menu.append([i.text.strip(), HOST + i.get('href')[1:]])
            #                 # break
            #
            #             # for i, z in enumerate(list_left_menu):
            #             #     print(i, z[0])
            #
            #         else:
            #             print("Ошибка запроса страницы")
            #
            #     except Exception:
            #         continue
            #
            #     q += 1                #
            #     break
            #     # time.sleep(1)

                # q = 1
                #
                #     link = list_main_menu[number_menu][0]
                #     print('Раздел:', link[0], '\n')

            # # Парсим левое мменю выбранного раздела
            # # try-except : т.к. есть разделы с другой разметкой страниц
            # try:
            #     page = requests.get(link[1], headers=HEADERS)
            #         if page.status_code == 200:
            #             soup = BeautifulSoup(page.text, 'html.parser')
            #             menu = soup.find('div', 'catalog-navigation-wrap').find_all('li', 'cat-nav-item dt102_li1')
            #

            else:
                print('Ошибка в выборе главного меню для "Женщин"')

#          # Мужчины
#          elif number_gender == 2:
#              print(gender_attrs_list[1][1])
#
#              request = requests.get(url + gender_attrs_list[1][1], headers=HEADERS)
#              if request.status_code == 200:
#                  soup = BeautifulSoup(request.text, 'lxml')
#                  gender_main_menu = soup.find('div', id='menu').find('nav')
#                  print(gender_main_menu)
#              else:
#                  print('Ошибка в выборе главного меню для "Мужчин"')
#
#          # Дети
#          else:
#              print(gender_attrs_list[0][1])
#
#              request = requests.get(url + gender_attrs_list[2][1], headers=HEADERS)
#              if request.status_code == 200:
#                  soup = BeautifulSoup(request.text, 'lxml')
#                  gender_main_menu = soup.find('div', id='menu').find('nav')
#                  print(gender_main_menu)
#              else:
#                  print('Ошибка в выборе главного меню для "Детей"')
    else:
        print("Ошибка запроса страницы 'lamoda.ru'")
    return list_left_menu


def quantity_productions(link_page):
    # Количество позиций товаров выбранной категории
    quantity_production = int(link_page.find('div', 'title').find('span').text.strip(' ').split()[0])
    print('Количество товара:', quantity_production, '\n')
    ...


def parser_page_product():
    list_left_menu = get_links(HOST)

    page = requests.get(list_left_menu[0][1], headers=HEADERS)
    if page.status_code == 200:
        soup_pr = BeautifulSoup(page.text, 'html.parser')

        blocks = soup_pr.find_all('div', 'products-list-item')

        # Парсим блоки товаров и сохраняем ссылки
        list_category_product = []
        flag = 0
        for block in blocks:
            list_category_product.append(HOST + block.find('a', 'products-list-item__link link').get('href')[1:])

            # Количество позиций товаров выбранной категории
            quantity_production = int(soup_pr.find('div', 'title').find('span').text.strip(' ').split()[0])
            print('Количество товара:', quantity_production)

            flag += 1
            if flag <= 5:
                continue
            else:
                break

        flag = 0
        for i in list_category_product:
            print(flag)
            print(i)
            flag += 1
    else:
        print("Ошибка запроса страницы")


if __name__ == '__main__':
    # parser_page_product()
    get_links(HOST)
