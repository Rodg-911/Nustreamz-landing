import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Set up Chrome WebDriver
driver_path = r"D:\DEV\Websites\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Input and output files
input_csv = "sitemap_car_list.csv"
output_csv = "sitemap_car_list_with_price_v3.csv"

# Read the sitemap CSV and store data
cars_data = []
with open(input_csv, "r", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cars_data.append(row)

# Open the output CSV for writing
with open(output_csv, "w", newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Car Title", "Location", "VIN", "URL", "Price", "Status"])
    writer.writeheader()

    for car in cars_data:
        url = car["URL"]
        try:
            driver.get(url)
            time.sleep(5)  # Wait for page to load
            
            # Check if the page contains the price element
            price_elements = driver.find_elements(By.CLASS_NAME, "vehiclePricingHighlightAmount")
            if price_elements:
                price = price_elements[0].text.strip()
                status = "Price Found"
            else:
                price = "N/A"
                status = "Not an inventory page or price not found"

        except Exception as e:
            print(f"Error fetching price for {car['Car Title']} at {url}: {e}")
            price = "N/A"
            status = f"Error: {e}"

        # Add price and status to car data and write to output
        car["Price"] = price
        car["Status"] = status
        writer.writerow(car)
        print(f"Fetched: {car['Car Title']} - Price: {price} - Status: {status}")

# Close the WebDriver
driver.quit()

print("Scraping completed and data saved to sitemap_car_list_with_price_v3.csv!")
