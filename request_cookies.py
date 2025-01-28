import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import json

# URLs to scrape cookies from
urls = [
    "https://www.carvana.com",
    "https://www.cars.com",
    "https://www.autotrader.com",
    "https://www.carmax.com",
    "https://www.edmunds.com",
    "https://www.vroom.com",
    "https://www.truecar.com",
    "https://www.shift.com",
    "https://www.tesla.com",
    "https://www.gilchristautomotive.com",
]

# Retry strategy for requests
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[403, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"],  # Updated parameter
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

# Selenium setup
def setup_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    try:
        service = Service("D:\DEV\Websites\chromedriver.exe")  # Replace with the path to chromedriver.exe
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except WebDriverException as e:
        print(f"Error initializing Selenium WebDriver: {e}")
        return None

# Fetch cookies using requests and Selenium fallback
cookies_combined = {}
failed_websites = []

for url in urls:
    print(f"Fetching cookies for {url}...")
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        cookies_combined[url] = requests.utils.dict_from_cookiejar(response.cookies)
        print(f"Cookies for {url}: {cookies_combined[url]}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch cookies for {url}: {e}")
        print(f"Falling back to Selenium for {url}...")

        # Selenium fallback
        driver = setup_selenium_driver()
        if driver:
            try:
                driver.get(url)
                selenium_cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
                cookies_combined[url] = selenium_cookies
                print(f"Cookies for {url} using Selenium: {selenium_cookies}")
            except Exception as se:
                print(f"Failed to fetch cookies for {url} using Selenium: {se}")
                failed_websites.append(url)
            finally:
                driver.quit()
        else:
            failed_websites.append(url)

# Save cookies to JSON files
with open("cookies_combined.json", "w") as cookies_file:
    json.dump(cookies_combined, cookies_file, indent=4)
print("Cookies saved to cookies_combined.json.")

with open("failed_websites.json", "w") as failed_file:
    json.dump(failed_websites, failed_file, indent=4)
print("Failed websites saved to failed_websites.json.")
