from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import sys

sys.stdout.reconfigure(encoding='utf-8')

data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()

    page.goto('https://books.toscrape.com/')

    while True:
        page.wait_for_selector('.col-xs-6')

        soup = BeautifulSoup(page.content(), "lxml")
        cards = soup.find_all(class_='col-xs-6')

        for card in cards:
            title = card.find('h3').a.text.strip()
            price = card.find(class_='price_color').text.strip()

            img_div = card.find("div", class_="image_container")
            if not img_div:
                continue

            a_tag = img_div.find("a")
            if not a_tag:
                continue

            href = a_tag.get("href")
            full_url = urljoin("https://books.toscrape.com/", href)

            data.append({
                "title": title,
                "price": price,
                "url": full_url
            })

        with open('books.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        next_btn = page.query_selector("li.next a")

        if not next_btn:
            break

        next_url = next_btn.get_attribute("href")
        page.goto(urljoin(page.url, next_url))

    browser.close()

print('--------Scraping Complete------------')