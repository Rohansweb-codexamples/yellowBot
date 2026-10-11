# YellowBot Website Studio — Rohans Web

YellowBot Studio is an AI-powered website builder. Describe a website, generate a complete HTML page with OpenAI, edit the source code, preview your changes, ask the AI to refine the page, save projects in your browser, and download a standalone HTML file.

## Features

- AI website generation from a natural-language brief.
- Design presets for business sites, portfolios, shop concepts, game hubs, nature pages and blank projects.
- Full editable HTML/CSS/JavaScript source in the browser.
- Live preview, refresh, and open-preview controls.
- Ask YellowBot to make changes while preserving the existing page.
- Save/reopen multiple projects using browser local storage.
- Download a standalone HTML file or copy the source.
- Yellow script, white, dark and nature styles plus light/dark studio appearance.
- The character image is loaded from `1000007744-removebg-preview.png` in this repository.

## Run locally

Requires Python 3.10+.

1. Install dependencies: `pip install -r requirements.txt`
2. Set your OpenAI API key as an environment variable. Never paste it into `index.html` or commit it to GitHub.
3. Start the app: `python app.py`
4. Open `http://localhost:5000`

### Windows PowerShell

Set the key for the current terminal session:

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
python app.py
```

Optional: set `OPENAI_MODEL` to a model available to your API account. The default is `gpt-4.1-mini`.

## Deploy on Render or another Python host

- Build/install command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Add `OPENAI_API_KEY` in the service's environment/secret settings.
- Optional environment variable: `OPENAI_MODEL`

Do not put your API key in public GitHub files or browser JavaScript. The Flask backend calls the OpenAI Responses API and keeps the key on the server. API usage may incur charges according to your OpenAI account.

GitHub Pages alone cannot run this Python backend. Use a Python web service for AI generation.

## Files

- `index.html` — studio UI, editable source, preview, project library and download
- `app.py` — secure server endpoints for OpenAI website generation and refinement
- `requirements.txt` — Flask and requests dependencies
- `1000007744-removebg-preview.png` — YellowBot character image
