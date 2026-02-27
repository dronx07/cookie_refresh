import json
from seleniumbase import SB

SELLER_URL = "https://sellercentral-europe.amazon.com/"
AMAZON_URL = "https://www.amazon.fr/"

def get_cookie_string(sb):
    return sb.driver.get_cookie_string()

def fetch_cookies():
    with SB(headless=False, uc=True) as sb:
        sb.open(SELLER_URL)
        sb.sleep(30)
        seller_cookie = get_cookie_string(sb)

        sb.open(AMAZON_URL)
        sb.sleep(30)
        amazon_cookie = get_cookie_string(sb)

        return seller_cookie, amazon_cookie

def main():
    q_seller_cookie, q_amazon_cookie = fetch_cookies()

    data = {
        "amazon": q_amazon_cookie,
        "seller": q_seller_cookie
    }

    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
