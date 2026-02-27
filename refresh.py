import os
import json
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

SELLER_URL = "https://sellercentral-europe.amazon.com/"
AMAZON_URL = "https://www.amazon.fr/"
SAS_URL = "https://sas.selleramp.com/site/login"


async def fetch_cookies(page, url, wait_time=30):
    """Open page, wait for manual login, return cookies as string."""
    await page.goto(url)
    print(f"Please login manually on {url}...")
    await asyncio.sleep(wait_time)
    cookies = await page.context.cookies()
    cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    return cookie_string


class SASLogin:
    """Automated SAS login using Playwright."""
    def __init__(self, email: str, password: str, headless: bool = True):
        self.email = email
        self.password = password
        self.headless = headless

    async def login(self, page):
        await page.goto(SAS_URL)
        await page.fill("input[name='LoginForm[email]']", self.email)
        await page.fill("input[name='LoginForm[password]']", self.password)
        await page.click("button[type='submit']")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(10)
        cookies = await page.context.cookies()
        return cookies


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context()
        page = await context.new_page()

        amazon_cookie = await fetch_cookies(page, AMAZON_URL, wait_time=30)

        seller_cookie = await fetch_cookies(page, SELLER_URL, wait_time=30)

        sas = SASLogin(
            email=os.getenv("EMAIL"),
            password=os.getenv("PASSWORD"),
            headless=False
        )
        sas_cookies = await sas.login(page)

        data = {
            "amazon": amazon_cookie,
            "seller": seller_cookie,
            "sas": sas_cookies
        }

        with open("cookies.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
