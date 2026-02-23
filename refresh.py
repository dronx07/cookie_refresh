import json
from seleniumbase import SB


AMAZON_URL = "https://sellercentral-europe.amazon.com/"
ROCKET_URL = "https://www.rocketsource.io/ean-to-asin"


def get_cookie_string(sb):
    cookies = sb.driver.get_cookie_string()
    return cookies


def fetch_cookies_q():
    with SB(headless=False, uc=True) as sb:
        sb.open(AMAZON_URL)
        sb.sleep(10)
        amazon_cookie = get_cookie_string(sb)

        sb.open(ROCKET_URL)
        sb.sleep(10)
        rocket_cookie = get_cookie_string(sb)

        return amazon_cookie, rocket_cookie


def fetch_cookies_e():
    with SB(headless=False, uc=True) as sb:
        sb.open(AMAZON_URL)
        sb.sleep(10)
        amazon_cookie = get_cookie_string(sb)

        sb.open(ROCKET_URL)
        sb.sleep(10)
        rocket_cookie = get_cookie_string(sb)

        return amazon_cookie, rocket_cookie


def main():
    q_amazon_cookie, q_rocket_cookie = fetch_cookies_q()
    e_amazon_cookie, e_rocket_cookie = fetch_cookies_e()

    data = {
        "qogita": {
            "amazon_cookie": q_amazon_cookie,
            "rocket_source_cookie": q_rocket_cookie
        },
        "eany": {
            "amazon_cookie": e_amazon_cookie,
            "rocket_source_cookie": e_rocket_cookie
        }
    }

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
