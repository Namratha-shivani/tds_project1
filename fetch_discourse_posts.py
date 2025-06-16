import requests
import json

# Load cookies
with open("cookies.txt", 'r') as file:
    cookie = file.read().strip()

headers = {
    "cookie": cookie
}

all_results = []
page = 1

while True:
    print(f"Fetching page {page}...")

    url = f"https://discourse.onlinedegree.iitm.ac.in/search.json?q=after%3A2025-01-01%20%23courses%3Atds-kb%20before%3A2025-04-14%20order%3Alatest_topic&page={page}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch page {page}, status code: {response.status_code}")
        break

    data = response.json()

    # If there are no topics or posts, assume we're done
    if not data.get("topics") and not data.get("posts"):
        print(f"✅ No more results at page {page}. Stopping.")
        break

    all_results.append(data)
    page += 1

# Save everything into one file
with open("discourse_all_pages.json", "w") as file:
    json.dump(all_results, file, indent=4)

print("🎉 All pages saved.")
