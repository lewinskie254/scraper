# First run: pip install playwright
# Then run: playwright install

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    # Launch a headless browser
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Go to the url
    url = 'https://timesjobs.com/job-search?keywords=python&location=&experience=&refreshed=true'
    page.goto(url)
    
    # Explicitly wait for the JavaScript to finish rendering the job layout cards
    # You would replace '.job-card-class' with whatever the actual container class is
    print("----waiting to load card -----------")
    page.wait_for_selector('.srp-card', timeout=10000)    
    # Now that the page is fully populated with data, grab the fully rendered HTML
    html_content = page.content()
    browser.close()

# Now Beautiful Soup can see everything perfectly!
soup = BeautifulSoup(html_content, 'lxml')
print(soup.find_all('div', class_='srp-card'))