import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# 1. Jumia Scraping Function
def get_jumia_category(item_name):
    url = f"https://www.jumia.com.eg/catalog/?q={item_name.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Identify category from the first product listing
        first_product = soup.find('article', {'class': 'prd'})
        if first_product and 'data-category' in first_product.attrs:
            return first_product['data-category'].split('/')[0]
        return "General Grocery"
    except:
        return "Not Found"

# 2. Seoudi Scraping Function
def get_seoudi_category(item_name):
    url = f"https://www.seoudi.com/search?q={item_name.replace(' ', '%20')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Identify category from the product badge
        category_tag = soup.find('span', {'class': 'product-category'})
        if category_tag:
            return category_tag.get_text().strip()
        return "Supermarket"
    except:
        return "Not Found"

# --- EXECUTION ---
items_to_test = ["whole milk", "rolls/buns", "sausage"]
jumia_list = []
seoudi_list = []

print("⏳ Scraping in progress... Please wait.\n")

for item in items_to_test:
    jumia_list.append((item, get_jumia_category(item)))
    seoudi_list.append((item, get_seoudi_category(item)))
    time.sleep(1) # Ethical delay

# --- OUTPUT RESULTS SEPARATELY ---

print("========================================")
print("📌 RESULTS FROM: JUMIA EGYPT")
print("========================================")
for item, cat in jumia_list:
    print(f"Item: {item.ljust(15)} | Category: {cat}")

print("\n" + "========================================")
print("📌 RESULTS FROM: SEOUDI MARKET")
print("========================================")
for item, cat in seoudi_list:
    print(f"Item: {item.ljust(15)} | Category: {cat}")