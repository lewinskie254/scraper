import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    url = 'https://timesjobs.com/job-search?keywords=python&location=&experience=&refreshed=true'
    page.goto(url)
    
    print("----waiting to load card -----------")
    page.wait_for_selector('.srp-card', timeout=10000)    
    html_content = page.content()
    browser.close()

soup = BeautifulSoup(html_content, "lxml")

job_cards = soup.find_all("div", class_="srp-card")
job_listings = []

for card in job_cards:

    title_tag = card.find("h2")
    job_title = title_tag.text.strip() if title_tag else "No Title"

    meta_container = card.select_one(".w-\\[85\\%\\] div.text-xs")
    company_name = "No Company"
    posted_date = "No Date"

    if meta_container:
        spans = meta_container.find_all("span")
        if len(spans) >= 2:
            company_name = spans[0].text.strip()
            posted_date = spans[1].text.replace("Posted on:", "").strip()

    desc_tag = card.find("div", class_="rtd-content")
    description = desc_tag.text.strip() if desc_tag else "No Description"

    skill_tags = card.find_all("span", class_="skill-tag")
    skills = [
        tag.get("title").strip()
        for tag in skill_tags
        if tag.get("title") and not tag.text.startswith("+")
    ]

    footer_spans = card.select(".block.md\\:flex span.font-semibold")
    location = "No Location"
    experience = "No Experience"

    if len(footer_spans) >= 2:
        location = footer_spans[0].text.strip()
        experience = footer_spans[1].text.strip()

    link_tag = card.find("a", target="_blank")
    job_url = link_tag.get("href") if link_tag else "No URL"

    job_data = {
        "title": job_title,
        "company": company_name,
        "date_posted": posted_date,
        "location": location,
        "experience_required": experience,
        "skills": skills,
        "summary": description,
        "link": job_url,
    }

    job_listings.append(job_data)

print(json.dumps(job_listings, indent=4))