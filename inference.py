import openai
import json
import base64
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def read_knowledge():
    discourse = json.load(open("discourse_data.json"))
    with open("tds_course_content.txt", "r") as f:
        course = f.read()
    return discourse, course

def generate_answer(question, image=None):
    discourse, course = read_knowledge()

    system_prompt = f"""
You are a helpful TDS virtual TA. You have access to the following knowledge:
1. Course content: {course[:10000]}
2. Discourse references: {[d['title'] for d in discourse]}

Always return JSON with 'answer' and a 'links' field (up to 2 relevant discourse links).
"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": question})

    if image:
        messages.append({
            "role": "user",
            "content": [{"type": "image_url", "image_url": {"url": f"data:image/webp;base64,{image}"}}],
        })

    response = openai.ChatCompletion.create(
        model="gpt-4o",  # or "gpt-3.5-turbo" if using 3.5
        messages=messages,
        temperature=0.2
    )

    answer = response["choices"][0]["message"]["content"]
    links = [{"url": d["url"], "text": d["title"]} for d in discourse[:2]]
    return {"answer": answer, "links": links}
