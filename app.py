from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAI klient
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")
    if not question:
        return jsonify({"answer": "Palun esita küsimus."})

    # GPT-4o päring
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sa oled abivalmis Tallinna Linnavalitsuse sisekontrolöri teenistuse jurist, kes vastab ainult korruptsioonialaste dokumentide põhjal mis on kaasa lisatud."},
            {"role": "user", "content": f"Küsimus: {question}"}
        ]
    )
    answer = response.choices[0].message.content.strip()
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
