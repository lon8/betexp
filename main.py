import csv
import json
import os
from time import sleep
import tomllib
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# cookies = {
#     'my_timezone': '+2',
# }

# headers = {
#     'authority': 'www.betexplorer.com',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#     'cache-control': 'max-age=0',
#     'referer': 'https://www.betexplorer.com/',
#     'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
# }

with open('config.toml', 'rb') as file: # Считываем config - файл
    cdata = tomllib.load(file)

pathname = f"data/soccer/{cdata['date']['year']}-{cdata['date']['month']}-{cdata['date']['day']}" #Создаем путь, если его нет
try:
    os.makedirs(pathname)
except:
    pass

with open(f'{pathname}/table.csv', 'a', encoding='utf-8') as file: #Создаем файл с заголовками
    writer = csv.writer(file)
    writer.writerow((
        "DateTime",
        "Sport",
        "Country",
        "Liga",
        "Team 1",
        "Team 2",
        "Odd 1",
        "Odd X",
        "Odd 2",
        "MP",
        "Team 1 Home L1 O", 
        "Team 1 Home L1 R", 
        "Team 1 Home L2 O", 
        "Team 1 Home L2 R", 
        "Team 1 Home L3 O",
        "Team 1 Home L3 R",
        "Team 1 Home L4 O", 
        "Team 1 Home L4 R", 
        "Team 1 Home L5 O",
        "Team 1 Home L5 R",
        "Team 1 Away L1 O",
        "Team 1 Away L1 R",
        "Team 1 Away L2 O",
        "Team 1 Away L2 R",
        "Team 1 Away L3 O",
        "Team 1 Away L3 R", 
        "Team 1 Away L4 O",
        "Team 1 Away L4 R", 
        "Team 1 Away L5 O",
        "Team 1 Away L5 R",
        "Team 2 Home L1 O", 
        "Team 2 Home L1 R", 
        "Team 2 Home L2 O", 
        "Team 2 Home L2 R", 
        "Team 2 Home L3 O", 
        "Team 2 Home L3 R", 
        "Team 2 Home L4 O", 
        "Team 2 Home L4 R", 
        "Team 2 Home L5 O", 
        "Team 2 Home L5 R", 
        "Team 2 Away L1 O", 
        "Team 2 Away L1 R", 
        "Team 2 Away L2 O", 
        "Team 2 Away L2 R", 
        "Team 2 Away L3 O", 
        "Team 2 Away L3 R", 
        "Team 2 Away L4 O", 
        "Team 2 Away L4 R", 
        "Team 2 Away L5 O", 
        "Team 2 Away L5 R", 
        "Link"
    ))



with open(f'{pathname}/links.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('user-data-dir=C:/Users/vladk/betexp/User_win') # Итак, здесь мы должны указать папку с данными. Это
options.add_argument('--profile-directory=Profile 1')                # нужно для того, чтобы мы работали в другом часовом
                                                                     # поясе (+2). Указываем полный путь к папке, а не относительный,
                                                                     # это важно!! Папка User - для Linux, папка User_win - для Windows

# Здесь также указываем путь к chromedriver. У меня он установлен в PATH, поэтому я путь не указываю.
browser = webdriver.Chrome(options=options)

# Начинаем проходиться по ссылкам в links.json. Для работы программы нужно запустить links.py
# Также важно будет указать дату в файле config.toml
for name, link in data.items():
    print(link)

    browser.get(link)

    sleep(1)
    
    soup = BeautifulSoup(browser.page_source, "lxml")
    date = soup.find('p', id='match-date').text #Дата

    breadcrumb_list = soup.find('ul', 'list-breadcrumb').find_all('li')
    sport = breadcrumb_list[1].text # Спорт
    country = breadcrumb_list[2].text # Страна
    league = breadcrumb_list[3].text # Лига
 
    teams = soup.find_all('h2', class_='list-details__item__title')
    team_1 = teams[0].text # Первая команда (по идее, она всегда домашняя. Я точно не знаю, не сильно разбираюсь в этом)
    team_2 = teams[1].text # Вторая

    match_id = link.split('/')[-2]
    try:
        average_odds = soup.find('tfoot', id='match-add-to-selection').find('tr').find_all('td', class_='table-main__detail-odds')
        odd_1 = average_odds[0].text # 1
        odd_2 = average_odds[1].text # X
        odd_3 = average_odds[2].text # 2
    except: # Если нету (их может не быть), то пишем None
        odd_1 = 'None'
        odd_2 = 'None'
        odd_3 = 'None'
    try:
        mp = soup.find('td', class_='matches_played col_matches_played').text # Количество матчей
    except:
        mp = "None"

    
    # _1 = Первая команда
    home_odds_1 = []
    home_results_1 = []
    away_odds_1 = []
    away_results_1 = []
    try:
        home_rows = soup.find('div', id='match-results-home').find('tbody').find_all('tr')
        
        # Проходимся по строчкам
        for row in home_rows:
            # В таблице название команды противника указаны с классом muted. Если команда с классом muted стоит первая, то
            # это значит, что наша команда была гостем
            test = row.find('td', class_='h-text-left').find('p', class_='muted')['class']
            if len(test) == 1: # Смысл проверки в том, что у нашей команды в html указано два класса.
                               # Если количество классов равно одному, то наша команда была гостем
                result = row.find('td', class_='table-main__formicon').find('i')['class'][-1] 
                # Здесь мы по названию класса иконки определяем результат матча
                if result == 'icon__d':
                    away_results_1.append('D')
                elif result == 'icon__w':
                    away_results_1.append('W')
                elif result == 'icon__l':
                    away_results_1.append('L')
                else:
                    away_results_1.append('N')
                odd = row.find_all('td', class_='table-main__odds')[-1].text # Если команда в гостях, то коэффициент будет последним
                away_odds_1.append(odd)
            else: # Делаем те же действия, только для случая того, когда команда играла дома
                result = row.find('td', class_='table-main__formicon').find('i')['class'][-1]
                if result == 'icon__d':
                    home_results_1.append('D')
                elif result == 'icon__w':
                    home_results_1.append('W')
                elif result == 'icon__l':
                    home_results_1.append('L')
                else:
                    home_results_1.append('N')
                odd = row.find_all('td', class_='table-main__odds')[0].text
                home_odds_1.append(odd)
    except:
        pass
    
    # Код немного кривоват, но работает максимально стабильно.
    # Если результатов домашних матчей меньше или больше пяти,
    # то мы либо добавляем None, либо удаляем самые старые элементы,
    # пока количество не станет равняться 5
    if len(home_odds_1) < 5:
        while len(home_odds_1) < 5:
            home_odds_1.append('None')
            home_results_1.append('None')
    if len(home_odds_1) > 5:
        while len(home_odds_1) > 5:
            home_odds_1.pop()
            home_results_1.pop()

    if len(away_odds_1) < 5:
        while len(away_odds_1) < 5:
            away_odds_1.append('None')
            away_results_1.append('None')
    if len(away_odds_1) > 5:
        while len(away_odds_1) > 5:
            away_odds_1.pop()
            away_results_1.pop()

    #_2 = Вторая команда
    # Проделываем те же действия для второй команды

    home_odds_2 = []
    home_results_2 = []
    away_odds_2 = []
    away_results_2 = []

    
    try:
        away_rows = soup.find('div', id='match-results-away').find('tbody').find_all('tr')

        for row in away_rows:
            test = row.find('td', class_='h-text-left').find('p', class_='muted')['class']
            if len(test) == 1:
                result = row.find('td', class_='table-main__formicon').find('i')['class'][-1]
                if result == 'icon__d':
                    away_results_2.append('D')
                elif result == 'icon__w':
                    away_results_2.append('W')
                elif result == 'icon__l':
                    away_results_2.append('L')
                else:
                    away_results_2.append('N')
                odd = row.find_all('td', class_='table-main__odds')[-1].text
                away_odds_2.append(odd)
            else:
                result = row.find('td', class_='table-main__formicon').find('i')['class'][-1]
                if result == 'icon__d':
                    home_results_2.append('D')
                elif result == 'icon__w':
                    home_results_2.append('W')
                elif result == 'icon__l':
                    home_results_2.append('L')
                else:
                    home_results_2.append('N')
                odd = row.find_all('td', class_='table-main__odds')[0].text
                home_odds_2.append(odd)
    except:
        pass

    if len(home_odds_2) < 5:
        while len(home_odds_2) < 5:
            home_odds_2.append('None')
            home_results_2.append('None')
    if len(home_odds_2) > 5:
        while len(home_odds_2) > 5:
            home_odds_2.pop()
            home_results_2.pop()

    if len(away_odds_2) < 5:
        while len(away_odds_2) < 5:
            away_odds_2.append('None')
            away_results_2.append('None')
    if len(away_odds_2) > 5:
        while len(away_odds_2) > 5:
            away_odds_2.pop()
            away_results_2.pop()
    
    # Открываем csv - файл и записываем все значения

    with open(f'{pathname}/table.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            date,
            sport,
            country,
            league,
            team_1,
            team_2,
            odd_1,
            odd_2,
            odd_3,
            mp,
            home_odds_1[0],
            home_results_1[0],
            home_odds_1[1],
            home_results_1[1],
            home_odds_1[2],
            home_results_1[2],
            home_odds_1[3],
            home_results_1[3],
            home_odds_1[4],
            home_results_1[4],
            away_odds_1[0],
            away_results_1[0],
            away_odds_1[1],
            away_results_1[1],
            away_odds_1[2],
            away_results_1[2],
            away_odds_1[3],
            away_results_1[3],
            away_odds_1[4],
            away_results_1[4],
            home_odds_2[0],
            home_results_2[0],
            home_odds_2[1],
            home_results_2[1],
            home_odds_2[2],
            home_results_2[2],
            home_odds_2[3],
            home_results_2[3],
            home_odds_2[4],
            home_results_2[4],
            away_odds_2[0],
            away_results_2[0],
            away_odds_2[1],
            away_results_2[1],
            away_odds_2[2],
            away_results_2[2],
            away_odds_2[3],
            away_results_2[3],
            away_odds_2[4],
            away_results_2[4],
            link
        ))
    print('Done!') # Готово!