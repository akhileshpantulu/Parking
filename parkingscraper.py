import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def scrape_ncp_manchester():
    # 1. Setup - Use a real browser User-Agent to avoid blocks
    url = "https://www.ncp.co.uk/find-a-car-park/car-parks/manchester/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Check if the page loaded correctly
        
        soup = BeautifulSoup(response.text, 'html.parser')
        car_parks = []

        # 2. Extract - Find each car park container
        # NCP typically uses 'car-park-card' or similar classes
        for card in soup.select('.c-car-park-card'):
            try:
                name = card.select_one('.c-car-park-card__title').text.strip()
                
                # NCP often shows "Prices from £X.XX"
                price_text = card.select_one('.c-car-park-card__price-value').text.strip()
                # Clean the price string to get just the number (e.g., "£5.50" -> 5.5)
                price = float(price_text.replace('£', '').replace('from', '').strip())

                car_parks.append({
                    "name": name,
                    "daily_rate": price,
                    "address": card.select_one('.c-car-park-card__address').text.strip(),
                    "operator": "NCP",
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
            except AttributeError:
                continue # Skip if a card is missing data

        # 3. Save - Write to the public folder for the React frontend
        os.makedirs('public', exist_ok=True)
        with open('public/parking_data.json', 'w') as f:
            json.dump({"car_parks": car_parks}, f, indent=2)
        
        print(f"Successfully scraped {len(car_parks)} car parks.")

    except Exception as e:
        print(f"Scraper error: {e}")

if __name__ == "__main__":
    scrape_ncp_manchester()
