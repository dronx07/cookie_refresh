import json
import os
from dotenv import load_dotenv
from seleniumbase import SB

load_dotenv()

e = os.getenv("EMAIL")
p = os.getenv("PASSWORD")


SELLERAMP_URL = "https://sas.selleramp.com/site/login"
AMAZON_URL = "https://sellercentral-europe.amazon.com/"

def login_selleramp_and_get_cookies(sb, email, password):
    sb.open(SELLERAMP_URL)
    sb.type("input[id='loginform-email']", email)
    sb.type("input[id='loginform-password']", password)
    sb.click("button[type='submit']")
    sb.sleep(15)
    return sb.driver.get_cookie_string()


def open_amazon_and_get_cookies(sb):
    sb.open(AMAZON_URL)
    sb.sleep(15)
    return sb.driver.get_cookie_string()


def fetch_all_cookies(email, password):
    with SB(headless=True, uc=True) as sb:
        selleramp_cookie = login_selleramp_and_get_cookies(sb, email, password)
        amazon_cookie = open_amazon_and_get_cookies(sb)
        return selleramp_cookie, amazon_cookie


def main():
    q_selleramp_cookie, q_amazon_cookie = fetch_all_cookies(e, p)
    e_selleramp_cookie, e_amazon_cookie = fetch_all_cookies(e, p)

    data = {
        "qogita": {
            "selleramp_cookie": q_selleramp_cookie,
            "amazon_cookie": q_amazon_cookie,
        },
        "eany": {
            "selleramp_cookie": e_selleramp_cookie,
            "amazon_cookie": e_amazon_cookie,
        }
    }

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
