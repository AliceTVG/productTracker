import requests
from bs4 import BeautifulSoup

# Constant Variables
URL = "https://ado-shop.com/products/tyjt59012"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_item_available():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the product button
        button = soup.find("button", class_="product-form__submit")

        button_text = button.get_text(strip=True).lower() if button else ""
        is_disabled = button.has_attr("disabled") if button else False

        if "sold out" in button_text or is_disabled:
            print("[INFO] Item is still sold out.")
            return False
        else:
            print("[ALERT] Item may be back in stock!")
            send_telegram_notification()
            return True
        
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch the page: {e}")
        return False
    

def send_telegram_notification():
    TOKEN = "7621293592:AAGLjwBz1E-GXUpaIRb0IdaKwVnmKYI4Szc"
    CHAT_ID = "6602010238"
    message = f"Ado Shop item may be back in stock!\n {URL}"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("[INFO] Telegram notification sent.")
    except requests.RequestException as e:
        print(f"[ERROR] Failed to send Telegram message: {e}")

# Run once (Render will schedule this hourly)
if __name__ == "__main__":
    is_item_available()
