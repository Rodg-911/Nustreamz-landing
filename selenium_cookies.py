from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time

# Set up Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(r"D:\path\to\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Websites to scrape
websites = [
    "https://www.carvana.com",
    "https://www.cars.com",
    "https://www.autotrader.com",
    "https://www.carmax.com",
    "https://www.edmunds.com",
    "https://www.vroom.com",
    "https://www.truecar.com",
    "https://www.shift.com",
    "https://www.tesla.com",
    "https://www.gilchristautomotive.com"
]

cookies_data = []

print("Starting selenium-based cookie scraping...")
for website in websites:
    try:
        driver.get(website)
        time.sleep(5)  # Allow JavaScript to load
        cookies = driver.get_cookies()
        cookies_data.append({"website": website, "cookies": cookies})
        print(f"Cookies for {website}: {cookies}")
    except Exception as e:
        print(f"Failed to fetch cookies for {website}: {e}")

# Save cookies to JSON file
with open("cookies_selenium.json", "w") as file:
    json.dump(cookies_data, file, indent=4)

driver.quit()
print("Cookies saved to cookies_selenium.json.")
