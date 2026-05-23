from playwright.async_api import async_playwright
import asyncio


async def main(): 
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False) 
        page = await browser.new_page()
        await page.goto("https://www.youtube.com/watch?v=iogcY_4xGjo")

        input("Press Enter to close browser...")
        await browser.close()



asyncio.run(main())

