import json
import time
import re
from datetime import datetime, timedelta
import pytz
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

def parse_date(date_str):
    # 현재 시간 기준
    now = datetime.now()
    
    # "약 5시간 전"과 같은 상대 시간 표현 처리
    hours_ago_match = re.search(r"약 (\d+)시간 전", date_str)
    if hours_ago_match:
        hours_ago = int(hours_ago_match.group(1))
        # 현재 시간에서 시간을 뺍니다.
        corrected_time = now - timedelta(hours=hours_ago)
        return corrected_time.strftime('%Y-%m-%d %H:%M')
    
    # "2023년 3월 26일"과 같은 절대 시간 표현 처리
    absolute_time_match = re.match(r"(\d+)년 (\d+)월 (\d+)일", date_str)
    if absolute_time_match:
        year, month, day = absolute_time_match.groups()
        # datetime 객체로 변환
        corrected_time = datetime(int(year), int(month), int(day))
        return corrected_time.strftime('%Y-%m-%d')
    
    # 시간 정보를 변환할 수 없는 경우 원본 문자열 반환
    return date_str

class Article:
    def __init__(self, web_element):
        try:
            self.href = web_element.find_element(By.XPATH, "a[1]").get_attribute("href")
        except Exception as e:
            self.href = None
            print(f"Error retrieving href: {e}")

        try:
            self.thumbnail = web_element.find_element(By.XPATH, "a[1]/img").get_attribute("src")
        except Exception as e:
            self.thumbnail = None
            print(f"Error retrieving thumbnail: {e}")

        try:
            self.headline = web_element.find_element(By.XPATH, "a[2]/h2").text
        except Exception as e:
            self.headline = None
            print(f"Error retrieving headline: {e}")

        try:
            self.context = web_element.find_element(By.XPATH, "p").text
        except Exception as e:
            self.context = None
            print(f"Error retrieving context: {e}")

        try:
            self.date = web_element.find_element(By.XPATH, "div[2]/span[1]").text
        except Exception as e:
            self.date = None
            print(f"Error retrieving date: {e}")

        try:
            self.tags = [tag.text for tag in web_element.find_elements(By.XPATH, "div[1]/a")]
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
    article_elements = driver.find_elements(By.XPATH, "/html/body/div/div[2]/div[2]/main/div/section/div[2]/div[2]/div")
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
