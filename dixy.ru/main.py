from bs4 import BeautifulSoup
import requests
import fake_useragent
import time

FILE_PATH = ''
HOST = ''
URL = 'https://dixy.ru/catalog/'

fake_user = fake_useragent.UserAgent().random
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
              "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-agent": fake_user
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
    # like Gecko) Chrome/88.0.4324.190 Safari/537.36"
}


def get_html(url):
    r = requests.get(url, headers=HEADERS)

    if r.status_code == 200:
        return r.text
    else:
        print("Ошибка запроса страницы")


def get_filter_menu(html):
    """
    Собираем ссылки меню категорий товаров

    :param html: r'url
    :return: dict_menu
    """
    soup = BeautifulSoup(html, 'lxml')

    # Парсим блок "фильтровать по категориям" и формируем список ссылок "названий фильтров (меню)"
    main_menu = soup.find('div', 'filter-panel').find('div', 'category-list').find('ul', 'common')
    list_menu_name = [z.text.strip() for z in main_menu.find_all('li')]

    # Формируем ссылки на страницы товаров и записываем в лист
    list_menu_link_add = []
    for mm in main_menu.find_all('li'):
        list_menu_link_add.append(mm.get('data-code'))

    # Формируем словарь {"name_menu": "link"}
    dict_menu = {'Каталог': URL}
    for n in range(len(list_menu_name)):
        dict_menu[list_menu_name[n]] = URL + list_menu_link_add[n]
        # dict_menu[i] = URL + list_menu_link[i]

    return dict_menu, list_menu_name, list_menu_link_add


def get_content_blocks(url_category):
    """
    Берет ссылку из словаря и парсит
    товары по выбранной категории

    :return: dict_product = []
    """

    print(f'Ссылка на страницу: {url_category}\n')

    r = requests.get(url_category, headers=HEADERS)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')

        # dict_products = []

        block_first = soup.find('div', 'items products').find_all('div', 'iAutoHeight item')

        z = 0
        for bf in block_first:

            z += 1
            print(f'.{z}.')

            try:
                price_old = bf.find('div', 'dixyCatalogItemPrice__oldprice').text.strip()
            except AttributeError:
                price_old = '-'
            try:
                price_sale = bf.find('div', 'dixyCatalogItemPrice__new').find('p').get('content') + ',' + \
                             bf.find('div', 'dixyCatalogItemPrice__kopeck').text.strip()
            except AttributeError:
                price_sale = '-'
            try:
                discount = bf.find('div', 'dixyCatalogItemPrice__discount').text.strip()
            except AttributeError:
                discount = '-'
            try:
                time_of_action = bf.find('div', 'dixyCatalogItem__term').text.strip()
            except AttributeError:
                time_of_action = '-'
            try:
                production_name = bf.find('div', 'dixyModal__info').find('div', 'dixyModal__title').text.strip()
            except AttributeError:
                production_name = '-'

            print('Commodity:', production_name)
            print(' Old price:', price_old)
            print(' New price:', price_sale)
            print(' Sale:', discount)
            print(' Data sale:', time_of_action.replace('  ', ' '))

            time.sleep(0.5)

            break

        block_second = soup.find('div', 'items products').find_all('div', 'iAutoHeight item more')
        for bs in block_second:
            # parse fields price

            z += 1
            print(f'.{z}.')

            try:
                price_old = bs.find('div', 'dixyCatalogItemPrice__oldprice').text.strip()
            except AttributeError:
                price_old = '-'
            try:
                price_sale = bs.find('div', 'dixyCatalogItemPrice__new').find('p').get('content') + ',' +\
                             bs.find('div', 'dixyCatalogItemPrice__kopeck').text.strip()
            except AttributeError:
                price_sale = '-'
            try:
                discount = bs.find('div', 'dixyCatalogItemPrice__discount').text.strip()
            except AttributeError:
                discount = '-'
            try:
                time_of_action = bs.find('div', 'dixyCatalogItem__term').text.strip()
            except AttributeError:
                time_of_action = '-'
            try:
                production_name = bs.find('div', 'dixyModal__info').find('div', 'dixyModal__title').text.strip()
            except AttributeError:
                production_name = '-'

            print('Commodity:', production_name)
            print(' Old price:', price_old)
            print(' New price:', price_sale)
            print(' Sale:', discount)
            # .split('-')[1].strip())
            print(' Data sale:', time_of_action.replace('  ', ' '))

            time.sleep(0.5)

            break

    else:
        print('Что-то не так с URL !')


def save_file():
    ...


if __name__ == '__main__':

    filter_menu = get_filter_menu(get_html(URL))
    # print(filter_menu[0]['Кондитерские изделия'] + '/?PAGEN_1=2')

    # Terminal menu output
    print('Список всех категорий товаров.')
    for i, j in enumerate(filter_menu[1]):
        print(' ', i, '-', j)
    question_1 = int(input('Введите номер:\n-> '))

    if question_1 == 0:
        print('Идет парсинг страницы:\n->', 'Вся продукция')
        get_content_blocks(filter_menu[0]['Каталог'])

    elif question_1 == 1:
        print('Идет парсинг страницы:\n->', 'Кондитерские изделия')
        get_content_blocks(filter_menu[0]['Кондитерские изделия'])
    # elif question_1 == 2:
    #     print('Идет парсинг страницы:\n->', 'Готовые завтраки, семечки, сухофрукты')
    #     get_content_blocks(filter_menu['Готовые завтраки, семечки, сухофрукты'])
    # elif question_1 == 3:
    #     print('Идет парсинг страницы:\n->', 'Консервы, соусы')
    #     get_content_blocks(filter_menu['Консервы, соусы'])
    # elif question_1 == 4:
    #     print('Идет парсинг страницы:\n->', 'Кофе, чай')
    #     get_content_blocks(filter_menu['Кофе, чай'])
    # elif question_1 == 5:
    #     print('Идет парсинг страницы:\n->', 'Красота')
    #     get_content_blocks(filter_menu['Красота'])
    # elif question_1 == 6:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 7:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 8:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 9:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 10:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 11:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 12:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 13:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 14:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 15:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 16:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 17:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 18:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
    # elif question_1 == 19:
    #     print('Идет парсинг страницы:\n->', filter_menu[''])
    #     get_content_blocks(filter_menu[''])
