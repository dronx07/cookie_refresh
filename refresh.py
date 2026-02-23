import asyncio
import json
from playwright.async_api import async_playwright


AMAZON_URL = "https://sellercentral-europe.amazon.com/"
ROCKET_URL = "https://www.rocketsource.io/ean-to-asin"


async def get_cookie_string(context):
    cookies = await context.cookies()
    return "; ".join(
        f"{cookie['name']}={cookie['value']}"
        for cookie in cookies
        if cookie.get("name") and cookie.get("value")
    )


async def fetch_site_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context()
        page = await context.new_page()

        # Amazon
        await page.goto(AMAZON_URL, wait_until="load")
        amazon_cookie = await get_cookie_string(context)

        # RocketSource
        await page.goto(ROCKET_URL, wait_until="load")
        rocket_cookie = await get_cookie_string(context)

        await browser.close()

        return amazon_cookie, rocket_cookie


async def main():
    amazon_cookie, rocket_cookie = await fetch_site_cookies()

    data = {
        "qogita": {
            "amazon_cookie": amazon_cookie,
            "rocket_source_cookie": rocket_cookie
        },
        "eany": {
            "amazon_cookie": amazon_cookie,
            "rocket_source_cookie": rocket_cookie
        }
    }

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
