import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


URL = "https://velog.io/@yeonjin1357"

class Article:
    def __init__(self, web_element):
        self.href = web_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        self.thumbnail = web_element.find_element(By.CSS_SELECTOR, "a > img").get_attribute("src")
        self.headline = web_element.find_element(By.CSS_SELECTOR, "a > h2").text
        self.context = web_element.find_element(By.CSS_SELECTOR, "p").text
        self.date = web_element.find_element(By.CSS_SELECTOR, "div > span").text
        self.tags = [tag.text for tag in web_element.find_elements(By.CSS_SELECTOR, "div > a")]
        # 댓글 수와 하트 수를 추출하는 코드는 페이지에 따라 수정해야 할 수 있습니다.
        self.comments = int(web_element.find_element(By.XPATH, "div[2]/div/span[1]").text)
        self.hearts = int(web_element.find_element(By.XPATH, "div[2]/div/span[3]").text)

    def to_dict(self):
        return {
            "href": self.href,
            "headline": self.headline,
            "context": self.context,
            "date": self.date,
            "tags": self.tags,
            "thumbnail": self.thumbnail,
            "comments": self.comments,
            "hearts": self.hearts
        }

def get_articles():
    # Selenium 옵션 설정
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # webdriver-manager를 사용하여 ChromeDriver를 자동으로 설정
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(URL)
    articles = []
    
    article_elements = driver.find_elements(By.CSS_SELECTOR, "div[class^='FlatPostCard_container__']")  # CSS 선택자는 페이지에 따라 수정해야 합니다.
    for element in article_elements:
        articles.append(Article(element))

    driver.quit()
    return articles

def to_json(data):
    with open('articles.json', 'w+', encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    articles = get_articles()
    article_data = [article.to_dict() for article in articles]
    to_json(article_data)
