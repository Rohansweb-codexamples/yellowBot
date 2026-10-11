import os
import re
import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=".")
API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
API_URL = "https://api.openai.com/v1/responses"

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/api/status")
def status():
    return jsonify(configured=bool(API_KEY), provider="OpenAI", model=MODEL)

def ask_openai(instructions, prompt, limit=14000):
    if not API_KEY:
        return None, (jsonify(error="OpenAI is not configured. Add OPENAI_API_KEY to your server environment settings, then redeploy."), 503)
    try:
        r = requests.post(API_URL, headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}, json={"model": MODEL, "instructions": instructions, "input": prompt, "max_output_tokens": limit, "store": False}, timeout=180)
    except requests.RequestException:
        return None, (jsonify(error="Could not reach OpenAI. Check the server connection and try again."), 502)
    if r.status_code == 401:
        return None, (jsonify(error="OpenAI rejected the key. Check OPENAI_API_KEY in your hosting settings."), 502)
    if r.status_code == 429:
        return None, (jsonify(error="OpenAI rate limit or account quota reached. Check your API usage and billing."), 429)
    if not r.ok:
        try:
            message = r.json().get("error", {}).get("message", "OpenAI request failed.")
        except ValueError:
            message = "OpenAI request failed."
        return None, (jsonify(error=str(message)[:500]), 502)
    try:
        data = r.json()
        parts = []
        for item in data.get("output", []):
            if item.get("type") == "message":
                for part in item.get("content", []):
                    if part.get("type") == "output_text":
                        parts.append(part.get("text", ""))
        answer = "\n".join(parts).strip()
    except (ValueError, TypeError, AttributeError):
        answer = ""
    if not answer:
        return None, (jsonify(error="The AI returned an empty result. Try a shorter request."), 502)
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
    answer, error = ask_openai(BASE_INSTRUCTIONS, prompt)
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
    answer, error = ask_openai(instructions, prompt, 16000)
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
