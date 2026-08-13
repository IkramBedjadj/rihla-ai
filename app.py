from flask import Flask, render_template, request, jsonify
from supervisor_agent import get_supervisor_response 



app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    data = request.get_json()

    question = data["question"]

    answer = get_supervisor_response(question)  

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True)
