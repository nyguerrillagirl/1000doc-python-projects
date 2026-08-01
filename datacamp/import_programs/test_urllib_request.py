from urllib.request import urlopen, Request

url = "https://www.wikipedia.org/"

headers = {
    "User-Agent": "MyPythonApp/1.0 (https://example.com)"
}
request = Request(url, headers=headers)

response = urlopen(request)

html = response.read()

response.close()

print(f"html:\n {html}")