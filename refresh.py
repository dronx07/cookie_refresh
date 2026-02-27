import json
import os
from dotenv import load_dotenv
from seleniumbase import SB

load_dotenv()

SELLER_URL = "https://sellercentral-europe.amazon.com/"
AMAZON_URL = "https://www.amazon.fr/"
SAS_LOGIN_URL = "https://sas.selleramp.com/site/login"


def get_cookie_string(sb):
    return sb.driver.get_cookie_string()


def get_cookie_dict_list(sb):
    """Return cookies as list of dicts (like Playwright did)."""
    return sb.driver.get_cookies()


def fetch_amazon_cookies():
    with SB(headless=False, uc=True) as sb:
        sb.open(SELLER_URL)
        sb.sleep(30)
        seller_cookie = get_cookie_string(sb)

        sb.open(AMAZON_URL)
        sb.sleep(30)
        amazon_cookie = get_cookie_string(sb)

        return seller_cookie, amazon_cookie


def fetch_sas_cookies(email, password, headless=False):
    with SB(headless=headless, uc=True) as sb:
        sb.open(SAS_LOGIN_URL)

        sb.type("input[name='LoginForm[email]']", email)
        sb.type("input[name='LoginForm[password]']", password)
        sb.click("button[type='submit']")

        sb.sleep(30)

        sas_cookies = get_cookie_dict_list(sb)

        return sas_cookies


def main():
    seller_cookie, amazon_cookie = fetch_amazon_cookies()

    sas_cookies = fetch_sas_cookies(
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        headless=False
    )

    data = {
        "amazon": amazon_cookie,
        "seller_central": seller_cookie,
        "sas": sas_cookies
    }

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
