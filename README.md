# YellowBot — Rohans Web

YellowBot is a responsive assistant interface with a yellow/orange theme, a custom illustrated bot character (separate from the brand mark), browser-saved chat history, theme switching and conversation export.

## Run locally

1. Install Python 3.10+.
2. Run `pip install -r requirements.txt`.
3. Create a Google AI Studio Gemini API key and set it as the `GEMINI_API_KEY` environment variable. Do not place the key in HTML or commit it to GitHub.
4. Run `python app.py` and open `http://localhost:5000`.

Optional: set `GEMINI_MODEL` to a model available to your API key. The default is `gemini-2.5-flash`.

## Deploy

Deploy as a Python web service with start command `python app.py`. Add `GEMINI_API_KEY` in the hosting provider's secret/environment settings. GitHub Pages alone serves static files and cannot run `app.py`; use a Python host for live AI replies.

## Files

- `index.html` — responsive chat interface
- `app.py` — Flask API; keeps the Gemini API key server-side
- `requirements.txt` — Python dependencies
