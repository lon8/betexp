# Скрипт для сбора ссылок матчей с коэффициентами
# Обязательно запускается перед main.py
# 

import configparser
import json
import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

result = {}
config = configparser.ConfigParser()
config.read('config.ini')

pathname = f"data/soccer/{config['date']['year']}-{config['date']['month']}-{config['date']['day']}" 
try:
    os.makedirs(pathname)
except:
    pass


options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('user-data-dir=/home/lon8/privet/betexp/User') # См. комментарии в аналогичном отрезке кода в файле main.py
options.add_argument('--profile-directory=Profile 1')

browser = webdriver.Chrome(options=options)

browser.get(f"https://www.betexplorer.com/next/soccer/?year={config['date']['year']}&month={config['date']['month']}&day={config['date']['day']}")

sleep(3) # Ждём три секунды для полной прогрузки страницы

html = browser.page_source

soup = BeautifulSoup(html, 'lxml')

trs = soup.find_all('tr', class_=False) # Находим все строки таблицы без какого-либо класса.

for tr in trs:
    try:
        name = tr.find('td', class_='table-main__tt').find('a').text # Берем имя матча. Исключение создано для PostPoned-мачтей.
                                                                     # Пропускаем их, если название класса иное
    except:
        continue
    link = tr.find('td', class_='table-main__tt').find('a')['href'] # Берем ссылку
    kef = tr.find('td', class_='table-main__odds')
    if kef is None or kef.text == '\xa0': # '\xa0' - символ "пробела". Простой способ указать пустоту в строке.
                                          # Если находим этот символ, значит коэффициентов на матч нет, а нам такие не нужны.
                                          # Продолжаем работу цикла
        continue
    result[name] = "https://www.betexplorer.com" + link # Добавляем элемент в словарь, если коэффициенты имеются

with open(f'{pathname}/links.json', 'w', encoding='utf-8') as file: # Записываем словарь в json-файл
    json.dump(result, file, indent=4, ensure_ascii=False)

print("Done!") # Готово!