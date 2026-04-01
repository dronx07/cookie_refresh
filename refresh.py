import json
import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

SELLER_URL = "https://sellercentral-europe.amazon.com/"
AMAZON_URL = "https://www.amazon.fr/"
SAS_LOGIN_URL = "https://sas.selleramp.com/site/login"

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

PROXY = os.getenv("PROXY", None)

proxy={"server": str(PROXY).split("@")[-1], "username": str(PROXY).split("@")[0].replace("http://", "").split(":")[0], "password": str(PROXY).split("@")[0].replace("http://", "").split(":")[-1]}

def launch_browser(playwright):
    return playwright.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )


def fetch_amazon_cookies(playwright, q):
    browser = launch_browser(playwright)
    context = browser.new_context(proxy=proxy)
    page = context.new_page()

    page.goto(AMAZON_URL, wait_until="load", timeout=30000)

    time.sleep(10)

    page.goto(f"https://www.amazon.fr/s?k={q}", wait_until="load", timeout=30000)

    time.sleep(10)

    cookies = context.cookies()
    browser.close()

    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)

    return cookie_str


def fetch_seller_cookies(playwright):
    browser = launch_browser(playwright)
    context = browser.new_context(proxy=proxy)
    page = context.new_page()

    page.goto(SELLER_URL, wait_until="load")
    page.wait_for_timeout(10000)

    cookies = context.cookies()
    browser.close()

    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)

    return cookie_str


def fetch_sas_cookies(playwright):
    browser = launch_browser(playwright)
    context = browser.new_context(proxy=proxy)
    page = context.new_page()

    page.goto(SAS_LOGIN_URL, wait_until="load")

    page.fill("input[name='LoginForm[email]']", EMAIL)
    page.fill("input[name='LoginForm[password]']", PASSWORD)
    page.click("button[type='submit']")

    page.wait_for_load_state("load")

    page.wait_for_timeout(10000)

    cookies = context.cookies()
    browser.close()

    return cookies


def main():
    cookie_sets = {}

    with sync_playwright() as playwright:

        print("Generating cookies set 1...")
        cookie_sets["set1"] = {
            "amazon": fetch_amazon_cookies(playwright, "DVD"),
            "seller": fetch_seller_cookies(playwright)
        }

        time.sleep(10)

        print("Generating cookies set 2...")
        cookie_sets["set2"] = {
            "amazon": fetch_amazon_cookies(playwright, "Jouets"),
            "seller": fetch_seller_cookies(playwright)
        }

        time.sleep(10)

        print("Generating cookies set 3...")
        cookie_sets["set3"] = {
            "amazon": fetch_amazon_cookies(playwright, "Jeux"),
            "seller": fetch_seller_cookies(playwright)
        }

        time.sleep(10)

        print("Generating cookies set 4...")
        cookie_sets["set4"] = {
            "amazon": fetch_amazon_cookies(playwright, "Livres"),
            "seller": fetch_seller_cookies(playwright)
        }

        time.sleep(10)

        print("Generating SAS cookie...")
        cookie_sets["sas"] = fetch_sas_cookies(playwright)

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookie_sets, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
