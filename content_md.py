import requests
import os
import re
from urllib.parse import urljoin

# Step 1: Base URL and main README
base_url = "https://tds.s-anand.net/2025-01/"
main_md = "_sidebar.md"

# Step 2: Create output directory
output_dir = "tds_content"
os.makedirs(output_dir, exist_ok=True)

# Step 3: Download main _sidebar.md
response = requests.get(urljoin(base_url, main_md))
response.raise_for_status()
main_content = response.text

# Step 4: Save the _sidebar.md file
with open(os.path.join(output_dir, main_md), "w", encoding="utf-8") as f:
    f.write(main_content)

# Step 5: Extract all .md links
md_links = re.findall(r'\(([^)]+\.md)\)', main_content)
md_links = list(set(md_links))  # Remove duplicates

# Step 6: Download and save each .md file with directory structure
for link in md_links:
    file_url = urljoin(base_url, link)
    local_path = os.path.join(output_dir, link)

    try:
        print(f"Downloading: {file_url}")
        r = requests.get(file_url)
        r.raise_for_status()

        # Ensure local directory exists
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Save file with directory structure
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"Saved: {local_path}")
    except Exception as e:
        print(f"Failed to download {link}: {e}")
