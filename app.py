import os
from flask import Flask, jsonify, request, send_from_directory
import requests

app = Flask(__name__, static_folder=".")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.post("/api/chat")
def chat():
    if not GEMINI_API_KEY:
        return jsonify(error="Set GEMINI_API_KEY in your server environment."), 503
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    contents = []
    for item in messages[-16:]:
        role = "model" if item.get("role") == "model" else "user"
        text = str(item.get("text", ""))[:12000]
        if text.strip():
            contents.append({"role": role, "parts": [{"text": text}]})
    if not contents:
        return jsonify(error="Please enter a message."), 400
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    try:
        response = requests.post(
            url,
            params={"key": GEMINI_API_KEY},
            json={
                "system_instruction": {"parts": [{"text": "You are YellowBot, a helpful, creative assistant created by Rohans Web. Give clear, useful answers. For code, provide complete working examples and explain where files belong. Never claim to have changed external files unless a tool actually did so."}]},
                "contents": contents,
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
            },
            timeout=45,
        )
        response.raise_for_status()
        result = response.json()
        reply = "".join(part.get("text", "") for part in result["candidates"][0]["content"]["parts"])
        return jsonify(reply=reply)
    except requests.RequestException:
        return jsonify(error="The AI provider request failed. Check the API key, model name and server logs."), 502
    except (KeyError, IndexError, TypeError):
        return jsonify(error="The AI provider returned an unexpected response."), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
