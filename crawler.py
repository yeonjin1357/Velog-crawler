import json
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree

URL = "https://velog.io/@yeonjin1357"
ARTICLE_SELECTOR = '//*[@id="html"]/body/div/div[1]/div[2]/main/section/div[2]/div[2]'

class Crawler:
    def __init__(self):
        pass

    def get_page(self, url: str):
        return requests.get(url)

    def parse(self, page: requests.Response):
        return bs(page.text, "html.parser")

htmlparser = etree.HTMLParser()

class Article:
    href: str
    headline: str
    context: str
    date: str
    tags: list[str]
    thumbnail: str
    comments: int
    hearts: int

    def to_dict(self):
        data = {
            "href": self.href,
            "headline": self.headline,
            "context": self.context,
            "date": self.date,
            "tags": self.tags,
            "thumbnail": self.thumbnail,
            "comments": self.comments,
            "hearts": self.hearts
        }
        return data

    def __init__(self, elem: etree._Element):
        self.href = elem.xpath("a[1]/@href")[0]
        self.thumbnail = elem.xpath("a[1]/img/@src")[0]
        self.headline = elem.xpath("a[2]/h2/text()")[0]
        self.context = elem.xpath("p/text()")[0]
        self.date = elem.xpath("div[2]/span/text()")[0]
        self.tags = [tag.text for tag in elem.xpath("div[1]/a")]
        self.comments = int(elem.xpath("div[2]/div/span[1]/text()")[0])
        self.hearts = int(elem.xpath("div[2]/div/span[3]/text()")[0])

def get_articles():
    articles = []
    crawler = Crawler()
    req = crawler.get_page(URL)
    parsed = crawler.parse(req)
    dom = etree.HTML(str(parsed), htmlparser)
    elems = dom.xpath(ARTICLE_SELECTOR)
    for elem in elems:
        articles.append(Article(elem))
    return articles

def to_json(data):
    with open('articles.json', 'w+', encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    articles = get_articles()
    article_data = [article.to_dict() for article in articles]
    to_json(article_data)
