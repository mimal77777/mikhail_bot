import requests

NOTION_API_KEY = "YOUR_NOTION_API_KEY"
DATABASE_ID = "YOUR_DATABASE_ID"

def add_to_notion(message):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    data = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": message
                        }
                    }
                ]
            }
        }
    }
    requests.post(url, json=data, headers=headers)
