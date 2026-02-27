import json
import os
from dotenv import load_dotenv
from seleniumbase import SB

load_dotenv()

SELLER_URL = "https://sellercentral-europe.amazon.com/"
AMAZON_URL = "https://www.amazon.fr/"
SAS_LOGIN_URL = "https://sas.selleramp.com/site/login"

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def fetch_all_cookies():
    with SB(headless=False, uc=True) as sb:
        sb.open(AMAZON_URL)
        sb.sleep(30)
        amazon_cookie = sb.driver.get_cookie_string()

        sb.open(SELLER_URL)
        sb.sleep(30)
        seller_cookie = sb.driver.get_cookie_string()

        sb.open(SAS_LOGIN_URL)
        sb.type("input[name='LoginForm[email]']", EMAIL)
        sb.type("input[name='LoginForm[password]']", PASSWORD)
        sb.click("button[type='submit']")
        sb.sleep(30)
        sas_cookies = sb.driver.get_cookies()

        return amazon_cookie, seller_cookie, sas_cookies

def main():
    amazon_cookie, seller_cookie, sas_cookies = fetch_all_cookies()

    data = {
        "amazon": amazon_cookie,
        "seller": seller_cookie,
        "sas": sas_cookies
    }

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
