from bs4 import BeautifulSoup
import requests
import time
# import csv
import fake_useragent

FILE = 'Lamoda.ru_page_sheet.csv'
HOST = 'https://www.lamoda.ru/'
URL = 'https://www.lamoda.ru/c/15/shoes-women/?sitelink=topmenuW&l=3&page={}'

fake_user = fake_useragent.UserAgent().random
HEADERS = {
    "Accept": "*/*",
    "User-Agent": fake_user
}


def parser_links_product_for_category_pages():
    r = requests.get(URL, headers=HEADERS)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        paginator = int(soup.find('div', 'paginator').get('data-pages'))

        # Собираем ссылки по всем страницам выбранного товара

        # Стартовые значения флага прерывания.
        # Не менять!
        flag_num_page = 1
        # number_product = 1

        list_url_productions = []

        for number_page in range(1, paginator + 1):
            page = requests.get(URL.format(number_page))

            if page.status_code == 200:
                soup_product = BeautifulSoup(page.text, 'html.parser')

                quantity_product = soup_product.find('div', 'products-catalog__head').text
                quantity_product = quantity_product.split()
                print("Количество товара", quantity_product[0] + ' ' + quantity_product[1] + '\n')

                blocks_products = soup_product.find_all('div', 'products-list-item')

                for block in blocks_products:
                    link_item = block.find('a', 'products-list-item__link link').get('href')
                    list_url_productions.append(HOST + link_item[1:])
            else:
                print("Ошибка в запросе страницы")
            # if list_url_productions is not None:
            #     for url_production in list_url_productions:
            #         # print(f'Страница {flag_num_page}\nТовар № {number_product}\n', HOST + url_production[1:])
            #         number_product += 1
            #     # Флаг прерывает парсинг на определенной странице
            #     if flag_num_page == 1:
            #         break
            # else:
            #     print("""
            #     Список ссылок товаров пуст.
            #     Ошибка в парсинге ссылок товаров по выбранной категории
            #     """)

            flag_num_page += 1
            time.sleep(1)

    return list_url_productions


# def get_product_content():
#     list_url_prod = (parser_links_product_for_category_pages())
#
#     list_params_production = []
#     for url in list_url_prod:
#         r = requests.get(url, headers=HEADERS)
#         if r.status_code == 200:
#             soup = BeautifulSoup(r.text, 'html.parser')
#             list_params_production.append({
#                     "Brand": '',
#                     "Model": '',
#                     "Price": ''
#             })
#
#
#     ...


def main():
    r = requests.get('https://www.lamoda.ru/p/ne024ewllis0/clothes-nerouge-kostyum/', headers=HEADERS)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')

        # Собираем данные в разделе "О товаре" (состав)
        info_product = soup.find('div', 'ii-product__attributes')
        list_prod_info = [{
            info_product.find('span', 'ii-product__attribute-label').text.strip():
                info_product.find('span', 'ii-product__attribute-value').text.strip().split(','),
            "inner_material": '',
            "Outsole material": '',
            "insole_material": '',
            "season": '',
            "color": '',
            "country": '',
            "clasp": '',
            "article": ''
        }]

        print(list_prod_info)

    else:
        print("Ошибка в запросе к странице товара")


# def save_in_csv(file):
#     with open(file, 'w', newline='') as f:
#         writer = csv.writer(f, delimiter=';')
#         writer.writerow(['Ссылка'])
#         for i in file:
#             writer.writerow(i[''])


if __name__ == '__main__':
    # list_url_prod = (parser_links_product_for_category_pages())
    # print(list_url_prod)
    # save_in_csv(list_url_productions)
    main()
