import requests
import json

with open("cookies.txt",'r') as file:
    cookie = file.read().strip()

print(cookie)

headers = {
    "cookie":cookie
}

response = requests.get("https://discourse.onlinedegree.iitm.ac.in/directory_items.json?period=yearly&order=likes_received&exclude_groups=&limit=5", headers = headers)

with open("discourse.json",'w') as file:
    json.dump(response.json(), file, indent=4)