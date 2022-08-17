import requests
from bs4 import BeautifulSoup

HOST = 'https://newyork.craigslist.org'
URL = 'https://newyork.craigslist.org/d/parking-storage/search/prk'
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"
    }


def get_contents(html):
    soup = BeautifulSoup(html.text, 'lxml')

    li_list = soup.find('ul', class_='rows').find_all('li')
    li_output = []

    # temp flag
    # flag = 0
    for li in li_list:
        data = li.find('div', class_='result-info').find('time', class_='result-date').text
        name = li.find('div', class_='result-info').find('h3').find('a', class_='result-title hdrlnk').text
        price = li.find('div', class_='result-info').find('span', class_='result-price').text

        link = li.find('div', class_='result-info').find('h3').find('a').get('href')
        description = get_product_item_content(link)

        li_output.append([data, name, price, ' '.join(description.split()[6:])])

    # # temp IF
    #     flag += 1
    #     if flag == 5:
    #         # for i in get_pic_var:
    #         #     print(i)
    #         break
    #
    # for i in li_output:
    #     for j in i:
    #         print(j)
    #     print(f'_/_/_._/_/\n')


def get_product_item_content(link):
    r = requests.get(link, headers= HEADERS)
    r.encoding = 'windows-1251'
    soup = BeautifulSoup(r.text, 'lxml')

    temp = soup.find('section', class_='userbody')
    story = temp.find('section', id='postingbody').text.strip().replace(r'\n', ' ')

    return story


def main(url):
    r = requests.get(url)
    r.encoding = 'windows-1251'
    get_contents(r)


if __name__ == '__main__':
    main(URL)
