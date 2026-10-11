import os
import re
import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=".")
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite").strip()
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/api/status")
def status():
    return jsonify(configured=bool(API_KEY), provider="Google Gemini", model=MODEL)

def ask_gemini(instructions, prompt, limit=14000):
    if not API_KEY:
        return None, (jsonify(error="Google Gemini is not configured. Add GEMINI_API_KEY to your Render environment variables, then redeploy."), 503)
    payload = {
        "systemInstruction": {"parts": [{"text": instructions}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": limit,
            "temperature": 0.7
        }
    }
    try:
        r = requests.post(
            API_URL.format(model=MODEL),
            headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
            json=payload,
            timeout=180
        )
    except requests.RequestException:
        return None, (jsonify(error="Could not reach Google Gemini. Check the server connection and try again."), 502)
    if r.status_code in (401, 403):
        return None, (jsonify(error="Google Gemini rejected the key. Check GEMINI_API_KEY in Render and make sure the key is enabled for the Gemini API."), 502)
    if r.status_code == 429:
        return None, (jsonify(error="Google Gemini's free-tier rate limit has been reached. Wait for the quota to reset, or check your Google AI Studio usage limits."), 429)
    if not r.ok:
        try:
            message = r.json().get("error", {}).get("message", "Google Gemini request failed.")
        except (ValueError, AttributeError):
            message = "Google Gemini request failed."
        return None, (jsonify(error=str(message)[:500]), 502)
    try:
        data = r.json()
        candidates = data.get("candidates", [])
        parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
        answer = "\n".join(part.get("text", "") for part in parts if isinstance(part, dict)).strip()
        finish_reason = candidates[0].get("finishReason", "") if candidates else ""
    except (ValueError, TypeError, AttributeError, IndexError):
        answer, finish_reason = "", ""
    if not answer:
        if finish_reason == "MAX_TOKENS":
            message = "The AI response reached its output limit. Try a smaller website brief."
        else:
            message = "The AI returned an empty result. Try a shorter request."
        return None, (jsonify(error=message), 502)
    return answer, None

def extract_html(value):
    value = value.strip()
    value = re.sub(r"^\s*```(?:html)?\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s*```\s*$", "", value)
    found = re.search(r"<!doctype html[\s\S]*", value, flags=re.IGNORECASE)
    return found.group(0).strip() if found else value

BASE_INSTRUCTIONS = """You are YellowBot Studio, a senior web designer and front-end engineer. Return one complete standalone HTML document only, beginning with <!doctype html>; no markdown fences or explanation. Put all CSS in style tags and JavaScript in script tags. Build a polished, responsive, accessible website with strong typography, careful spacing, mobile-first layout, hover and focus states, complete example content and useful working interactions. Keep it self-contained with no build tools or required packages. Do not create fake non-working buttons. Forms must have front-end validation and clearly state if they are demo-only. Do not claim a backend, accounts, payments or database exists when it does not. Keep the code readable and easy to edit. Do not include secret credentials."""

@app.post("/api/generate")
def generate():
    d = request.get_json(silent=True) or {}
    name = str(d.get("name", "My Website"))[:100]
    idea = str(d.get("idea", "")).strip()[:8000]
    style = str(d.get("style", "professional"))[:40]
    size = str(d.get("complexity", "rich"))[:40]
    features = str(d.get("features", ""))[:2000]
    if not idea:
        return jsonify(error="Describe the website you want to create."), 400
    prompt = f"""Create a complete website.
Website name: {name}
User idea: {idea}
Visual style: {style}
Build size: {size}
Features: {features or 'Choose suitable useful features.'}
Make the design custom and professionally art-directed. Include responsive sections and working front-end interactions. Return the entire HTML document only."""
    answer, error = ask_gemini(BASE_INSTRUCTIONS, prompt)
    if error:
        return error
    answer = extract_html(answer)
    if "<html" not in answer.lower() or "<body" not in answer.lower():
        return jsonify(error="The AI did not return a complete HTML page. Please generate again."), 502
    if len(answer) > 150000:
        return jsonify(error="The generated website is too large. Try a more focused request."), 502
    return jsonify(html=answer)

@app.post("/api/refine")
def refine():
    d = request.get_json(silent=True) or {}
    name = str(d.get("name", "My Website"))[:100]
    source = str(d.get("html", "")).strip()
    change = str(d.get("change", "")).strip()[:5000]
    if not source or not change:
        return jsonify(error="Provide website code and describe the changes you want."), 400
    if len(source) > 100000:
        return jsonify(error="This website source is too large for one edit. Remove unused sections or ask for a smaller website."), 413
    instructions = """You are YellowBot Studio, a careful senior front-end engineer editing an existing website. Return only the full updated standalone HTML document, with no markdown fences or commentary. Preserve existing content, visual identity and working functionality unless the user asks to change them. Apply the requested edits fully; avoid replacing the whole site with a generic template. Keep CSS and JavaScript inside the HTML. Make controls work and keep the source readable."""
    prompt = f"""Website name: {name}
Requested changes:
{change}

Current complete HTML source:
{source}

Return the full updated HTML document, not a patch or partial snippet."""
    answer, error = ask_gemini(instructions, prompt, 16000)
    if error:
        return error
    answer = extract_html(answer)
    if "<html" not in answer.lower() or "<body" not in answer.lower():
        return jsonify(error="The AI did not return a complete updated page. Try a more specific change request."), 502
    if len(answer) > 150000:
        return jsonify(error="The updated website is too large. Ask for a more focused edit."), 502
    return jsonify(html=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
