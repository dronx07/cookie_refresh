import json
import asyncio
from seleniumbase import SB
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

load_dotenv()

SELLER_URL = "https://sellercentral-europe.amazon.com/"
AMAZON_URL = "https://www.amazon.fr/"


def get_cookie_string(sb):
    return sb.driver.get_cookie_string()


def fetch_amazon_cookies():
    with SB(headless=False, uc=True) as sb:
        sb.open(SELLER_URL)
        sb.sleep(30)
        seller_cookie = get_cookie_string(sb)

        sb.open(AMAZON_URL)
        sb.sleep(30)
        amazon_cookie = get_cookie_string(sb)

        return seller_cookie, amazon_cookie


class SASLogin:
    def __init__(self, email: str, password: str, headless: bool = True):
        self.login_url = "https://sas.selleramp.com/site/login"
        self.email = email
        self.password = password
        self.headless = headless

    async def login(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.headless,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(self.login_url, wait_until="load")
            await page.fill("input[name='LoginForm[email]']", self.email)
            await page.fill("input[name='LoginForm[password]']", self.password)
            await page.click("button[type='submit']")
            await page.wait_for_load_state("load")
            await asyncio.sleep(30)

            cookies = await context.cookies()
            await browser.close()

            return cookies


async def main():
    seller_cookie, amazon_cookie = fetch_amazon_cookies()
    sas = SASLogin(
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        headless=False
    )
    sas_cookies = await sas.login()
    data = {
        "amazon": amazon_cookie,
        "seller_central": seller_cookie,
        "sas": sas_cookies
    }

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
