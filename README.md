# Lingo TV
Translate between 60+ Indian and world languages on a TV-style website. Pick a channel (language) on each TV, type, press Translate.
100% free: no API keys, no paid services. It tries Google Translate (two endpoints), then MyMemory.

## Run locally
    pip install -r requirements.txt
    python app.py          # http://localhost:8000
If a translation fails, open http://localhost:8000/api/diag to see which free engine is blocked on your network.

## Deploy on Render (free)
1. Put this folder in a GitHub repo.
2. Render dashboard > New > Blueprint > pick the repo (reads `render.yaml`). Or New > Web Service: build `pip install -r requirements.txt`, start `gunicorn app:app --bind 0.0.0.0:$PORT`.
Free Render sites sleep after ~15 min idle; the first visit then takes about a minute.
