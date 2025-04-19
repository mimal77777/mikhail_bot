from flask import Flask, request
import requests
import os
from notion_sync import add_to_notion

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_PATH = f"/{BOT_TOKEN}"


@app.route("/7829368082:AAEI--GfMALMubHeC4oBZhs9FBXQiTJ4v5I", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        message = data["message"].get("text", "")

        # Добавление в Notion
        add_to_notation(message)

        # Ответ пользователю
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "Записал! Вдохни, выдохни. Мы на связи."
            }
        )

    return {"ok": True}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
