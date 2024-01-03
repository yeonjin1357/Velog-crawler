import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from pyvirtualdisplay import Display

# 가상 디스플레이 설정
display = Display(visible=0, size=(1920, 1080))  
display.start()

# ChromeDriver 자동 설치
chromedriver_autoinstaller.install()

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--remote-debugging-port=9222")

# WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)
URL = "https://velog.io/@yeonjin1357"
driver.get(URL)

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

def get_articles(driver):
    articles = []
    article_elements = driver.find_elements(By.CSS_SELECTOR, "div[class^='FlatPostCard_block__']")
    for element in article_elements:
        articles.append(Article(element))
    return articles

def to_json(data):
    with open('articles.json', 'w+', encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    try:
        articles = get_articles(driver)
        article_data = [article.to_dict() for article in articles]
        to_json(article_data)
    except Exception as e:
        print("오류 발생:", e)
    finally:
        driver.quit()
        display.stop()
