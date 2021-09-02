import requests
from bs4 import BeautifulSoup
import string
import os

title_news = []
page = int(input())
articles_type = input()
cwd = os.getcwd()
# print(cwd)

def save_article_on_page(the_article_type, dir_name, url):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for i in soup.find_all('article'):
        span = i.find('span', {"class": "c-meta__type"}).text
        if span == the_article_type:
            title = i.find('a', {'data-track-label': "link"}).text
            name = title.strip().translate(str.maketrans(" ", "_", string.punctuation)) + ".txt"
            title_news.append(name)
            urla = f"https://www.nature.com{i.a.get('href')}"
            r2 = requests.get(urla)
            soup2 = BeautifulSoup(r2.content, 'html.parser')
            article_body = soup2.find('div', {'class': 'c-article-body'}).text.strip()
            file = open(dir_name + '\\' + name, 'w', encoding='UTF-8')
            file.write(article_body)
            print('File written')
            file.close()



for n in range(page):
    dir_name = f'Page_{n + 1}'
    url = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&Page={n + 1}'
    save_article_on_page(articles_type, dir_name, url)
print("Saved all articles.")