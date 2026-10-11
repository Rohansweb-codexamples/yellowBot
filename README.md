# YellowBot AI Website Builder — Rohans Web

**Live app: https://yellowbot-aib1.onrender.com/**

Open the live AI builder: [yellowbot-aib1.onrender.com](https://yellowbot-aib1.onrender.com/)

Source code: [Rohansweb-codexamples/yellowBot on GitHub](https://github.com/Rohansweb-codexamples/yellowBot)

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
4. Keep the key private. Add it to Render as `GROQ_API_KEY`; never put it in `index.html` or commit it to GitHub.

The default model is `llama-3.3-70b-versatile`. If it is unavailable for your account, choose an active model from the Groq Console and set `GROQ_MODEL` accordingly.

## Deploy / update on Render

This repository uses a **Python Flask backend**, so a `package.json` is not needed.

1. Open [Render Dashboard](https://dashboard.render.com/) and choose **New + → Web Service**, or open the existing YellowBot service.
2. Make sure the service is connected to [this GitHub repository](https://github.com/Rohansweb-codexamples/yellowBot) and deploys the `main` branch.
3. Select **Python** as the runtime.
4. Set **Build Command** to:
   ```bash
   pip install -r requirements.txt
   ```
5. Set **Start Command** to:
   ```bash
   python app.py
   ```
6. Under **Environment**, add `GROQ_API_KEY` = your secret Groq API key. Optional: `GROQ_MODEL=llama-3.3-70b-versatile`.
7. In Render, choose **Manual Deploy → Deploy latest commit** if the homepage still shows the old version. Then hard-refresh the live page with **Ctrl+Shift+R**.

Render's free web service may sleep when idle and has its own usage limits. Groq also has API rate limits. If you receive a 429 response, check your Groq Console limits and wait for the quota window to reset.

## Your two YellowBot domains

Use the domains for two different purposes:

- **`https://yellowbot.rohansweb.co.uk`** — the public landing page: what YellowBot is, features, screenshots, and a button that opens the studio.
- **`https://studio.yellowbot.rohansweb.co.uk`** — the actual AI website builder in this repository.

They should be two separate Render services if you want them to show different websites. Adding both custom domains to one Render service makes both addresses show the same app; DNS alone cannot choose different pages on the same service.

### Connect the Studio domain to this app

1. Open the existing YellowBot web service in [Render Dashboard](https://dashboard.render.com/).
2. Open **Settings → Custom Domains → Add Custom Domain**.
3. Add `studio.yellowbot.rohansweb.co.uk`.
4. In the DNS manager for `rohansweb.co.uk`, create the exact **CNAME** record Render tells you to use. For a subdomain, Render's guide says to point the CNAME to the service's `onrender.com` hostname; use the value shown in your dashboard.
5. Return to Render and click **Verify**. Wait for the TLS certificate and HTTPS to become active.

Keep `https://yellowbot-aib1.onrender.com/` as a fallback while setting this up. Do not remove existing DNS records unless you know what they do. Render's official guide: [Custom Domains](https://render.com/docs/custom-domains).

### Set up the public landing page

Create a **second** Render service for a separate static landing page (it can be a separate GitHub repository), then add `yellowbot.rohansweb.co.uk` to that service under **Settings → Custom Domains**. Add the DNS record Render specifies and verify it. Put a prominent “Open YellowBot Studio” link on the landing page pointing to `https://studio.yellowbot.rohansweb.co.uk`.

DNS changes must be made at the provider that manages `rohansweb.co.uk`; changing this GitHub repository cannot create DNS records or verify custom domains for you.

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

- `index.html` — AI builder homepage, editor, preview, project library and download
- `app.py` — Flask endpoints for Groq website generation and refinement
- `requirements.txt` — Flask and requests dependencies
- `1000007744-removebg-preview.png` — YellowBot character image

**Note:** GitHub Pages alone cannot run the Python AI backend; use Render or another Python web service.
