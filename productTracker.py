import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Constant Variables
URL = "https://ado-shop.com/products/tyjt59012"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
ALERT_FILE = "last_alert.txt"
ALERT_COOLDOWN_MINUTES = 15

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
            last_alert_time = get_last_alert_time()
            now = datetime.now()

            if not last_alert_time or now - last_alert_time > timedelta(minutes=ALERT_COOLDOWN_MINUTES):
                print("[ALERT] Item may be back in stock! Sending alert...")
                send_telegram_notification()
                save_alert_time()
            else:
                print("[INFO] Item may be in stock, but last alert was sent recently. Skipping.")
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

def get_last_alert_time():
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "r") as f:
            try:
                return datetime.fromisoformat(f.read().strip())
            except ValueError:
                return None
    return None

def save_alert_time():
    with open(ALERT_FILE, "w") as f:
        f.write(datetime.now().isoformat())

# Run once (Render will schedule this hourly)
if __name__ == "__main__":
    is_item_available()
