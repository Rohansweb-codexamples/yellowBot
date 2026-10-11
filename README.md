# YellowBot Website Studio — Rohans Web

YellowBot Studio is an AI-powered website builder using **Google Gemini**, not OpenAI. Describe a website, generate a complete HTML page, edit the source, preview it, ask the AI to refine it, save projects in your browser, and download standalone HTML.

## Features

- AI website generation from a natural-language brief using Google Gemini.
- Design presets for business sites, portfolios, shop concepts, game hubs, nature pages and blank projects.
- Full editable HTML/CSS/JavaScript source in the browser.
- Live preview, refresh, and open-preview controls.
- Ask YellowBot to make changes while preserving the existing page.
- Save/reopen multiple projects using browser local storage.
- Download a standalone HTML file or copy the source.
- Yellow script, white, dark and nature styles plus light/dark studio appearance.
- Character image loaded from `1000007744-removebg-preview.png` in this repository.

## Free AI setup

1. Open [Google AI Studio](https://aistudio.google.com/apikey).
2. Create an API key for the Gemini API.
3. The Gemini API has a free tier, but it is **not unlimited**. Limits depend on the model and your account/project. The default model is `gemini-2.5-flash-lite`; check your current quotas in [Google's rate-limit documentation](https://ai.google.dev/gemini-api/docs/rate-limits).
4. Never put the key in `index.html` or commit it to GitHub. Add it as a secret environment variable on Render.

## Deploy on Render

This repository uses a **Python Flask backend**, so a `package.json` is not needed.

1. Push this repository to GitHub (the updated files are already committed here).
2. In [Render](https://render.com/), choose **New + → Web Service** and connect `Rohansweb-codexamples/yellowBot`.
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
   - Key: `GEMINI_API_KEY`
   - Value: your Google AI Studio API key
   - Optional: `GEMINI_MODEL` = `gemini-2.5-flash-lite`
7. Create the service and wait for deployment. Open the Render URL, then check that the AI status says **Gemini AI connected**.

Render's free web-service plan may sleep when idle and can have its own usage limits. The Gemini free tier also has request/token quotas; neither should be described as unlimited. If you hit a 429 rate-limit response, wait for quota reset and check AI Studio usage.

## Run locally

Requires Python 3.10+.

```bash
pip install -r requirements.txt
```

Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="your-gemini-api-key"
python app.py
```

Then open `http://localhost:5000`.

## Files

- `index.html` — studio UI, editable source, preview, project library and download
- `app.py` — Flask endpoints for Gemini website generation and refinement
- `requirements.txt` — Flask and requests dependencies
- `1000007744-removebg-preview.png` — YellowBot character image

GitHub Pages alone cannot run the Python backend; deploy to a Python web service such as Render.
