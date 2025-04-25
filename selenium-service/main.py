import time
import redis
from selenium import webdriver

r = redis.Redis(host='redis-service', port=6379, decode_responses=True)

def fetch_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get("https://example.com")
    title = driver.title
    driver.quit()
    return title

while True:
    try:
        data = fetch_data()
        r.set("latest_title", data)
        print(f"[INFO] Wrote to Redis: {data}")
    except Exception as e:
        print(f"[ERROR] {e}")
    time.sleep(30)  # Every 30 seconds
