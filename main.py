from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
from notion_sync import add_to_notion
from phrases import get_random_phrase  # функция возвращает одну случайную фразу

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("OWNER_CHAT_ID")

# Telegram Webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    message = data["message"].get("text", "")
    add_to_notion(message)
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": "Записал! Вдохни, выдохни. Мы идём вперёд."}
    )
    return {"ok": True}

# Рассылка случайных фраз
def send_random_message():
    if not CHAT_ID or not BOT_TOKEN:
        return
    text = get_random_phrase()
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text}
    )

# Планировщик сообщений раз в час с 6:30 до 23:00
scheduler = BackgroundScheduler(timezone="Europe/Moscow")
for hour in range(6, 24):  # до 23:00 включительно
    scheduler.add_job(send_random_message, "cron", hour=hour, minute=30)

scheduler.start()

# Запуск сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
