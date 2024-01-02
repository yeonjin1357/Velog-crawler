import json
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree

URL = "https://velog.io/@yeonjin1357"
# ARTICLE_SELECTOR 수정 필요
ARTICLE_SELECTOR = 'body/div/div/div[2]/main/section/div[2]/div[2]'

class Crawler:
    def __init__(self):
        pass

    def get_page(self, url: str):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching the page: HTTP {response.status_code}")
            return None
        return response

    def parse(self, page: requests.Response):
        return bs(page.text, "html.parser")

htmlparser = etree.HTMLParser()

class Article:
    def __init__(self, elem: etree._Element):
        try:
            head = elem.xpath("a[2]")
            if not head:
                head = elem.xpath("a[1]")
            if not head or not head[0].xpath("h2"):
                raise IndexError("Headline element is not found.")
            
            self.href = head[0].attrib.get("href")
            self.headline = head[0].xpath("h2")[0].text.strip()
            self.context = elem.xpath("p")[0].text.strip()
            self.date = elem.xpath("div[2]/span")[0].text.strip()
            self.tags = self.get_tags(elem)
            self.thumbnail = elem.xpath("a[1]/div/img/@src")[0].strip()

        except IndexError as e:
            print(f"An IndexError occurred: {e}")
            print(f"Element HTML: {etree.tostring(elem, pretty_print=True)}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(f"Element HTML: {etree.tostring(elem, pretty_print=True)}")
            raise

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
        return [tag.text.strip() for tag in tag_elements if tag.text]

def get_articles():
    articles = []
    crawler = Crawler()
    req = crawler.get_page(URL)
    
    if not req:
        return articles

    try:
        parsed = crawler.parse(req)
        dom = etree.HTML(str(parsed), htmlparser)
        elems = dom.xpath(ARTICLE_SELECTOR)
        
        if not elems:
            raise ValueError("No articles found. The ARTICLE_SELECTOR might be incorrect.")
        
        for elem in elems:
            try:
                articles.append(Article(elem))
            except Exception as e:
                print(f"Error processing an article: {e}")
    except Exception as e:
        print(f"An error occurred while parsing the page: {e}")

    return articles

def to_json(data, filename='articles.json'):
    with open(filename, 'w+', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    articles_data = get_articles()
    if articles_data:
        article_data = [article.to_dict() for article in articles_data]
        to_json(article_data)
    else:
        print("Failed to retrieve articles.")
