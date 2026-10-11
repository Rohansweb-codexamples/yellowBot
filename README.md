# YellowBot Website Studio — Rohans Web

YellowBot Studio is an AI-powered website builder using **GroqCloud** and open-weight models, not OpenAI or Google Gemini. Describe a website, generate a complete HTML page, edit the source, preview it, ask the AI to refine it, save projects in your browser, and download standalone HTML.

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
4. Keep the key private. Add it to Render as `GROQ_API_KEY`; never put it in `index.html` or commit it to GitHub.

The default model is `llama-3.3-70b-versatile`. If it is unavailable for your account, choose an active model from the Groq Console and set `GROQ_MODEL` accordingly.

## Deploy on Render

This repository uses a **Python Flask backend**, so a `package.json` is not needed.

1. Open [Render Dashboard](https://dashboard.render.com/) and choose **New + → Web Service**.
2. Connect the GitHub repository `Rohansweb-codexamples/yellowBot`.
3. Select **Python** as the runtime.
4. Set **Build Command** to:
   ```bash
   pip install -r requirements.txt
   ```
5. Set **Start Command** to:
   ```bash
   python app.py
   ```
6. Under **Environment**, add:
   - `GROQ_API_KEY` = your secret Groq API key
   - Optional: `GROQ_MODEL` = `llama-3.3-70b-versatile`
7. Create the service or manually deploy the latest commit. Open the Render URL and check the status says **Groq AI connected**.

Render's free web service may sleep when idle and has its own usage limits. Groq also has API rate limits. If you receive a 429 response, check your Groq Console limits and wait for the quota window to reset.

## Run locally

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

- `index.html` — studio UI, editable source, preview, project library and download
- `app.py` — Flask endpoints for Groq website generation and refinement
- `requirements.txt` — Flask and requests dependencies
- `1000007744-removebg-preview.png` — YellowBot character image

GitHub Pages alone cannot run the Python backend; deploy to a Python web service such as Render.
