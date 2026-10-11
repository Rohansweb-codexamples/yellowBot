# YellowBot — Base44 Dev Environment

## What this is
A Python Flask app (AI website builder) that serves static HTML pages and proxies AI generation/refinement requests to Groq's Chat Completions API.

## Stack
- **Runtime:** Python 3.12 (via `python:3.12-slim` Docker image)
- **Framework:** Flask 3.x
- **Dependencies:** `requirements.txt` (Flask, requests) — installed on container startup
- **Dev server:** `flask run --reload` (live reload enabled via bind mount)
- **Port:** App listens on 5000 inside the container, mapped to host port 3000

## Running
```bash
docker compose -f docker-compose.base44.yml up -d
```

## Secrets
- `GROQ_API_KEY` — required for AI generation/refinement to work. The app boots without it (returns 503 on AI endpoints) but all features need it. Get from https://console.groq.com/keys.
- `GROQ_MODEL` — optional, defaults to `llama-3.3-70b-versatile` in the code.

## Verification
- `curl http://localhost:3000/api/status` → JSON with `configured: true` when GROQ_API_KEY is set
- `curl http://localhost:3000/` → homepage HTML
- `curl http://localhost:3000/chat` → chat/builder page
- `curl http://localhost:3000/blank` → blank editable HTML page

## Notes
- Published sites are stored on disk in `./published/` (created at runtime).
- No build step — source is bind-mounted and dependencies install on startup.
- Flask debug mode + reloader is enabled for live code reloading.
