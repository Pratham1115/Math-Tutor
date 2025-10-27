from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load dataset
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "questions.csv")
dataset = pd.read_csv(CSV_PATH)

# Track simple student stats
student_stats = {
    "score": 0,
    "total": 0,
    "correct": 0,
    "current_difficulty": 1
}

@app.route("/")
def home():
    return "✅ MathMentor AI Backend Running"

@app.route("/get_question", methods=["GET"])
def get_question():
    if dataset.empty:
        return jsonify({"question": "No questions available."})

    q = dataset.sample(1).iloc[0]
    return jsonify({
        "id": int(q["id"]),
        "question": q["question"],
        "answer": str(q["answer"]),
        "difficulty": 1,
        "explanation": q.get("explanation", "No explanation available.")
    })


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    student_answer = str(data.get("student_answer", "")).strip()
    correct_answer = str(data.get("correct_answer", "")).strip()
    qid = data.get("id")

    student_stats["total"] += 1

    question = dataset[dataset["id"] == qid]
    explanation = question.iloc[0]["explanation"] if not question.empty else "No explanation available."

    if student_answer == correct_answer:
        student_stats["correct"] += 1
        student_stats["score"] += 1
        result = "✅ Correct!"
    else:
        student_stats["score"] -= 1
        result = "❌ Incorrect."

    accuracy = round((student_stats["correct"] / student_stats["total"]) * 100, 2)

    return jsonify({
        "result": result,
        "score": student_stats["score"],
        "accuracy": accuracy,
        "next_difficulty": student_stats["current_difficulty"],
        "explanation": explanation
    })

if __name__ == "__main__":
    app.run(debug=True)
