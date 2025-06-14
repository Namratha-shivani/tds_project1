import json
import os

# Load the new JSON file
with open('discourse.json', 'r') as f:
    data = json.load(f)

# Extract new topics
new_topics = data.get("topic_list", {}).get("topics", [])

# Load existing topics if the output file already exists
if os.path.exists('filtered_topics.json'):
    with open('filtered_topics.json', 'r') as f:
        existing_data = json.load(f)
        existing_topics = existing_data.get("topics", [])
else:
    existing_topics = []

# Combine topics (optional: avoid duplicates by ID)
combined = {topic['id']: topic for topic in existing_topics + new_topics}
all_topics = list(combined.values())

# Save the combined topics
with open('filtered_topics.json', 'w') as f:
    json.dump({"topics": all_topics}, f, indent=4)

print(f"{len(new_topics)} new topics added. Total: {len(all_topics)} topics in filtered_topics.json")

