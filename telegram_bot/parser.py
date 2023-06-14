import json
import requests
import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup


def get_event():
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4076.0 Mobile Safari/537.36'}
    url = 'https://ufc.ru/events'
    req = requests.get(url=url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')
    names_lst = []
    event = soup.find('div', class_='field field--name-taxonomy-term-title field--type-ds field--label-hidden field__item').find('h5').text.strip()
    date_time = soup.find('div', class_='c-card-event--result__date tz-change-data').find('a').text.strip()
    address = soup.find('div', class_='field field--name-location field--type-address field--label-hidden field__item').find('p').text.strip()

    names_lst.append(
        {
            "event": event,
            "address": address,
            "date_time": date_time
        }
    )
    with open('data/event.json', 'w', encoding="utf-8") as f:
        json.dump(names_lst, f, indent=4, ensure_ascii=False)
    print('-----Событие записано в файл-----')



def run_job():
    print("Running job...")
    get_event()
    print("Job completed.")


get_event()

next_run = datetime.now() + timedelta(hours=1)
while True:
    current_time = datetime.now()

    if current_time >= next_run:
        run_job()
        next_run = current_time + timedelta(hours=1)

    time.sleep(60)
