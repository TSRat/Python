import requests
import json
import os

api_url = "https://api.example.com/chat"
api_key = os.getenv("MY_CHAT_API_KEY", "YOUR_API_KEY")
headers = {
    "Content-type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY",
}
payload = {
    "model": "chat-model",
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}

try:
    response = requests.post(api_url, headers=headers, json=payload, auth=(api_key, ""), timeout=15)
    response.raise_for_status()
    data = response.json()
    print(data)
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as e:
    print(f"An error occurred: {e}")

