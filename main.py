from flask import Flask, request
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
from notion_sync import add_to_notion

app = Flask(__name__)

# Переменные среды
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OWNER_CHAT_ID = os.environ.get("OWNER_CHAT_ID")
WEBHOOK_URL = f"https://mikhail-bot.onrender.com/{BOT_TOKEN}"

# Установка Webhook при старте
def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": WEBHOOK_URL})
    print("Webhook set:", response.text)

# Автоматическое сообщение по расписанию
def send_scheduled_message():
    text = "Привет, Михаил Миллиардер! Время проверить фокус. Что ты сейчас делаешь?"
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": OWNER_CHAT_ID, "text": text}
    )

# Настройка планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(send_scheduled_message, "cron", hour=16, minute=30)  # Пример: 16:30
scheduler.add_job(send_scheduled_message, "cron", hour=7, minute=30)   # Утро
scheduler.add_job(send_scheduled_message, "cron", hour=21, minute=30)  # Вечер
scheduler.start()

# Обработка входящих сообщений из Telegram
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

if __name__ == "__main__":
    set_webhook()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
