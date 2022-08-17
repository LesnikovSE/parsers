import requests
from bs4 import BeautifulSoup

HOST = 'https://www.kinonews.ru'
URL = 'https://www.kinonews.ru/premiers_world/'
HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    r.encoding = 'windows-1251'
    return r


def get_content(html):
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'lxml')
        trs = soup.find('table', class_='w100p').find_all('tr')

        for tr in trs:
            # tds = tr.find_all('td')
            #
            # for td in tds:
            #     if len(td) == 1:
            #         continue
            #     else:
            #         print(len(td))
            #         print(td)
            #         break
            try:
                date_f = tr.find('div', class_='premier-date').get_text(strip=True)
                name_f = tr.find_all('a', class_='titlefilm').get_text(strip=True)
                url_f = HOST + tr.find('a', class_='titlefilm').get('href')
            except:
                date_f = ''
                name_f = ''
                url_f = ''

            print(date_f, name_f, url_f)

    else:
        print("Error url")


def main():
    get_content(get_html(URL))


if __name__ == '__main__':
    main()
