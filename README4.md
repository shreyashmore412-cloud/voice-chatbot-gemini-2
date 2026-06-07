# 🎙️ Voice Chatbot (Claude-powered)

Talk to Claude using your microphone — it listens, thinks, and speaks back!

---

## ⚡ Quick Setup (do this once)

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

> **Windows users** – if `pyaudio` fails, run this first:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

> **Linux/Ubuntu users** – you may need:
> ```bash
> sudo apt-get install python3-pyaudio portaudio19-dev espeak
> ```

> **Mac users** – you may need:
> ```bash
> brew install portaudio
> pip install pyaudio
> ```

---

### 2. Add your Anthropic API key

Open `chatbot.py` and replace line 6:

```python
ANTHROPIC_API_KEY = "YOUR_API_KEY_HERE"
```

With your actual key (get one free at https://console.anthropic.com/):

```python
ANTHROPIC_API_KEY = "sk-ant-..."
```

---

### 3. Run it

```bash
python chatbot.py
```

---

## 🗣️ How to use

| Action | What to do |
|---|---|
| Talk to the bot | Just speak after "🎤 Listening…" appears |
| Stop the bot | Say **"quit"**, **"exit"**, or **"bye"** |
| No response | Wait for silence detection, then speak again |

---

## ⚙️ Optional tweaks (inside chatbot.py)

| Setting | What it does |
|---|---|
| `engine.setProperty("rate", 160)` | Change speaking speed (words/min) |
| `WAKE_PHRASE = "hey bot"` | Only respond after you say this phrase |
| `max_tokens=512` | Longer/shorter AI replies |

---

## 🛠️ Troubleshooting

- **Mic not detected** → Check your OS mic permissions for Python/Terminal
- **PyAudio install error** → See platform notes above
- **"Invalid API key"** → Double-check the key in chatbot.py
- **Speech not recognised** → Speak clearly; ensure you have internet (Google STT)
