import json
import requests
from bs4 import BeautifulSoup

with open('data/soccer/2023-04-11/links.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

