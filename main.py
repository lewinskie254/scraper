import json
from bs4 import BeautifulSoup

with open("index.html", "r") as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, "lxml")
    book_cards = soup.find_all("div", class_="card")

    book_details = []

    for book in book_cards:
        topic_tag = book.find("span", class_="badge")
        title_tag = book.find("h2", class_="book-title")
        author_tag = book.find("p", class_="author")
        description_tag = book.find("p", class_="description")
        price_tag = book.find("span", class_="price")

        clean_map = {
            "topic": topic_tag.text.strip() if topic_tag else "No Topic",
            "title": title_tag.text.strip() if title_tag else "No Title",
            "author": (
                author_tag.text.replace("By ", "").strip()
                if author_tag
                else "No Author"
            ),
            "description": (
                description_tag.text.strip()
                if description_tag
                else "No Description"
            ),
            "price": price_tag.text.strip() if price_tag else "No Price",
            "category_slug": book.get("data-category", "No Category"),
        }

        book_details.append(clean_map)

pretty_json = json.dumps(book_details, indent=4)
print(pretty_json)