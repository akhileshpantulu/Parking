import requests
from bs4 import BeautifulSoup
import json
import os

def run_scraper():
    # Example for a specific parking site
    url = "https://www.example-parking-site.com/manchester"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    # Logic to find car parks (you'll customize the tags)
    for item in soup.select('.parking-card'):
        results.append({
            "name": item.select_one('.name').text,
            "daily_rate": float(item.select_one('.price').text.replace('£', '')),
            "address": item.select_one('.address').text
        })
    
    # Save the data to a JSON file that the frontend can see
    with open('public/parking_data.json', 'w') as f:
        json.dump({"car_parks": results}, f)

if __name__ == "__main__":
    run_scraper()
