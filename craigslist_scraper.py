import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://dallas.craigslist.org/search/cta"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_listings(zip_code, radius):
    params = {"postal": zip_code, "search_distance": radius}
    results = []
    page = 0

    while True:
        params["s"] = page  # Craigslist uses 's' for pagination (0, 120, 240...)
        print(f"Fetching page {page // 120 + 1}...")
        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch URL: {BASE_URL} (Status Code: {response.status_code})")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all listings on the page
        listings = soup.find_all("li", class_="cl-static-search-result")
        if not listings:
            print("No listings found on this page.")
            break

        for listing in listings:
            try:
                # Extract car title
                title_tag = listing.find("div", class_="title")
                title = title_tag.text.strip() if title_tag else "N/A"

                # Extract link to detailed listing
                link_tag = listing.find("a")
                detail_link = link_tag["href"] if link_tag else "N/A"

                # Extract price
                price_tag = listing.find("div", class_="price")
                price = price_tag.text.strip() if price_tag else "N/A"

                # Extract location
                location_tag = listing.find("div", class_="location")
                location = location_tag.text.strip() if location_tag else "N/A"

                # Append to results
                results.append({
                    "title": title,
                    "detail_link": detail_link,
                    "price": price,
                    "location": location,
                })
            except Exception as e:
                print(f"Error parsing listing: {e}")

        # Check for next page
        next_button = soup.find("a", class_="button next")
        if not next_button:
            print("No next page found.")
            break

        page += 120  # Increment offset for the next page
        time.sleep(2)  # Rate-limiting to prevent being blocked

    return results

def save_to_csv(data, filename):
    if not data:
        print("No data to save.")
        return
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Saved {len(data)} listings to {filename}")

if __name__ == "__main__":
    zip_code = "75165"
    radius = 50
    print(f"Fetching listings for ZIP {zip_code} within {radius} miles...")
    listings = fetch_listings(zip_code, radius)
    save_to_csv(listings, f"craigslist_{zip_code}_{radius}miles.csv")
