import requests

url = "https://www.wikipedia.org/"
headers = {
    "User-Agent": "MyPythonApp/1.0 (https://example.com)"
}
r = requests.get(url, headers=headers)
print(r.status_code)
print(r.text[:500])