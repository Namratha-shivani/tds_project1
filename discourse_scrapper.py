import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

def get_posts_between(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    results = []

    for page in range(1, 20):  # tune based on how many pages needed
        url = f"{BASE_URL}/latest.json?page={page}"
        res = requests.get(url)
        topics = res.json().get("topic_list", {}).get("topics", [])
        for topic in topics:
            created = datetime.strptime(topic["created_at"][:10], "%Y-%m-%d")
            if start <= created <= end:
                topic_url = f"{BASE_URL}/t/{topic['slug']}/{topic['id']}"
                results.append({
                    "title": topic["title"],
                    "url": topic_url,
                    "created_at": topic["created_at"]
                })
    with open("discourse_data.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    get_posts_between("2025-01-01", "2025-04-14")
