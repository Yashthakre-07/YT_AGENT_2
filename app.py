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

    transcript = fetch_transcript(url)

    video_context = transcript

    return jsonify({"message": "Video processed successfully"})


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

    answer = ask_llm(prompt)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)