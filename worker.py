import os
import time
import requests
from datetime import datetime
from phrases import get_random_phrase

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, json=payload)
    print("Отправлено:", response.status_code, text)

if __name__ == "__main__":
    while True:
        now = datetime.now()
        if 6 <= now.hour < 23:
            phrase = get_random_phrase()
            send_message(phrase)
        time.sleep(3600)  # Ждём 1 час
