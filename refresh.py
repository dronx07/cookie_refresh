import json
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

SELLER_URL = "https://sellercentral-europe.amazon.com/"
AMAZON_URL = "https://www.amazon.fr/"
SAS_LOGIN_URL = "https://sas.selleramp.com/site/login"

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def fetch_amazon_cookies(p):
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(AMAZON_URL, wait_until="load")
    cookies = context.cookies()
    cookie_string = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
    context.close()
    browser.close()
    return cookie_string


def fetch_seller_cookies(p):
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(SELLER_URL, wait_until="load")
    cookies = context.cookies()
    cookie_string = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
    context.close()
    browser.close()
    return cookie_string


def fetch_sas_cookies(p):
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(SAS_LOGIN_URL, wait_until="load")
    page.fill("input[name='LoginForm[email]']", EMAIL)
    page.fill("input[name='LoginForm[password]']", PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_load_state("load")
    cookies = context.cookies()
    context.close()
    browser.close()
    return cookies


def main():
    with sync_playwright() as p:
        amazon_cookie = fetch_amazon_cookies(p)
        seller_cookie = fetch_seller_cookies(p)
        sas_cookies = fetch_sas_cookies(p)

    data = {
        "amazon": amazon_cookie,
        "seller": seller_cookie,
        "sas": sas_cookies
    }

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
