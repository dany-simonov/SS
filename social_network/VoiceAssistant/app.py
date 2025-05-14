# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from core.assistant import AssistantCore

app = Flask(__name__)
assistant = AssistantCore()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listen", methods=["POST"])
def listen():
    response, audio_filename = assistant.listen_and_respond()
    return jsonify({
        "text": response,
        "audio": f"/static/audio/{audio_filename}" if audio_filename else None,
        "history": assistant.get_history()
    })

@app.route("/static/audio/<filename>")
def audio(filename):
    return send_from_directory("static/audio", filename)

if __name__ == "__main__":
    app.run(debug=True)
