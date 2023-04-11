import json
import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

result = {}
year = "2023"
month = "04"
day = "11"


options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument(r'user-data-dir=User/')
options.add_argument('--profile-directory=Profile 1')

browser = webdriver.Chrome(options=options)

browser.get(f'https://www.betexplorer.com/next/soccer/?year={year}&month={month}&day={day}')

sleep(5)

html = browser.page_source

soup = BeautifulSoup(html, 'lxml')

trs = soup.find_all('tr', class_=False)

for tr in trs:
    try:
        name = tr.find('td', class_='table-main__tt').find('a').text
    except:
        continue
    link = tr.find('td', class_='table-main__tt').find('a')['href']
    kef = tr.find('td', class_='table-main__odds')
    if kef is None or kef.text == '\xa0':
        continue
    result[name] = "https://www.betexplorer.com" + link
pathname = f'data/soccer/{year}-{month}-{day}'
try:
    os.makedirs(pathname)
except:
    pass
with open(f'{pathname}/links.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)

print("Done!")