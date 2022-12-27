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

year_ = '2022'

my_path_ = './data_weekend'

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
    # 'cookie': '_gid=GA1.2.42207672.1672040870; _gcl_au=1.1.2090788266.1672040870; _ga_TDHNQ6RXD5=GS1.1.1672142442.3.0.1672142442.0.0.0; _ga=GA1.1.2021857423.1672040869',
    'origin': 'https://www.nchacutting.com',
    'referer': 'https://www.nchacutting.com/ncha-shows/world-standings/show-results',
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
    'showType': 'WeekendShows',
}

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

            print(f'\t{ev_name_} >>> ID : {id_}')

            f_d = (e.text.split(' ')[0]).strip().split('/')
            file_date = f"{year_}-{int(f_d[0]):02}-{int(f_d[1]):02}"

            dir_name = f'{my_path_}/{year_}/{date_}/{ev_name_}'
            my_makedirs(f'{dir_name}')

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

                    col_1 = th_[1].text
                    if col_1 != 'Rider':
                        tmp1 = str(div_[1]).split('<span>')

                        horse_ = tmp1[0].replace('<td>', '').replace('<br/>', '').strip()
                        owner__ = ' '.join(str(tmp1[1]).split('<br/>')[0].strip().split())
                        owner_ = owner__.replace(' 2nd Owner: ', '*****').replace('Owner: ', '')

                        info_all.append(
                            {
                                f"{th_[0].text}": ' '.join(div_[0].text.strip().split()),
                                f"Horse": horse_,
                                f"Owner": owner_,
                                f"{th_[2].text}": ' '.join(div_[2].text.strip().split()),
                                f"{th_[3].text}": ' '.join(div_[3].text.strip().split()),
                                f"{th_[4].text}": ' '.join(div_[4].text.strip().split()),
                                f"{th_[5].text}": ' '.join(div_[5].text.strip().split())
                            }
                        )

                    else:
                        tmp1 = str(div_[2]).split('<span>')

                        horse_ = tmp1[0].replace('<td>', '').replace('<br/>', '').strip()
                        owner__ = ' '.join(str(tmp1[1]).split('<br/>')[0].strip().split())
                        owner_ = owner__.replace(' 2nd Owner: ', '*****').replace('Owner: ', '')

                        info_all.append(
                            {
                                f"{th_[0].text}": ' '.join(div_[0].text.strip().split()),
                                f"{th_[1].text}": ' '.join(div_[1].text.strip().split()),
                                f"Horse": horse_,
                                f"Owner": owner_,
                                f"{th_[3].text}": ' '.join(div_[3].text.strip().split()),
                                f"{th_[4].text}": ' '.join(div_[4].text.strip().split()),
                                f"{th_[5].text}": ' '.join(div_[5].text.strip().split())
                            }
                        )

                file_name = f'{id_[0]}_{title_}.json' \
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

                with open(f'{dir_name}/{file_date}_{file_name}', 'w', encoding='utf-8') as file:
                    json.dump(info_all, file, indent=4, ensure_ascii=False)
