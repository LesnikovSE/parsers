#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import requests
from bs4 import BeautifulSoup as bs
import output

URL = 'http://www.usynovite.ru/db/'
HOST = 'http://www.usynovite.ru'


def get_html(url):
    r = requests.get(url, timeout=5)
    if r.ok:
        return r.text
    else:
        print("bad request")


def get_region_code(link):
    r = get_html(link)
    soup = bs(r, 'html.parser')
    divs_s = soup.select_one('.poisk__form>div>div>select')
    option = divs_s.select('option')
    dict_regions = {}
    for i in option[1:]:
        dict_regions[i.text.strip()] = int(i.get('value'))
    return dict_regions


def parse_region(reg):
    form_data = {'region': reg}
    s = requests.session()
    r = requests.post(URL, data=form_data)
    pages = paginator(r.text)

    list_output = []

    if pages != 0:
        for page in range(pages):
            print(f'обрабатывается страница {page+1}')
            paginator_link = f"?p={page+1}&last-search"
            r = s.post(URL + paginator_link, data=form_data)
            soup = bs(r.text, 'html.parser')
            blocks = soup.select('.search-bd__slaider')

            for block in blocks:
                info_div = block.select_one('div:nth-child(2)')
                href = info_div.find('a').get('href')
                name = info_div.select_one('a>h2').text
                info = block.select('p')
                number_questionnaire = info[0].text.strip().split(':')
                region = info[1].text.strip().split(':')
                birth = info[2].text.strip()
                color_eyes = info[3].text.strip().split(':')
                color_hair = info[4].text.strip().split(':')
                character = info[5].text.strip().split(':')
                device_shapes = info[6].text.strip().split(':')
                group_of_health = info[7].text.strip().split(':')
                absence_mom = info[8].text.strip().split(':')
                absence_dad = info[9].text.strip().split(':')
                family = info[10].text.strip().split(':')
                date_publicattion_photo = info[11].text.strip().split(' — ')
                where_to_apply = info[12].find('a').get('href')

                list_output.append(
                    {
                        number_questionnaire[1].strip():
                            {
                                'Имя': name,
                                'Ссылка': HOST+href,
                                region[0]: region[1].strip(),
                                'Дата рождения': birth,
                                color_eyes[0]: color_eyes[1].strip(),
                                color_hair[0]: color_hair[1].strip(),
                                character[0]: character[1].strip(),
                                device_shapes[0]: device_shapes[1].strip(),
                                group_of_health[0]: group_of_health[1].strip(),
                                absence_mom[0]: absence_mom[1].strip(),
                                absence_dad[0]: absence_dad[1].strip(),
                                family[0]: family[1].strip(),
                                date_publicattion_photo[0]: date_publicattion_photo[1].strip(),
                                'куда обращаться': HOST+where_to_apply
                            }
                    }
                )
            time.sleep(0.2)
    else:
        list_output.append({'None': 'None'})
        time.sleep(0.2)

    return list_output


def paginator(html):
    soup = bs(html, 'html.parser')
    if soup.select_one('div.paginator'):
        pages = soup.select_one('div.paginator').select_one('a.paginator__to-end').get('href')
        pages = pages.split('=')[1].split('&')[0]
    else:
        pages = 0
    return int(pages)


if __name__ == '__main__':
    dict_code_region = get_region_code(URL)
    main_output = {}

    for code_region in dict_code_region.values():
        print(f"Собираем информацию по региону: {code_region}")
        data = parse_region(code_region)
        main_output[code_region] = data

        with open(f'output/output.json', 'w+') as f:
            output.dump(main_output, f, ensure_ascii=False)
