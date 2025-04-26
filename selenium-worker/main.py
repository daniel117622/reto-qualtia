import time
from bs4 import BeautifulSoup
import redis
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

r = redis.Redis(host='redis-service', port=6379, decode_responses=True)

# Define the pages and the redis keys
pages = {
    "enlatados"  : "https://www.tiendasjumbo.co/supermercado/despensa/enlatados-y-conservas",
    "harinas"    : "https://www.tiendasjumbo.co/supermercado/despensa/harinas-y-mezclas-para-preparar",
    "chocolates" : "https://www.tiendasjumbo.co/supermercado/despensa/bebida-achocolatada-en-polvo",
    "aceite"     : "https://www.tiendasjumbo.co/supermercado/despensa/aceite"
}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    options=options
)

def fetch_and_store(driver):
    for key, url in pages.items():
        try:
            driver.get(url)

            time.sleep(3)  
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(3)

            page_source = driver.page_source
            
            soup = BeautifulSoup(page_source, "html.parser")
            brand_elements = soup.find_all(class_="vtex-product-summary-2-x-brandName")
            brand_names = [el.get_text(strip=True) for el in brand_elements]

            if brand_names:
                r.delete(key)  
                r.rpush(key, *brand_names)
                print(f"[INFO] Stored brand names list for {key}: {brand_names}")
            else:
                r.set(key, "no element")


        except Exception as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")

try:
    while True:
        fetch_and_store(driver)
        time.sleep(30)  
except Exception as e:
    print(f"[FATAL ERROR] {e}")
finally:
    driver.quit()
