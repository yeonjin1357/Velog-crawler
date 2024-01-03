import requests
from bs4 import BeautifulSoup as bs
from lxml import etree

URL = "https://velog.io/@yeonjin1357"
ARTICLE_SELECTOR = '//*[@id="html"]/body/div/div[1]/div[2]/main/section/div[2]/div[2]/div'

class Crawler:
    def __init__(self):
        pass

    def get_page(self, url: str):
        return requests.get(url)

    def parse(self, page: requests.Response):
        return bs(page.text, "html.parser")

htmlparser = etree.HTMLParser()

def get_articles():
    crawler = Crawler()
    req = crawler.get_page(URL)
    parsed = crawler.parse(req)
    dom = etree.HTML(str(parsed), htmlparser)
    elems = dom.xpath(ARTICLE_SELECTOR)
    for elem in elems:
        print(etree.tostring(elem, pretty_print=True).decode("utf-8"))

if __name__ == "__main__":
    get_articles()
