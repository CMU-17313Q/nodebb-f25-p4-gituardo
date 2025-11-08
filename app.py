import os

from flask import Flask
from flask import request, jsonify
from src.translator import translate_content

app = Flask(__name__)

@app.route("/")
def translator():
    content = request.args.get("content", default = "", type = str)
    is_english, translated_content = translate_content(content)
    return jsonify({
        "is_english": is_english,
        "translated_content": translated_content,
    })
@app.route("/translate", methods=["POST"])
def hardcoded_translate():
    data = request.get_json()
    text = data.get("text", "") if data else ""
    # For P4A, we return a dummy translation response
    return jsonify({
        "translated": "Hello, this is a hardcoded translation for P4A",
        "is_english": False
    }), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
