import csv
import json
import os
from bs4 import BeautifulSoup
import requests
import tomllib

cookies = {
    'my_timezone': '+2', # Важно. Если будете работать с куки, то этот параметр обязателен
                         # Нужен для корректности отображения даты
}

headers = {
    'authority': 'www.betexplorer.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'referer': 'https://www.betexplorer.com/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

with open('config.toml', 'rb') as file: # Считываем config - файл
    cdata = tomllib.load(file)

pathname = f"data/soccer/{cdata['date']['year']}-{cdata['date']['month']}-{cdata['date']['day']}" #Создаем путь, если его нет
try:
    os.makedirs(pathname)
except:
    pass

with open(f'{pathname}/result.csv', 'w', encoding='utf-8') as file: # Добавляем заголовки
    writer = csv.writer(file)
    writer.writerow((
        "Team 1", "Team 2", "Result"
    ))

with open(f'{pathname}/links.json', 'r', encoding='utf-8') as file: # Загружаем данные из links.json
    jdata = json.load(file)

for name, link in jdata.items():
    req = requests.get(link, headers=headers, cookies=cookies)

    soup = BeautifulSoup(req.text, 'lxml')

    teams = soup.find_all('h2', class_='list-details__item__title')

    team_1 = teams[0].text # Команда №1
    team_2 = teams[1].text # Команда №2

    score = soup.find('p', id='js-score').text # Счет игры. Если его еще нет, будет указано "-:-"

    with open(f'{pathname}/result.csv', 'a', encoding='utf-8') as file: # Записываем данные в файл
        writer = csv.writer(file)
        writer.writerow((
            team_1, team_2, score
        ))

    print(name)
print('Done!')