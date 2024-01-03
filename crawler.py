import json
import time
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
        try:
            self.href = web_element.find_element(By.XPATH, "/a[1]").get_attribute("href")
        except Exception as e:
            self.href = None
            print(f"Error retrieving href: {e}")

        try:
            self.thumbnail = web_element.find_element(By.XPATH, "/a[1]/img").get_attribute("src")
        except Exception as e:
            self.thumbnail = None
            print(f"Error retrieving thumbnail: {e}")

        try:
            self.headline = web_element.find_element(By.XPATH, "/a[2]/h2").text
        except Exception as e:
            self.headline = None
            print(f"Error retrieving headline: {e}")

        try:
            self.context = web_element.find_element(By.XPATH, "/p").text
        except Exception as e:
            self.context = None
            print(f"Error retrieving context: {e}")

        try:
            self.date = web_element.find_element(By.XPATH, "/div[2]/span[1]").text
        except Exception as e:
            self.date = None
            print(f"Error retrieving date: {e}")

        try:
            self.tags = [tag.text for tag in web_element.find_elements(By.XPATH, "/div[1]/a")]
        except Exception as e:
            self.tags = []
            print(f"Error retrieving tags: {e}")

    def to_dict(self):
        return {
            "href": self.href,
            "headline": self.headline,
            "context": self.context,
            "date": self.date,
            "tags": self.tags,
            "thumbnail": self.thumbnail,
        }

def get_articles(driver):
    articles = []
    time.sleep(3)  # 3초간 대기
    article_elements = driver.find_elements(By.XPATH, "/html/body/div/div[1]/div[2]/main/section/div[2]/div[2]/div")
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
