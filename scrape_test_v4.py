import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Chrome WebDriver with updated options
driver_path = r"D:\DEV\Websites\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--ignore-gpu-blocklist")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress ffmpeg errors

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Example: Prevent loading of images, audio, or video to optimize
driver.execute_cdp_cmd(
    "Network.setBlockedURLs",
    {"urls": ["*.jpg", "*.png", "*.gif", "*.mp3", "*.mp4", "*.webp", "*.wav"]}
)
driver.execute_cdp_cmd("Network.enable", {})

# Input and output files
input_csv = "sitemap_car_list.csv"
output_csv = "sitemap_car_list_with_price_v4.csv"
error_log_file = "error_log.txt"

# Define URLs to exclude
excluded_urls = [
    "findmycar", "buy-online", "fleet-vehicles", "orderparts", "locations",
    "paymentcalc", "privacy-policy", "customer-reviews", "careers",
    "newspecials", "certified-pre-owned", "searchused", "under-15k", "service",
    "parts", "preapproved", "you-buy-we-drive", "staff", "aboutus", "titanium-certified",
    "toyota-gilchrist-automotive", "carfax-1-owner", "lifted-trucks-for-sale-texas",
    "best-mid-sized-truck-2019", "best-2019-pickup-trucks", "triton-protect-warranty",
    "optimum-collision", "texas-lease-deals", "leasevsfinance", "vehicle-recalls",
    "the-gilchrist-difference", "community-involvement", "en-espanol",
    "black-friday-auto-deals-texas", "gilchrist-in-the-news", "privacy-requests"
]

# Read the sitemap CSV and filter data
cars_data = []
with open(input_csv, "r", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if not any(excluded in row["URL"] for excluded in excluded_urls):
            cars_data.append(row)

print(f"Filtered down to {len(cars_data)} relevant URLs.")

# Open the output CSV for writing
with open(output_csv, "w", newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Car Title", "Location", "VIN", "URL", "Price", "Status"])
    writer.writeheader()

    # Open error log file for writing errors
    with open(error_log_file, "w", encoding="utf-8") as error_log:
        for car in cars_data:
            url = car["URL"]
            try:
                driver.get(url)
                time.sleep(3)  # Wait for the page to load

                # Find the price on the page
                price_element = driver.find_element(By.CLASS_NAME, "vehiclePricingHighlightAmount")
                price = price_element.text.strip() if price_element else "N/A"
                status = "Price Found"
            except Exception as e:
                error_message = f"Error fetching price for {car['Car Title']} ({url}): {e}"
                print(error_message)
                error_log.write(error_message + "\n")
                price = "N/A"
                status = "Error"

            # Add price and status to car data and write to output
            car["Price"] = price
            car["Status"] = status
            writer.writerow(car)
            print(f"Processed: {car['Car Title']} - Price: {price}")

# Close the WebDriver
driver.quit()

print(f"Scraping completed. Results saved to {output_csv}. Errors logged to {error_log_file}.")
