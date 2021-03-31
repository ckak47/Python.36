import requests
from lxml import html
from bs4 import BeautifulSoup
soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')