from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json 
from urllib.parse import urljoin
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = []
with sync_playwright() as p: 
    browser = p.chromium.launch(headless=False,  slow_mo=500)
    page = browser.new_page()

    page.goto('https://books.toscrape.com/')
    page.wait_for_selector('.col-xs-6', timeout=10000)    
    html_content = page.content()
    soup = BeautifulSoup(html_content, "lxml")

    cards = soup.find_all(class_='col-xs-6')

    for i, card in enumerate(cards): 
        title_div = card.find('h3')
        title = title_div.a.text.strip()
        price_div = card.find('div', class_='product_price')
        price = price_div.find(class_='price_color').text.strip()
        img_div = card.find("div", class_="image_container")
        if not img_div:
            continue

        a_tag = img_div.find("a")
        if not a_tag:
            continue

        href = a_tag.get("href")
        full_url = urljoin("https://books.toscrape.com/", href)

        clean_map = {
            'title' : title, 
            'price' : price, 
            'url' : full_url
        }
        data.append(clean_map)
    browser.close()


print(json.dumps(data, indent=4, ensure_ascii=False))
