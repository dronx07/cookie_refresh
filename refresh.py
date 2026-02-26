import json
from seleniumbase import SB

SELLER_URL = "https://sellercentral-europe.amazon.com/"
AMAZON_URL = "https://www.amazon.fr/"

def get_cookie_string(sb):
    return sb.driver.get_cookie_string()

def fetch_cookies():
    with SB(headless=False, uc=True) as sb:
        sb.open(SELLER_URL)
        sb.wait_for_ready_state_complete()
        seller_cookie = get_cookie_string(sb)

        sb.open(AMAZON_URL)
        sb.wait_for_ready_state_complete()
        amazon_cookie = get_cookie_string(sb)

        return seller_cookie, amazon_cookie

def main():
    q_seller_cookie, q_amazon_cookie = fetch_cookies()
    e_seller_cookie, e_amazon_cookie = fetch_cookies()

    data = {
        "qogita": {
            "amazon_cookie": q_amazon_cookie,
            "rocket_source_cookie": q_seller_cookie
        },
        "eany": {
            "amazon_cookie": e_amazon_cookie,
            "rocket_source_cookie": e_seller_cookie
        }
    }

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
