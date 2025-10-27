from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import requests

app = Flask(__name__)
CORS(app)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
CSV_PATH = "C:/Users/USER/OneDrive/Documents/mtai/Math-Tutor/backend/data/question.csv"



# Load dataset if exists
if os.path.exists(CSV_PATH):
    dataset = pd.read_csv(CSV_PATH)
else:
    dataset = pd.DataFrame(columns=["id", "question", "answer", "difficulty", "explanation"])

# Student performance stats
student_stats = {
    "score": 0,
    "total": 0,
    "correct": 0,
    "current_difficulty": 1
}

@app.route("/")
def home():
    return "✅ MathMentor AI Backend Running"

# 📥 Get Question
@app.route("/get_question", methods=["GET"])
def get_question():
    difficulty = student_stats["current_difficulty"]
    topic = request.args.get("topic", None)

    filtered = dataset
    if topic:
        filtered = filtered[filtered["topic"].str.lower() == topic.lower()]
    if not filtered.empty:
        filtered = filtered[filtered["difficulty"] == difficulty]

    if filtered.empty:
        filtered = dataset  # fallback to any question

    q = filtered.sample(1).iloc[0]
    return jsonify({
        "id": int(q["id"]),
        "question": q["question"],
        "answer": str(q["answer"]),
        "difficulty": int(q["difficulty"]),
        "explanation": q["explanation"],
        "topic": q["topic"]
    })

# 📤 Submit Answer
@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    global student_stats
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

    # 🧠 Difficulty Logic
    if accuracy > 80 and student_stats["current_difficulty"] < 3:
        student_stats["current_difficulty"] += 1
    elif accuracy < 50 and student_stats["current_difficulty"] > 1:
        student_stats["current_difficulty"] -= 1

    return jsonify({
        "result": result,
        "score": student_stats["score"],
        "accuracy": accuracy,
        "next_difficulty": student_stats["current_difficulty"],
        "explanation": explanation
    })

# 📁 Upload CSV
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if not file or not file.filename.endswith(".csv"):
        return jsonify({"message": "❌ Please upload a valid CSV file!"})

    file.save(CSV_PATH)
    global dataset
    dataset = pd.read_csv(CSV_PATH)
    return jsonify({"message": "✅ CSV uploaded successfully!"})

# 🌐 Download CSV from URL
@app.route("/download_questions", methods=["POST"])
def download_questions():
    url = request.json.get("url")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(CSV_PATH, "wb") as f:
                f.write(response.content)
            global dataset
            dataset = pd.read_csv(CSV_PATH)
            return jsonify({"message": "✅ Questions downloaded successfully!"})
        else:
            return jsonify({"message": "❌ Failed to download file. Check the URL!"})
    except Exception as e:
        return jsonify({"message": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
