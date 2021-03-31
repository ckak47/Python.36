import requests
from lxml import html
from bs4 import BeautifulSoup
url = 'http://data.gdeltproject.org/events/index.html' #需要爬数据的网址
page = requests.Session().get(url)
tree = html.fromstring(page.text)
soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
file_name = soup.find_all("CSV.zip")
print(soup.text)
