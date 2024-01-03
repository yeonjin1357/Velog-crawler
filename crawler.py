import json
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree

URL = "https://velog.io/@yeonjin1357"
ARTICLE_SELECTOR = '//*[@id="html"]/body/div/div[1]/div[2]/main/section/div[2]/div[2]/div[1]'

class Crawler:
    def __init__(self):
        pass

    def get_page(self, url: str):
        return requests.get(url)

    def parse(self, page: requests.Response):
        return bs(page.text, "html.parser")

htmlparser = etree.HTMLParser()

class Article:
    def __init__(self, elem: etree._Element):
        self.href = elem.xpath(".//a/@href")[0]
        self.headline = elem.xpath(".//h2/text()")[0].strip()
        self.context = elem.xpath(".//p/text()")[0].strip()
        self.date = elem.xpath(".//div[contains(@class, 'FlatPostCard_subInfo__')]/span[1]/text()")[0].strip()
        self.thumbnail = elem.xpath(".//img/@src")[0].strip()
        self.tags = self.get_tags(elem)

    def to_dict(self):
        return {
            'href': self.href,
            'headline': self.headline,
            'context': self.context,
            'date': self.date,
            'tags': self.tags,
            'thumbnail': self.thumbnail
        }

    def get_tags(self, elem: etree._Element):
        tag_elements = elem.xpath(".//div[contains(@class, 'FlatPostCard_tagsWrapper__')]/a")
        return [tag.text.strip() for tag in tag_elements]

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

def to_json(data, filename='articles.json'):
    with open(filename, 'w+', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    articles_data = get_articles()
    article_data = [article.to_dict() for article in articles_data]
    to_json(article_data)
