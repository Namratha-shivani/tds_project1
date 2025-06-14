import requests
import json

with open("cookies.txt",'r') as file:
    cookie = file.read().strip()

print(cookie)

headers = {
    "cookie":cookie
}

response = requests.get("https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34/l/latest.json?filter=default&page=3", headers = headers)

with open("discourse.json",'w') as file:
    json.dump(response.json(), file, indent=4)