"""Lingo TV - free translation between 60+ languages. No API keys, no paid services.
Tries these free engines in order and uses the first that works:
  1. Google Translate (web endpoint)   2. Google Translate (backup endpoint)   3. MyMemory (free translation memory)"""
import os, re, time, collections, requests
from flask import Flask, jsonify, request, send_from_directory
from languages import LANGS, NAMES

app = Flask(__name__, static_folder="static", static_url_path="/static")
MAX_CHARS = int(os.environ.get("MAX_CHARS", "3000"))
PER_MIN = int(os.environ.get("RATE_PER_MIN", "30"))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"}
hits, cache = collections.defaultdict(list), collections.OrderedDict()

def chunks(text, n):
    """Split on line breaks / sentence ends so every piece is <= n characters; keeps line breaks."""
    out = []
    for line in text.split("\n"):
        parts = re.split(r"(?<=[.!?।॥。！？؟])\s+", line) if len(line) > n else [line]
        buf = ""
        for p in parts:
            while len(p) > n: out.append(p[:n]); p = p[n:]
            if len(buf) + len(p) + 1 > n and buf: out.append(buf); buf = p
            else: buf = (buf + " " + p).strip() if buf else p
        out.append(buf); out.append("\n")
    out.pop()
    return out

def run(text, n, fn):
    return "".join(p if p == "\n" or not p.strip() else fn(p) for p in chunks(text, n))

def google(text, src, dst):
    def one(q):
        r = requests.get("https://translate.googleapis.com/translate_a/single", headers=UA, timeout=15,
            params={"client": "gtx", "sl": src, "tl": dst, "dt": "t", "q": q})
        r.raise_for_status()
        return "".join(s[0] for s in r.json()[0] if s and s[0])
    return run(text, 1200, one)

def google_backup(text, src, dst):
    def one(q):
        r = requests.get("https://clients5.google.com/translate_a/t", headers=UA, timeout=15,
            params={"client": "dict-chrome-ex", "sl": src, "tl": dst, "q": q})
        r.raise_for_status()
        j = r.json()
        if isinstance(j, dict) and "sentences" in j: return "".join(s.get("trans", "") for s in j["sentences"])
        if isinstance(j, list): return j[0][0] if isinstance(j[0], list) else j[0]
        raise ValueError("unexpected reply")
    return run(text, 1200, one)

def mymemory(text, src, dst):
    def one(q):
        r = requests.get("https://api.mymemory.translated.net/get", headers=UA, timeout=15,
            params={"q": q, "langpair": f"{'Autodetect' if src == 'auto' else src}|{dst}"})
        r.raise_for_status()
        j = r.json()
        if str(j.get("responseStatus")) != "200": raise ValueError(j.get("responseDetails", "MyMemory error"))
        return j["responseData"]["translatedText"]
    return run(text, 450, one)

ENGINES = [("Google Translate", google), ("Google Translate (backup)", google_backup), ("MyMemory", mymemory)]

@app.get("/healthz")
def healthz(): return "ok"

@app.get("/")
def index(): return send_from_directory("static", "index.html")

@app.get("/api/languages")
def languages(): return jsonify(languages=LANGS, engine="Google Translate")

@app.get("/api/diag")
def diag():
    """Open /api/diag in the browser: shows which free engine works from this computer/server."""
    res = {}
    for name, fn in ENGINES:
        try: res[name] = "OK: " + fn("Good morning", "en", "hi")
        except Exception as e: res[name] = f"FAILED: {type(e).__name__}: {e}"
    return jsonify(res)

@app.post("/api/translate")
def translate():
    d = request.get_json(silent=True) or {}
    text, src, dst = (d.get("text") or "").strip(), d.get("from", "auto"), d.get("to", "")
    if not text: return jsonify(error="Type or paste some text first."), 400
    if len(text) > MAX_CHARS: return jsonify(error=f"Please keep it under {MAX_CHARS} characters."), 400
    if dst not in NAMES or (src != "auto" and src not in NAMES): return jsonify(error="Unknown language channel."), 400
    if src == dst: return jsonify(translation=text, engine="same language")
    ip = (request.headers.get("X-Forwarded-For", request.remote_addr) or "?").split(",")[0].strip()
    now = time.time(); hits[ip] = [t for t in hits[ip] if now - t < 60]
    if len(hits[ip]) >= PER_MIN: return jsonify(error="Too many requests. Please wait a minute."), 429
    hits[ip].append(now)
    k = (src, dst, text)
    if k in cache: return jsonify(translation=cache[k][0], engine=cache[k][1])
    net_errors = 0
    for name, fn in ENGINES:
        try:
            out = fn(text, src, dst)
            if out and out.strip():
                cache[k] = (out, name)
                if len(cache) > 500: cache.popitem(last=False)
                return jsonify(translation=out, engine=name)
        except (requests.ConnectionError, requests.Timeout) as e:
            net_errors += 1; app.logger.warning("%s: %s", name, e)
        except Exception as e:
            app.logger.warning("%s failed: %s: %s", name, type(e).__name__, e)
    if net_errors == len(ENGINES):
        return jsonify(error="This computer cannot reach the free translation services. Check your internet or firewall, then try again."), 502
    return jsonify(error="The free translators did not answer. Wait a few seconds and try again."), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
