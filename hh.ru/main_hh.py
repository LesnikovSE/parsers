import requests
from bs4 import BeautifulSoup
import time
import fake_useragent
import random

HOST = 'https://hh.ru/'
URL_VACANCIES = 'https://hh.ru/search/vacancy'
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


def get_vacancies_list():
    find_vacancy = input('Введите название ваканси:\n-> ').strip().split()
    # find_vacancy = 'Python стажер'.strip().split()
    find_vacancy = '+'.join(find_vacancy)

    # https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=%D0%B1%D0%B8%D0%BE%D0%BB%D0%BE%D0%B3
    pattern_link = '{}/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text={}' \
        .format(HOST, find_vacancy)

    r = get_html(pattern_link)
    soup = BeautifulSoup(r.text, 'lxml')

    # list_find_vacancy = []

    count_vacancy = soup.find('h1', {'data-qa': 'bloko-header-1'}).text.strip()
    print('Количество вакансий:', count_vacancy, '\n')

    blocks = soup.find('div', 'vacancy-serp').find_all('div', 'vacancy-serp-item')

    flag = int(input("Введите количество вакансий для парсинга.\n'Ноль' - парсить весь список вакансий.\n-> "))
    print()
    point = 1
    for block in blocks:
        print("№", point)
        print("Вакансия:", block.find('div', 'vacancy-serp-item__info') \
              .find('span', 'g-user-content').find('a').text)
        print("Фирма:", block.find('a', 'bloko-link bloko-link_secondary').text.strip())
        print("Локация:", block.find('span', 'vacancy-serp-item__meta-info').text.strip())
        print("Обязанность:", block.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}) \
              .text.strip())
        print("Требования:", block.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}) \
              .text.strip())

        # print(block.find('div', 'vacancy-serp-item__row vacancy-serp-item__row_controls'))
        try:
            print('Дата публикации:', block.find('div', 'vacancy-serp-item__row vacancy-serp-item__row_controls') \
                  .find('span', 'vacancy-serp-item__publication-date vacancy-serp-item__publication-date_s-only').text.strip())
        except AttributeError:
            print('Дата публикации: Рекламное сообщение')
        print()
        time.sleep(random.randint(0, 3))

        point += 1
        if point > flag != 0:
            break


if __name__ == '__main__':
    get_vacancies_list()
    print("Парсинг завершен")
    print(input("Нажмите любую клавишу...\n"))
