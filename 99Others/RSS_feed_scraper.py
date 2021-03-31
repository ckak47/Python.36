import requests
from bs4 import BeautifulSoup
import json
import time


def save_function(article_list):
    with open('articles.txt', 'w') as outfile:
        json.dump(article_list, outfile)


if __name__ == '__main__':
    # start time stamp
    # timestamp1 = time.clock()
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())

    # scraping function
    article_list = []
    try:
        r = requests.get('https://www.torlock.com/music/rss.xml')
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text
            article = {
                'title': title,
                'link': link,
                'published': published
            }
            article_list.append(article)
    finally:
        print(article_list)
