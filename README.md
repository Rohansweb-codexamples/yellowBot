# YellowBot Studio — Rohans Web

YellowBot Studio is a playful, game-like page creator. The YellowBot character image is loaded from `1000007744-removebg-preview.png` in this repository.

## What it does

- A guided creative quest with four short steps: choose a page type, name it, pick a visual mood, and write the page details.
- Page templates for landing pages, portfolios, events, nature pages, game pages and blank canvases.
- Four polished themes: yellow script, clean white, sharp dark and fresh nature.
- Preview and edit the page title, description, button text and theme.
- Save creations in browser storage, reopen them from the library, and download a standalone HTML page.
- Light/dark studio appearance and progress/level counters.

YellowBot is written to feel encouraging and friendly, but this page-building mode is a guided rules-based experience rather than a live AI model. Your answers drive the page creation. Saved projects live in the current browser.

## Run locally

1. Open `index.html` directly in a browser, or serve this folder using any static web server.
2. Keep `1000007744-removebg-preview.png` next to `index.html` so the character image loads.

The optional Flask backend and `requirements.txt` remain in the repository for future server features. The current guided page builder does not require an AI API key.

## Files

- `index.html` — YellowBot Studio interface, guided creator, preview, library and HTML export
- `1000007744-removebg-preview.png` — YellowBot character image used in the interface
- `app.py` — optional Flask backend
- `requirements.txt` — Python dependencies
