## How to send request to update score


```python
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
```

Try it:

```python
python3 tests.py
```    


<br/>


All donations are Greatly Appreciated! 💛 


<a href="https://www.buymeacoffee.com/abdibrokhim" target="_blank"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=abdibrokhim&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

<br/>