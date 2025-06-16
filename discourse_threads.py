import requests
import json
import os
import time

# Load cookies
with open("cookies.txt", 'r') as file:
    cookie = file.read().strip()

headers = {
    "cookie": cookie
}

# Create output folder for threads
os.makedirs("discourse_threads", exist_ok=True)

all_results = []
seen_topic_ids = set()
page = 1

while True:
    print(f"\n📄 Fetching search results: page {page}")
    url = f"https://discourse.onlinedegree.iitm.ac.in/search.json?q=after%3A2025-01-01%20%23courses%3Atds-kb%20before%3A2025-04-14%20order%3Alatest_topic&page={page}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch page {page}, status code: {response.status_code}")
        break

    data = response.json()

    # Stop when no more posts or topics
    if not data.get("topics") and not data.get("posts"):
        print(f"No more data at page {page}. Done.")
        break

    all_results.append(data)

    # Extract topic IDs from posts and download threads
    for post in data.get("posts", []):
        topic_id = post["topic_id"]
        if topic_id in seen_topic_ids:
            continue
        seen_topic_ids.add(topic_id)

        print(f"Fetching full thread for topic_id: {topic_id}")
        topic_url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_id}.json?track_visit=true&forceLoad=true"
        topic_response = requests.get(topic_url, headers=headers)

        if topic_response.status_code != 200:
            print(f"Failed to fetch thread for topic {topic_id}. Skipping.")
            continue

        thread_data = topic_response.json()
        slug = thread_data["post_stream"]["posts"][0]["topic_slug"]
        filename = f"discourse_threads/{slug}.json"

        with open(filename, "w") as f:
            json.dump(thread_data, f, indent=4)

        print(f"Saved thread to {filename}")
        time.sleep(0.5)  # throttle requests

    page += 1

# Save search results
with open("discourse_all_pages.json", "w") as file:
    json.dump(all_results, file, indent=4)

print("\n All search pages and thread files saved.")

