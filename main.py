from flask import Flask, request
import requests
from notion_sync import add_to_notion

app = Flask(__name__)
BOT_TOKEN = "YOUR_BOT_TOKEN"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    message = data["message"].get("text", "")
    add_to_notion(message)
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
        "chat_id": chat_id,
        "text": "Записал! Вдохни, выдохни. Мы всё успеем."
    })
    return {"ok": True}

if __name__ == "__main__":
    app.run(debug=True)
