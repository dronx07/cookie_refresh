import os
import json
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

SELLER_URL = "https://sellercentral-europe.amazon.com/"
AMAZON_URL = "https://www.amazon.fr/"
SAS_URL = "https://sas.selleramp.com/site/login"

async def fetch_site_cookies(browser, url, wait_time=30):
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(url)
    print(f"Please login manually on {url}...")
    await asyncio.sleep(wait_time)
    cookies = await context.cookies()
    cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    await context.close()
    return cookie_string

class SASLogin:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    async def login(self, browser):
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(SAS_URL)
        await page.fill("input[name='LoginForm[email]']", self.email)
        await page.fill("input[name='LoginForm[password]']", self.password)
        await page.click("button[type='submit']")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(10)
        cookies = await context.cookies()
        await context.close()
        return cookies

async def main():
    HEADLESS = False
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS, args=["--disable-blink-features=AutomationControlled"])
        amazon_cookie = await fetch_site_cookies(browser, AMAZON_URL, 30)
        seller_cookie = await fetch_site_cookies(browser, SELLER_URL, 30)
        sas = SASLogin(email=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))
        sas_cookies = await sas.login(browser)
        await browser.close()
        data = {
            "amazon": amazon_cookie,
            "seller": seller_cookie,
            "sas": sas_cookies
        }
        with open("cookies.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
