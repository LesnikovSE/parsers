"""
https://free-proxy-list.net/
"""
import requests
from bs4 import BeautifulSoup
from random import choice


def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:50]

    proxies = []

    for tr in trs:
        tds = tr.find_all('td')

        ip = tds[0].text.split()
        port = tds[1].text.split()
        type_ip = 'https' if 'yes' in tds[6].text.split() else 'http'
        proxy = {
            'schema': type_ip,
            'address': ip[0] + ':' + port[0]
        }
        proxies.append(proxy)

    return choice(proxies)


def get_html(url):
    # proxies = {'https': 'ipaddress:5000'}
    p = get_proxy()
    # {'schema': '', 'address': ''}

    proxy = {p['schema']: p['address']}
    r = requests.get(url, proxies=proxy, timeout=2)
    return r.json()['origin']


def main():
    url = 'http://httpbin.org/ip'

    print(get_html(url))


if __name__ == '__main__':
    main()
