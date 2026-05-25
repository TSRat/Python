import requests
import json

response = requests.get("https://api.github.com")
print(response.status_code)
print(response.json())

try:
    with open("data.json", "r", encoding = "utf-8") as f:
        txt = json.load(f)
        print(txt["gender"])
except FileNotFoundError:
    print("文件不存在！")
except json.JSONDecodeError:
    print("文件内容不是有效的 JSON！")
        