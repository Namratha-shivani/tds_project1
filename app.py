import os
from flask import Flask, request, jsonify, abort
import openai

app = Flask(__name__)

# Hardcoded API key (replace with your actual token)
openai.api_key = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjEwMDEzNzFAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9._D_oV6c70_Qv5VDjJyFcol8hvlECafcHAKHv6uwB7b8"

# Set the custom OpenAI API base URL
openai.api_base = "https://aipipe.org/openai/v1"

def generate_answer(question, image_base64=None):
    system_prompt = (
        "You are a helpful assistant answering student questions clearly and concisely."
    )

    user_prompt = question
    if image_base64:
        user_prompt += " Note: An image attachment was provided but cannot be analyzed."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )

        answer = response.choices[0].message.content.strip()

    except Exception as e:
        answer = f"Sorry, I encountered an error while processing your question: {str(e)}"

    links = []
    if "tokenizer" in question.lower() or "tokenizer" in answer.lower():
        links.append({
            "url": "https://huggingface.co/docs/tokenizers/python/latest/",
            "text": "Learn more about tokenizers"
        })

    return answer, links

@app.route('/api/', methods=['POST'])
def api():
    if not request.is_json:
        abort(400, description="Content-Type must be application/json")

    data = request.get_json()

    question = data.get('question')
    image_base64 = data.get('image', None)

    if not question:
        abort(400, description="Missing 'question' in request JSON")

    answer, links = generate_answer(question, image_base64)

    return jsonify({
        "answer": answer,
        "links": links
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
