from flask import Flask, request, jsonify
import asyncio
from playwright.async_api import async_playwright
import base64

app = Flask(__name__)

# URLs
COURSE_URL = "https://tds.s-anand.net/#/2025-01/"
DISCOURSE_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"

# Global variables
course_data = ""
discourse_data = ""

# Async function to fetch rendered HTML
async def fetch_rendered_text(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(5000)  # Wait 5 sec for JavaScript to load
        content = await page.content()
        text = await page.inner_text("body")
        await browser.close()
        return text

# Fetch content from both sources
def preload_content():
    global course_data, discourse_data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    course_data = loop.run_until_complete(fetch_rendered_text(COURSE_URL))
    discourse_data = loop.run_until_complete(fetch_rendered_text(DISCOURSE_URL))

# Basic answer generator
def answer_question(q):
    q_lower = q.lower()
    if "assignment" in q_lower or "module" in q_lower:
        return course_data[:1000] + "..."  # Return sample content
    elif "doubt" in q_lower or "discuss" in q_lower:
        return discourse_data[:1000] + "..."
    else:
        return "I could not find an exact answer, but please check the course site or Discourse forum."

@app.route("/api/", methods=["POST"])
def answer_api():
    data = request.get_json(force=True)
    question = data.get("question", "")
    attachment = data.get("image")

    if not question:
        return jsonify({"error": "Missing 'question'"}), 400

    if attachment:
        try:
            base64.b64decode(attachment)
        except Exception:
            return jsonify({"error": "Invalid base64 image"}), 400

    response = answer_question(question)
    return jsonify({"answer": response})

if __name__ == "__main__":
    print("Preloading course and forum content...")
    preload_content()
    print("Starting server.")
    app.run(host="0.0.0.0", port=5000)

