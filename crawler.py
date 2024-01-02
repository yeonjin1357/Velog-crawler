import json
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree

URL = "https://velog.io/@yeonjin1357"
# 게시글을 나타내는 더 구체적인 클래스 이름으로 ARTICLE_SELECTOR 수정
ARTICLE_SELECTOR = '//*[contains(@class, "FlatPostCard_block__")]'

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
        # XPath 쿼리를 현재 게시물의 HTML 구조에 맞게 수정
        self.href = elem.xpath(".//a/@href")[0]
        self.headline = elem.xpath(".//h2/text()")[0].strip()
        self.context = elem.xpath(".//p/text()")[0].strip()
        # 날짜 추출을 위한 XPath 수정
        self.date = elem.xpath(".//div[contains(@class, 'FlatPostCard_subInfo__')]/span[1]/text()")[0].strip()
        # 썸네일 이미지 URL 추출을 위한 XPath 수정
        self.thumbnail = elem.xpath(".//img/@src")[0].strip()
        self.tags = self.get_tags(elem)

    def to_dict(self):
        # 모든 속성을 사전으로 변환
        return {
            'href': self.href,
            'headline': self.headline,
            'context': self.context,
            'date': self.date,
            'tags': self.tags,
            'thumbnail': self.thumbnail
        }

    def get_tags(self, elem: etree._Element):
        # 태그 추출을 위한 XPath 수정
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
        # 예외 처리를 추가하여 빈 요소로 인한 오류 방지
        try:
            articles.append(Article(elem))
        except IndexError as e:
            print(f"Error processing element: {e}")
    return articles

def to_json(data, filename='articles.json'):
    with open(filename, 'w+', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    articles_data = get_articles()
    articles_dict = [article.to_dict() for article in articles_data]
    to_json(articles_dict)
