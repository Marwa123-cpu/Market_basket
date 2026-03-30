import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_food_categories():
    """
    Scrapes a list of common food categories to augment the grocery dataset.
    This fulfills the Web Scraping (BeautifulSoup) requirement.
    """
    url = "https://en.wikipedia.org/wiki/List_of_food_groups"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # We look for all 'headlines' (h2) which represent main food groups
        # (e.g., Dairy, Meat, Vegetables)
        categories = [head.text.strip().replace('[edit]', '') for head in soup.find_all('h2') if len(head.text) > 2]
        
        # Filter out Wikipedia junk headers
        cleaned_categories = [cat for cat in categories if cat not in ['Contents', 'See also', 'References', 'External links']]
        
        return pd.DataFrame(cleaned_categories, columns=['Scraped_Category'])
    except Exception as e:
        print(f"Scraping Error: {e}")
        return None

print("Scraper Module Loaded Successfully.")