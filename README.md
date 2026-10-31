# Lingo TV

**Pick a channel. Type your words. Zap between 60+ languages.**

Lingo TV is a free translation website built with Python and Flask. It has a playful browser interface where languages are TV "channels": you tune one TV to the language you write in, tune the other TV to the language you want, and press **Translate**. It covers popular Indian languages (Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali and more) and many world languages (Spanish, French, Japanese, Arabic and more).

It needs **no API keys and no paid services**.

## ✨ Features

- **61 languages:** 23 Indian and neighbouring languages plus 38 world languages, with translation between any two of them.
- **TV channel guide:** Each TV has a language dropdown styled as a channel guide, with channel numbers, each language's own script, and a search box.
- **Channel zapping:** The ▲ ▼ buttons switch to the next or previous channel, with a static-and-logo flash like a real TV.
- **Auto-detect:** The "from" TV has an *Any language* channel (CH 00) that detects what you typed.
- **Language letter background:** The first letter of every language's name in its own script (E, తె, हि, 日, ع and more) drifts softly across a white background. The two languages you picked glow gently, and tapping a letter tunes the "to" TV to that language.
- **Swap button:** Exchange the two languages and move the translation back into the input box.
- **Try-a-phrase buttons:** One tap translates *Hello!*, *Thank you*, *Good morning*, *Where is the toilet?*, *How much is this?* or *I need help*.
- **Easy for all ages:** Large type, big buttons, A− / A+ text size (remembered between visits), keyboard support, and `Ctrl`/`Cmd` + `Enter` to translate.
- **Light haptics:** A gentle tap when you press Translate or change a language (see [Haptics](#-haptics)).
- **Copy and Clear:** Copy the translation or start over in one tap.
- **Free engines with automatic backup:** Tries several free translation services in order (see [How It Works](#️-how-it-works)).
- **Built-in protection:** Per-visitor rate limit, input length limit, and a small in-memory cache.
- **Ready for Render:** Includes a `render.yaml` blueprint and a `/healthz` health check.

## 🚀 Quick Start

### Requirements

- Python 3.10 or newer recommended
- Internet access (translation is done by free online services, and the page loads Google Fonts)
- macOS, Windows, or Linux

### 1. Extract the project

Extract the ZIP and open a terminal inside the `lingo-tv` folder.

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open <http://localhost:8000> in your browser. Stop the server with `Ctrl+C`.

### 5. Try it on your phone (same Wi-Fi)

The server listens on all network interfaces. Find your computer's local address (for example `192.168.0.185`) and open `http://192.168.0.185:8000` on your phone. This is also the easiest way to feel the haptics.

## 🎮 How to Use

1. **Choose a channel on each TV.** Tap the language bar, search or scroll the channel guide, and pick a language. Or use ▲ ▼ to zap one channel at a time.
2. **Type or paste your words** into the left TV (up to 3000 characters).
3. **Press Translate ▶.** The translation appears on the right TV. Use **Copy** to take it with you.

| Control | What it does |
| --- | --- |
| Language bar | Opens the channel guide with search |
| ▲ / ▼ | Next / previous channel |
| ⇄ Swap | Exchanges the two languages and moves the result back to the input |
| Translate ▶ | Translates (`Ctrl`/`Cmd` + `Enter` in the text box does the same) |
| Copy / Clear | Copies the translation / empties both TVs |
| A− / A+ | Smaller or bigger text |
| Background letters | Tap one to tune the "to" TV to that language |
| Try a phrase | Fills in a common phrase and translates it |

## ⚙️ How It Works

```
Browser UI (static/index.html)
          |
          | GET  /api/languages   -> channel list + background letters
          | POST /api/translate   -> { text, from, to }
          v
     app.py (Flask)
          |  checks: not empty, length limit, valid languages,
          |          same-language shortcut, per-visitor rate limit, cache
          v
   free engines, tried in order (first success wins)
   1. Google Translate (web endpoint)
   2. Google Translate (backup endpoint)
   3. MyMemory (free translation memory)
          |
          v
   translation + engine name shown under the TVs
```

- **Long text** is split on line breaks and sentence ends (1200 characters per piece for Google, 450 for MyMemory) and joined back together, keeping your line breaks.
- **Auto-detect** sends `auto` as the source language.
- **Same language** (from = to) returns your text unchanged.
- **Cache:** The last 500 translations are kept in memory, so repeating a translation is instant. The cache is cleared when the server restarts.
- **Rate limit:** Each visitor (by IP address) may make `RATE_PER_MIN` translations per minute (default 30).
- **Friendly errors:** If no service can be reached, the page says so and suggests checking the internet or firewall.

## 🌍 Languages

| Group | Languages |
| --- | --- |
| India and neighbours (23) | English, Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Urdu, Odia, Assamese, Nepali, Sanskrit, Sindhi, Konkani, Maithili, Dogri, Bhojpuri, Meiteilon (Manipuri), Mizo, Sinhala |
| World (38) | Spanish, French, German, Italian, Portuguese, Russian, Japanese, Chinese (Simplified), Chinese (Traditional), Korean, Arabic, Persian, Hebrew, Turkish, Dutch, Polish, Ukrainian, Greek, Swedish, Danish, Finnish, Czech, Romanian, Hungarian, Thai, Vietnamese, Indonesian, Malay, Filipino, Burmese, Khmer, Lao, Swahili, Amharic, Afrikaans, Georgian, Armenian, Mongolian |

Channel numbers follow this order (CH 01 = English, CH 03 = Telugu, and so on).

## 🔧 Settings

All settings are optional environment variables.

| Variable | Default | Meaning |
| --- | --- | --- |
| `PORT` | `8000` | Port for `python app.py` (Render sets this for you) |
| `MAX_CHARS` | `3000` | Longest text accepted in one translation |
| `RATE_PER_MIN` | `30` | Translations allowed per visitor per minute |

**macOS / Linux**

```bash
export PORT=9000
python app.py
```

**Windows PowerShell**

```powershell
$env:PORT="9000"
python app.py
```

If you change `MAX_CHARS`, also change the `maxlength` and the `/ 3000` counter text in `static/index.html` so the page matches.

## ☁️ Deploy on Render (free)

1. Create a GitHub repository and upload the contents of this folder (`app.py`, `languages.py`, `requirements.txt`, `render.yaml`, `README.md` and the `static/` folder).
2. Sign in at <https://render.com> and choose **New → Blueprint**, then select your repository. Render reads `render.yaml` and creates the service.
   - Prefer doing it by hand? Choose **New → Web Service** and use:
     - **Build command:** `pip install -r requirements.txt`
     - **Start command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60`
     - **Health check path:** `/healthz`
3. Wait for the first deploy to finish, then open the `.onrender.com` address Render shows.

Good to know:

- The free plan puts the site to sleep after about 15 minutes without visitors. The next visit then takes up to a minute to wake it.
- No environment variables or secrets are required.
- If translation does not work after deploying, open `/api/diag` on your site (see [Troubleshooting](#️-troubleshooting)).

## 🗂️ Project Structure

```
lingo-tv/
├── app.py              # Flask server, translation engines, rate limit, cache
├── languages.py        # The language list (code, English name, native name, first letter)
├── requirements.txt    # flask, requests, gunicorn
├── render.yaml         # Render blueprint (free plan, health check)
├── README.md
└── static/
    └── index.html      # The whole interface: TV sets, channel guide, background letters
```

### API

| Method and path | Purpose |
| --- | --- |
| `GET /` | The website |
| `GET /api/languages` | The language list used by the page |
| `POST /api/translate` | Translates `{ "text": "...", "from": "en", "to": "te" }` |
| `GET /api/diag` | Tests each free engine and shows which one works from this computer or server |
| `GET /healthz` | Returns `ok` (used by Render's health check) |

## ➕ Add or Change a Language

1. Open `languages.py` and add a line to the `RAW` list in this format:

   ```
   code|English name|Native name|First letter(s) in that script
   ```

   Example: `te|Telugu|తెలుగు|తె`

2. Use a language code that Google Translate understands (for example `te`, `zh-CN`, `mni-Mtei`).
3. New **Indian or neighbouring** languages should go inside the first 23 lines. The channel guide treats the first 23 entries as "India and neighbours". If you add more than 23 there, update `INDIA=23` near the top of the script in `static/index.html`.
4. Restart the server. The new channel and its background letter appear automatically.

## 📳 Haptics

Lingo TV gives a very light tap when you press **Translate** or change a language.

| Device | Result |
| --- | --- |
| Android phones (Chrome, Firefox) | Short vibration |
| iPhone (iOS 17.4 or newer) | Native haptic tick |
| Mac, Windows and other computers | No haptics (browsers do not offer them) |

## 🛠️ Troubleshooting

- **"The free translators did not answer" or "cannot reach the free translation services":** Open `http://localhost:8000/api/diag`. It tries every engine with "Good morning" and shows which ones work and which fail, with the reason. Check your internet connection, VPN and firewall. Try again after a few seconds, because free services sometimes limit busy periods.
- **"Too many requests":** You reached the per-minute limit. Wait a minute, or raise `RATE_PER_MIN`.
- **Port 8000 is already in use:** Stop the other program or start Lingo TV on another port with `PORT` (see [Settings](#-settings)).
- **Background letters or language names look like empty boxes:** The page loads fonts from Google Fonts, so it needs an internet connection. A few rare scripts (for example Meitei Mayek) may also need a font installed on your device.
- **First visit on Render is very slow:** The free plan was asleep. Wait about a minute, then it responds normally.
- **A translation sounds odd:** Free engines translate word by word more often than a human would. Use short, clear sentences, and check important translations with a native speaker.
- **Copy button does nothing:** Some browsers only allow copying on secure (`https`) pages. Select the text and copy it by hand, or use the deployed Render site.

## 🔐 Privacy and Limits

- Your text is sent to third-party free translation services (Google Translate endpoints and MyMemory) to be translated. Do not enter passwords, personal documents, or other sensitive information.
- Lingo TV has no accounts and does not store your translations on disk. The server keeps the last 500 results in memory only, and your browser stores just your chosen text size.
- Free engines can change, slow down, or block requests without notice, and the Google web endpoints used here are not an official, supported API. For a busy production site, switch to an official paid translation API.
- Translations are machine-generated. Do not rely on them alone for legal, medical, or safety-critical text.
- The page uses Google Fonts (Fredoka and Noto Sans families), which are open-licensed fonts loaded from Google's servers.
