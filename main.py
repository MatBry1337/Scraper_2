import requests
from string import punctuation
from pathlib import Path
from bs4 import BeautifulSoup


def write_article(soup: BeautifulSoup, valid_type: str, page_path: Path):
    def process_title(title: str) -> str:
        title = title.strip()
        for i in punctuation:
            title = title.replace(i, "")
        title = title.replace(" ", "_")
        return title

    def get_content(url) -> str:
        url = "https://www.nature.com" + url
        r = requests.get(url)
        if r.status_code == 200:
            soupy = BeautifulSoup(r.content, 'html.parser')
            try:
                body = soupy.find("div", {"class": "c-article-body"}).text
            except AttributeError:
                try:
                    body = soupy.find("div", {"class": "article-item__body"}).text
                except AttributeError:
                    body = soupy.find("article").text
            return body

    for article in soup.find_all("article"):
        article_type = article.find("span", {"data-test": "article.type"}).find("span").text
        if article_type == valid_type:
            a_tag = article.find("a", {"data-track-action": "view article"})
            article_url = a_tag["href"]
            article_title = process_title(a_tag.text) + ".txt"
            article_body = get_content(article_url)
            with open(page_path/article_title, 'w') as file:
                file.write(article_body)
            print(article_body)


def main():
    org_url = "https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page="
    page = int(input())
    valid_type = input()
    for num in range(1, page+1):
        page_path = Path(Path.cwd()/f"Page_{num}")
        page_path.mkdir(exist_ok=True)
        url = org_url + str(num)
        r = requests.get(url)
        if r.status_code == 200:
            main_page = BeautifulSoup(r.content, "html.parser")
            write_article(main_page, valid_type, page_path)
        else:
            print(f"Error: {r.status_code}")


if __name__ == "__main__":
    main()


# def save_article_on_page(article_type, dir_name, url):
#     if not os.path.exists(dir_name):
#         os.mkdir(dir_name)
#     title_news = []
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     for i in soup.find_all('article'):
#         span = i.find('span', {"class": "c-meta__type"}).text
#         if span == article_type:
#             title = i.find('a', {'data-track-label': "link"}).text
#             name = title.strip().translate(str.maketrans(" ", "_", string.punctuation)) + ".txt"
#             title_news.append(name)
#             link = 'https://www.nature.com' + i.find('a')['href']
#             r2 = requests.get(link)
#             soup2 = BeautifulSoup(r2.content, 'html.parser')
#             article_body = soup2.find('div', {'class': ['c-article-body', 'article-item__body', 'article']})
#
#             if article_body is not None:
#                 body = article_body.text.strip()
#                 file = open(dir_name + '\\' + name, 'w', encoding='UTF-8')
#                 file.write(body)
#                 print('File written')
#                 file.close()
#             else:
#                 print('Empty article body')
#
#             # body = article_body.text.strip()
#             # file = open(dir_name + '\\' + name, 'w', encoding='UTF-8')
#             # file.write(body)
#             # print('File written')
#             # file.close()
#
#
# for n in range(page):
#     dir_name = f'Page_{n + 1}'
#     url = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&Page={n + 1}'
#     save_article_on_page(article_type, dir_name, url)
# print("Saved all articles.")
#
# #Correspondence










