from flask import Flask, request, jsonify, render_template
from transcript import fetch_transcript
from rag_chat import ask_llm

app = Flask(__name__)

video_context = ""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process_video", methods=["POST"])
def process_video():
    global video_context

    data = request.json
    url = data["url"]

    try:
        transcript = fetch_transcript(url)
        video_context = transcript
        return jsonify({"message": "Video processed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat", methods=["POST"])
def chat():
    global video_context

    data = request.json
    question = data["question"]
    language = data.get("language", "english")

    if language == "hindi":
        instruction = "Answer ONLY in Hindi language."

    elif language == "english":
        instruction = "Answer ONLY in English language."

    elif language == "both":
        instruction = "First answer in English, then answer in Hindi."

    else:
        instruction = "Answer in English."

    # limit transcript size to avoid token errors
    context = video_context[:12000]

    prompt = f"""
{instruction}

Use the following YouTube transcript to answer the question.

Transcript:
{context}

Question:
{question}
"""

    try:
        answer = ask_llm(prompt)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
