import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.us-proxy.org/')
soup = BeautifulSoup(r.text, 'lxml')

trs = soup.find('table', id='proxylisttable').find('tbody').find_all('tr')

for tr in trs:
    tds = tr.find_all('td')

    # proxy_list =
    for td in tds:
        print(td.get_text())
