# How to send request to update score

import requests

url = "https://tggameehacker-api.ba-students.uz/api/update_score/"

headers = {
    "Content-Type": "application/json"
}

payload = {
    "api_key": "",
    "url": "",
    "score": 10
}

response = requests.post(url, headers=headers, params=payload, )

if response.status_code == 200:
    print("Score updated successfully.")
else:
    print("Error:", response.status_code)