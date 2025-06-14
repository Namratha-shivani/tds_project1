import requests
import json
from datetime import datetime
import time

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

def get_full_thread(slug, topic_id):
    url = f"{BASE_URL}/t/{slug}/{topic_id}.json"
    res = requests.get(url)
    if res.status_code != 200:
        return []
    data = res.json()
    posts = data.get("post_stream", {}).get("posts", [])
    thread = []
    for post in posts:
        thread.append({
            "username": post.get("username"),
            "created_at": post.get("created_at"),
            "content": post.get("cooked")
        })
    return thread

def get_posts_between(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    results = []

    for page in range(1, 50):  # increase page range if needed
        print(f"Scraping page {page}...")
        url = f"{BASE_URL}/latest.json?page={page}"
        res = requests.get(url)
        if res.status_code != 200:
            break

        topics = res.json().get("topic_list", {}).get("topics", [])
        if not topics:
            break

        for topic in topics:
            created = datetime.strptime(topic["created_at"][:10], "%Y-%m-%d")
            if start <= created <= end:
                slug = topic["slug"]
                topic_id = topic["id"]
                print(f"Fetching thread: {slug} ({topic_id})")
                thread = get_full_thread(slug, topic_id)
                topic_url = f"{BASE_URL}/t/{slug}/{topic_id}"
                results.append({
                    "title": topic["title"],
                    "url": topic_url,
                    "created_at": topic["created_at"],
                    "posts": thread
                })
                time.sleep(1)  # polite delay to avoid rate limits

    with open("discourse_data.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    get_posts_between("2025-01-01", "2025-04-14")

