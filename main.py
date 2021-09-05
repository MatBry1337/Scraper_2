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











