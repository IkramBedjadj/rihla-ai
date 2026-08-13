from flask import Flask, render_template, request, jsonify
from supervisor_agent import get_supervisor_response  # ← بدل search_agent



app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    data = request.get_json()

    question = data["question"]

    answer = get_supervisor_response(question)  # ← بدل get_response(question, SYSTEM_PROMPT)

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True)