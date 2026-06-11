import speech_recognition as sr
import pyttsx3
import sys
import urllib.request
import urllib.error
import json

# ── CONFIG ──────────────────────────────────────────────────────────────────
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# ────────────────────────────────────────────────────────────────────────────

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Models to try in order (first working one will be used)
MODELS_TO_TRY = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-preview-05-20",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-pro",
]

def find_working_model():
    """Try each model and return the first one that responds."""
    print(" Finding a working model for your API key...")
    test_payload = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": "hi"}]}]
    }).encode("utf-8")

    for model in MODELS_TO_TRY:
        url = f"{BASE_URL}/models/{model}:generateContent?key={GEMINI_API_KEY}"
        req = urllib.request.Request(
            url, data=test_payload,
            headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status == 200:
                    print(f" Found working model: {model}")
                    return model
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if "API_KEY_INVALID" in body or "API key not valid" in body:
                print(" Invalid API key! Please check chatbot.py")
                sys.exit(1)
            # 404 = model not found, 429 = quota, try next
            print(f"   ✗ {model} → {e.code}")
        except Exception as e:
            print(f"   ✗ {model} → {e}")

    return None

def speak(engine, text):
    print(f"\n Gemini: {text}\n")
    engine.say(text)
    engine.runAndWait()

def listen(recognizer, mic):
    print(" Listening… (speak now)")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print(" No speech detected – try again.")
            return None
    try:
        text = recognizer.recognize_google(audio)
        print(f" You said: {text}")
        return text
    except sr.UnknownValueError:
        print(" Couldn't understand – please repeat.")
        return None
    except sr.RequestError as e:
        print(f"  Speech recognition error: {e}")
        return None

def ask_gemini(model, history, user_text):
    history.append({"role": "user", "parts": [{"text": user_text}]})
    payload = json.dumps({
        "system_instruction": {
            "parts": [{"text": (
                "You are a friendly, concise voice assistant. "
                "Keep answers short – ideally 1-3 sentences – "
                "because your replies will be spoken aloud."
            )}]
        },
        "contents": history
    }).encode("utf-8")

    url = f"{BASE_URL}/models/{model}:generateContent?key={GEMINI_API_KEY}"
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    history.append({"role": "model", "parts": [{"text": reply}]})
    return reply

def main():
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("  Please open chatbot.py and replace YOUR_GEMINI_API_KEY_HERE with your Gemini API key.")
        print("    Get one free at: https://aistudio.google.com/")
        sys.exit(1)

    print(" Starting Voice Chatbot…")

    model = find_working_model()
    if not model:
        print("\n No working model found for your API key.")
        print("   Your free quota may be exhausted for today. Try again tomorrow.")
        print("   Or visit https://aistudio.google.com/ to check your quota.")
        sys.exit(1)

    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    engine.setProperty("volume", 1.0)

    history = []

    print("\n  Voice chatbot ready!")
    print("    Say something to start. Say 'quit' or 'exit' to stop.\n")
    speak(engine, "Hi! I'm your voice assistant. How can I help you today?")

    while True:
        user_input = listen(recognizer, mic)
        if user_input is None:
            continue
        if user_input.lower().strip() in {"quit", "exit", "bye", "goodbye", "stop"}:
            speak(engine, "Goodbye! Have a great day!")
            break
        try:
            reply = ask_gemini(model, history, user_input)
            speak(engine, reply)
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            print(f"  HTTP Error {e.code}: {body[:200]}")
            speak(engine, "Sorry, I ran into an error. Please try again.")
        except Exception as e:
            print(f"  Error: {e}")
            speak(engine, "Sorry, I ran into an error. Please try again.")

if __name__ == "__main__":
    main()
