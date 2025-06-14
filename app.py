from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import base64
import re

app = Flask(__name__)

# URLs to fetch data from
COURSE_CONTENT_URL = "https://tds.s-anand.net/#/2025-01/"
DISCOURSE_POSTS_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"

# Global variables to cache content
course_content_text = ""
discourse_posts_text = ""

def fetch_course_content():
    # Fetch the course content page and extract meaningful text
    try:
        res = requests.get(COURSE_CONTENT_URL)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        # Extract visible text, excluding scripts/styles/navigation
        texts = soup.stripped_strings
        filtered_text = []
        for t in texts:
            # Remove navigation or unrelated text by filtering keywords or length
            if len(t) > 20 and not re.search(r"(login|signup|register|menu|search)", t, re.I):
                filtered_text.append(t)
        return "\n".join(filtered_text)

    except Exception as e:
        print(f"Failed to fetch course content: {e}")
        return ""

def fetch_discourse_posts():
    # Fetch the discourse category page and extract text of posts
    try:
        res = requests.get(DISCOURSE_POSTS_URL)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        # The page is dynamic, might not have all posts loaded.
        # Extract all text visible (basic fallback)
        texts = soup.stripped_strings
        filtered_text = []
        for t in texts:
            if len(t) > 20 and not re.search(r"(login|signup|register|menu|search)", t, re.I):
                filtered_text.append(t)
        return "\n".join(filtered_text)

    except Exception as e:
        print(f"Failed to fetch discourse posts: {e}")
        return ""

def answer_question(question):
    # Simple keyword search for demonstration:
    question_lower = question.lower()

    if any(k in question_lower for k in ["course", "content", "topic", "module"]):
        # Search course content
        if course_content_text:
            # Return the first 500 chars that contain a keyword (naive)
            idx = course_content_text.lower().find(question_lower.split()[0])
            if idx != -1:
                snippet = course_content_text[max(0, idx-50):idx+450]
                return f"From course content:\n{snippet}..."
            else:
                return "Course content is available but no exact match found."
        else:
            return "Course content not available currently."

    elif any(k in question_lower for k in ["discourse", "discussion", "posts", "question", "answer"]):
        # Search discourse posts
        if discourse_posts_text:
            idx = discourse_posts_text.lower().find(question_lower.split()[0])
            if idx != -1:
                snippet = discourse_posts_text[max(0, idx-50):idx+450]
                return f"From discourse posts:\n{snippet}..."
            else:
                return "No relevant discourse posts found."
        else:
            return "Discourse posts not available currently."

    else:
        # fallback
        return ("Sorry, I can only answer questions about the TDS course content and discourse posts "
                "for Tools in Data Science course.")

@app.route('/api/', methods=['POST'])
def api():
    global course_content_text, discourse_posts_text
    data = request.get_json(force=True)
    question = data.get("question")
    attachments = data.get("image")  # optional base64 file

    if not question:
        return jsonify({"error": "Missing 'question' field in request"}), 400

    if attachments:
        try:
            _ = base64.b64decode(attachments)
        except Exception:
            return jsonify({"error": "Invalid base64 attachment"}), 400

    # Lazy load content if empty
    if not course_content_text:
        course_content_text = fetch_course_content()
    if not discourse_posts_text:
        discourse_posts_text = fetch_discourse_posts()

    answer = answer_question(question)

    return jsonify({"answer": answer})

if __name__ == "__main__":
    # Preload the content once at startup for faster response
    print("Fetching course content and discourse posts...")
    course_content_text = fetch_course_content()
    discourse_posts_text = fetch_discourse_posts()
    print("Content loaded, starting server.")
    app.run(host="0.0.0.0", port=5000)
