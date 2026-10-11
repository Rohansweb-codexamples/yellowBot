<p align="center"><img src="1000007744-removebg-preview.png" alt="YellowBot" width="160"></p>

<h1 align="center">YellowBot AI Website Builder — Rohans Web</h1>

<p align="center">AI-powered website builder using GroqCloud and open-weight models.</p>

---

YellowBot is an AI-powered website builder using **GroqCloud** and open-weight models, not OpenAI or Google Gemini. Describe a website, generate a complete HTML page, edit the source, preview it, ask the AI to refine it, save projects in your browser, and download standalone HTML.

## Features

- AI website generation from a natural-language brief using Groq's Chat Completions API.
- Design presets for business sites, portfolios, shop concepts, game hubs, nature pages and blank projects.
- Full editable HTML/CSS/JavaScript source in the browser.
- Live preview, refresh, and open-preview controls.
- Ask YellowBot to make changes while preserving the existing page.
- Save/reopen multiple projects using browser local storage.
- Download a standalone HTML file or copy the source.
- Yellow script, white, dark and nature styles plus light/dark studio appearance.
- Character image loaded from `1000007744-removebg-preview.png` in this repository.

## Get a Groq API key

1. Open [Groq Console](https://console.groq.com/keys) and sign in.
2. Create an API key.
3. Groq has a free developer tier on supported models, subject to model-specific rate limits and usage policies. **It is not unlimited**; see [Groq's supported models and rate limits](https://console.groq.com/docs/models).
4. Keep the key private. Add it as `GROQ_API_KEY` in your Base44 environment; never put it in `index.html` or commit it to GitHub.

The default model is `llama-3.3-70b-versatile`. If it is unavailable for your account, choose an active model from the Groq Console and set `GROQ_MODEL` accordingly.

## Run with Base44 (Docker Compose)

```bash
docker compose -f docker-compose.base44.yml up -d
```

The app starts on port 3000. Open `http://localhost:3000` in your browser.

## Run locally (without Docker)

Requires Python 3.10+.

```bash
pip install -r requirements.txt
```

Windows PowerShell:
```powershell
$env:GROQ_API_KEY="your-groq-api-key"
python app.py
```

Then open `http://localhost:5000`.

## Files

- `index.html` — AI builder homepage, editor, preview, project library and download
- `app.py` — Flask endpoints for Groq website generation and refinement
- `requirements.txt` — Flask and requests dependencies
- `1000007744-removebg-preview.png` — YellowBot character image
- `chat.html` — Chat-based AI website builder workspace
- `blank.html` — Blank editable HTML starting point
