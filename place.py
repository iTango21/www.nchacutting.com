import requests
from bs4 import BeautifulSoup
import lxml
import json
from fake_useragent import UserAgent
import os
import re
# from random import randrange
ua = UserAgent()
ua_ = ua.random

import string

year_ = '2019'

my_path_ = './data'

month_arr = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }


def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

# list_inp = [100, 75, 100, 20, 75, 12, 75, 25]
# a = set()
# b = set()
#
# for i in list_inp:
#     b.clear()
#     b.add(i)
#
#     if a.intersection(b):
#         print(f'{i} - inter')
#     else:
#         print(f'{i} - not inter')
#         a.add(i)
#
# print(a)
#
# breakpoint()



# list_inp = [100, 75, 100, 20, 75, 12, 75, 25]


# val_ = []
# val = set(val_)
#
#
# list_inp = [100, 75, 100, 20, 75, 12, 75, 25]
# # set_res = set(list_inp)
# # print("The unique elements of the input list using set():\n")
# # list_res = (list(set_res))
#
#
# for item in list_inp:
#     i = str(item)
#     print(i)
#     if i.intersection(set(val_)) != set():
#         val_.append(i)
#         print(i)


# for item in list_res:
#     print(item)

# if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
#         .intersection(set(json.load(open('cenz.json')))):  # != set():
#     print('Маты запрещены!..')

# Lines processed:

# breakpoint()








url_ = 'https://www.nchacutting.com/ShowResultsWidget/ShowResultsWidget/'


# cookies = {
#     '_ga_TDHNQ6RXD5': 'GS1.1.1672040869.1.0.1672040869.0.0.0',
#     '_ga': 'GA1.1.2021857423.1672040869',
# }

headers = {
    'authority': 'www.nchacutting.com',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,vi;q=0.5,pt;q=0.4,ka;q=0.3',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_ga_TDHNQ6RXD5=GS1.1.1672040869.1.0.1672040869.0.0.0; _ga=GA1.1.2021857423.1672040869',
    'origin': 'https://www.nchacutting.com',
    'referer': 'https://www.nchacutting.com/ncha-shows/world-standings/lae-show-results',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': f'{ua_}',
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    'pointYear': f'{year_}',
    'showType': 'LAEShows',
}


res_list = []
s1_ = set()
s2_ = set()


with requests.Session() as session:
    response = requests.post(
        f'{url_}',
        headers=headers,
        data=data,
        timeout=(3, 3)
    )

    soup = BeautifulSoup(response.text, 'lxml')
    m_ = soup.find_all('a', class_='list-group-item')
    e_ = soup.find_all('div', class_='row')

    # print(len(m_))
    # print(len(e_))

    for i, x in enumerate(m_):
        tmp_ = x.text.strip().split(' - ')

        month = tmp_[0]
        mmm = month_arr[f'{month}']

        year = tmp_[1]

        date_ = f'{year}_{mmm:02}_{month}'
        print(f'\n{date_}')

        event_ = e_[i].find_all('div', class_='list-group-item small')
        for e in event_:
            id__ = e.find('a').get('onclick')
            id_ = [int(i) for i in re.findall(r'\b\d+\b', id__)]
            # id_ = re.findall('[0-9]+', id__)


            hhh = {
                'authority': 'www.nchacutting.com',
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,vi;q=0.5,pt;q=0.4,ka;q=0.3',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                # 'cookie': '_gid=GA1.2.1213264937.1672038364; _gcl_au=1.1.2084281150.1672038364; _ga_TDHNQ6RXD5=GS1.1.1672038364.1.1.1672038375.0.0.0; _ga=GA1.2.1187653290.1672038364',
                'origin': 'https://www.nchacutting.com',
                'referer': 'https://www.nchacutting.com/ncha-shows/world-standings/lae-show-results',
                'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': f'{ua_}',
                'x-requested-with': 'XMLHttpRequest',
            }

            ddd = {
                'showId': f'{id_[0]}',
            }

            rrr = requests.post(
                'https://www.nchacutting.com/ShowResultsWidget/GetEntriesAndResults/',
                headers=hhh,
                data=ddd,
                timeout=(3, 3)
            )

            new_ = BeautifulSoup(rrr.text, 'lxml')

            all_ = new_.find_all('a', class_='list-group-item small')

            for a in all_:

                info_all = []

                title__ = a.find('div', class_='col-sm-6')
                title_ = title__.text
                th_ = a.find_all('th')
                tr_ = a.find('tbody').find_all('tr')

                for r in tr_:
                    div_ = r.find_all('td')

                    pl_ = div_[0].text.strip()
                    # pl_tmp = pl_.split(' ')

                    # if pl_tmp[0] == 'GoRound':
                    #     place_ = pl_tmp[-1].replace('G', '').split('-')[0]
                    # elif pl_tmp[0] == 'Semifinal':
                    #     place_ = pl_tmp[-1].replace('SF', '').split('-')[0]
                    # else:
                    #     place_ = pl_.split('-')[0]

                    # list_inp = [100, 75, 100, 20, 75, 12, 75, 25]
                    # set_res = set(list_inp)
                    # print("The unique elements of the input list using set():\n")
                    # list_res = (list(set_res))
                    #
                    # for item in list_res: print(item)
                    # Lines
                    # processed:
                    # breakpoint()

                    if (re.findall(r'^\D', pl_)):
                        s2_.clear()
                        s2_.add(pl_)

                        if s1_.intersection(s2_):
                            pass
                        else:
                            s1_.add(pl_)
                            res_list.append(pl_)

                            ev_name_ = e.text.replace("Results", "").strip() \
                                .replace(">", "") \
                                .replace("<", "") \
                                .replace("|", "") \
                                .replace(":", "") \
                                .replace("['", "") \
                                .replace("']", "") \
                                .replace("'", "") \
                                .replace(",", "") \
                                .replace("?", "") \
                                .replace("#", "") \
                                .replace(" ", "_") \
                                .replace("\\", "") \
                                .replace("/", "") \
                                .replace('"', '=') \
                                .replace("*", "")

                            print(f'\t{pl_} ----->>>>> {ev_name_}')

with open(f'place_{year_}.json', 'w', encoding='utf-8') as file:
    json.dump(res_list, file, indent=4, ensure_ascii=False)
