import os
import re
import json
import secrets
import threading
from pathlib import Path
from datetime import datetime, timezone

import requests
from flask import Flask, jsonify, request, send_from_directory, abort

BASE_DIR = Path(__file__).resolve().parent
PUBLISH_DIR = Path(os.getenv("PUBLISH_DIR", str(BASE_DIR / "published")))
PUBLISH_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="/static")
API_KEY = os.getenv("GROQ_API_KEY", "").strip()
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()
API_URL = "https://api.groq.com/openai/v1/chat/completions"
publish_lock = threading.Lock()
published_sites = {}

def load_published():
    # Published HTML files are kept on disk for as long as the server filesystem persists.
    for file in PUBLISH_DIR.glob("*.html"):
        try:
            published_sites[file.stem] = file.read_text(encoding="utf-8")
        except OSError:
            pass

load_published()

@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.get("/chat")
@app.get("/chat.html")
def chat_page():
    return send_from_directory(BASE_DIR, "chat.html")

@app.get("/blank")
def blank_site():
    return send_from_directory(BASE_DIR, "blank.html")

@app.get("/api/status")
def status():
    return jsonify(configured=bool(API_KEY), provider="Groq", model=MODEL, publishing=True)

def ask_groq(instructions, prompt, limit=14000):
    if not API_KEY:
        return None, (jsonify(error="AI is not configured. Add GROQ_API_KEY to the server environment, then restart."), 503)
    payload = {"model": MODEL, "messages": [{"role": "system", "content": instructions}, {"role": "user", "content": prompt}], "max_tokens": limit, "temperature": 0.7}
    try:
        response = requests.post(API_URL, headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}, json=payload, timeout=180)
    except requests.RequestException:
        return None, (jsonify(error="Could not reach Groq. Check the server connection and try again."), 502)
    if response.status_code in (401, 403):
        return None, (jsonify(error="Groq rejected the key. Check GROQ_API_KEY."), 502)
    if response.status_code == 429:
        return None, (jsonify(error="Groq rate limit reached. Wait for the quota to reset and try again."), 429)
    if not response.ok:
        try:
            message = response.json().get("error", {}).get("message", "Groq request failed.")
        except (ValueError, AttributeError):
            message = "Groq request failed."
        return None, (jsonify(error=str(message)[:500]), 502)
    try:
        choices = response.json().get("choices", [])
        answer = choices[0].get("message", {}).get("content", "").strip() if choices else ""
    except (ValueError, TypeError, AttributeError, IndexError):
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

BASE_INSTRUCTIONS = """You are YellowBot Studio, a senior web designer and front-end engineer. Return one complete standalone HTML document only, beginning with <!doctype html>; no markdown fences or explanation. Put all CSS and JavaScript inside the HTML. Build polished, responsive, accessible pages with useful working front-end interactions. No build tools or required packages. Do not create fake non-working buttons. Forms must validate and disclose when demo-only. Never claim a backend, accounts, payments or database exists unless provided. Do not include secret credentials."""

@app.post("/api/generate")
def generate():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "My Website"))[:100]
    idea = str(data.get("idea", "")).strip()[:8000]
    style = str(data.get("style", "professional"))[:40]
    features = str(data.get("features", ""))[:2000]
    if not idea:
        return jsonify(error="Describe the website you want to create."), 400
    prompt = f"Create a complete website.\nName: {name}\nIdea: {idea}\nVisual style: {style}\nFeatures: {features or 'Choose suitable useful features.'}\nReturn the entire standalone HTML document only."
    answer, error = ask_groq(BASE_INSTRUCTIONS, prompt)
    if error:
        return error
    html = extract_html(answer)
    if "<html" not in html.lower() or "<body" not in html.lower():
        return jsonify(error="The AI did not return a complete HTML page. Try again."), 502
    if len(html) > 150000:
        return jsonify(error="Generated website is too large. Try a more focused request."), 502
    return jsonify(html=html)

@app.post("/api/refine")
def refine():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "My Website"))[:100]
    source = str(data.get("html", "")).strip()
    change = str(data.get("change", "")).strip()[:5000]
    if not source or not change:
        return jsonify(error="Provide website code and describe the changes you want."), 400
    if len(source) > 100000:
        return jsonify(error="This website source is too large for one edit."), 413
    instructions = "You are a careful senior front-end engineer. Return only the full updated standalone HTML document. Preserve existing content and working functionality unless asked to change it. Keep CSS and JavaScript inside the HTML."
    answer, error = ask_groq(instructions, f"Website: {name}\nRequested changes: {change}\nCurrent HTML:\n{source}\nReturn the full updated HTML.", 16000)
    if error:
        return error
    html = extract_html(answer)
    if "<html" not in html.lower() or "<body" not in html.lower():
        return jsonify(error="The AI did not return a complete updated page. Try a more specific request."), 502
    if len(html) > 150000:
        return jsonify(error="Updated website is too large. Ask for a more focused change."), 502
    return jsonify(html=html)

@app.post("/api/publish")
def publish():
    data = request.get_json(silent=True) or {}
    html = str(data.get("html", "")).strip()
    if not html or "<html" not in html.lower() or "<body" not in html.lower():
        return jsonify(error="Create a complete HTML website before publishing."), 400
    if len(html) > 150000:
        return jsonify(error="This website is too large to publish."), 413
    slug = secrets.token_urlsafe(7).replace("-", "").replace("_", "")[:12].lower()
    try:
        with publish_lock:
            (PUBLISH_DIR / f"{slug}.html").write_text(html, encoding="utf-8")
            published_sites[slug] = html
    except OSError:
        return jsonify(error="The server could not save the published site. Check disk permissions."), 500
    return jsonify(slug=slug, url=request.url_root.rstrip("/") + "/p/" + slug)

@app.get("/p/<slug>")
def public_site(slug):
    html = published_sites.get(slug)
    if html is None:
        file = PUBLISH_DIR / f"{slug}.html"
        if file.is_file() and file.parent == PUBLISH_DIR:
            try:
                html = file.read_text(encoding="utf-8")
            except OSError:
                html = None
    if html is None:
        abort(404)
    from flask import Response
    return Response(html, mimetype="text/html; charset=utf-8")

@app.get("/api/published")
def list_published():
    return jsonify(sites=[{"slug": slug, "url": request.url_root.rstrip("/") + "/p/" + slug} for slug in sorted(published_sites)])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
