from flask import Flask, request, jsonify
from inference import generate_answer

app = Flask(__name__)

@app.route("/api/", methods=["POST"])
def answer():
    data = request.get_json()
    question = data.get("question", "")
    image = data.get("image", None)
    if not question:
        return jsonify({"error": "No question provided"}), 400
    try:
        response = generate_answer(question, image)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
