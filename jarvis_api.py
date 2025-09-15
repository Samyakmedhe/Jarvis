import os
import datetime
import webbrowser
import pyttsx3
import pywhatkit
import wikipedia
import speech_recognition as sr
from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALLOW_DESTRUCTIVE = os.getenv("ALLOW_DESTRUCTIVE", "false").lower() == "true"
JARVIS_PORT = int(os.getenv("JARVIS_PORT", 5001))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# ==========================
# Flask App
# ==========================
app = Flask(__name__)
CORS(app)

# ==========================
# Voice Engine
# ==========================
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1)

# Supported languages
languages = {
    "spanish": "es", "french": "fr", "german": "de", "hindi": "hi",
    "chinese": "zh-cn", "japanese": "ja", "italian": "it",
    "russian": "ru", "arabic": "ar", "portuguese": "pt"
}

# ==========================
# Speak Helper
# ==========================
def speak(text):
    """Converts text to speech"""
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()
    return text

# ==========================
# Listen Helper
# ==========================
def listen():
    """Capture voice input"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return "Sorry, I could not understand."
    except sr.RequestError:
        return "Could not request results."

# ==========================
# Command Processor
# ==========================
def process_command(command: str):
    command = command.lower().strip()

    if not command:
        return speak("I didn’t hear a command.")

    if "hello" in command:
        return speak("Hello! How can I assist you?")

    # -------- System Commands (Protected) --------
    if ALLOW_DESTRUCTIVE:
        if "shutdown" in command:
            speak("Shutting down your system.")
            os.system("sudo shutdown -h now")
            return "Shutting down."
        elif "restart" in command:
            speak("Restarting your system.")
            os.system("sudo shutdown -r now")
            return "Restarting system."
        elif "sleep" in command:
            speak("Putting system to sleep.")
            os.system("pmset sleepnow")
            return "System going to sleep."
    else:
        if any(x in command for x in ["shutdown", "restart", "sleep"]):
            return speak("Destructive commands are disabled for safety.")

    # -------- Volume / Brightness --------
    if "increase brightness" in command:
        os.system("osascript -e 'tell application \"System Events\" to key code 144'")
        return speak("Brightness increased.")
    if "decrease brightness" in command:
        os.system("osascript -e 'tell application \"System Events\" to key code 145'")
        return speak("Brightness decreased.")
    if "increase volume" in command:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
        return speak("Volume increased.")
    if "decrease volume" in command:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
        return speak("Volume decreased.")
    if "mute" in command:
        os.system("osascript -e 'set volume output muted true'")
        return speak("Muted.")
    if "unmute" in command:
        os.system("osascript -e 'set volume output muted false'")
        return speak("Unmuted.")

    # -------- Apps / Settings --------
    if "open bluetooth" in command:
        os.system("open -a 'Bluetooth File Exchange'")
        return speak("Bluetooth settings opened.")
    if "open wi-fi settings" in command:
        os.system("open /System/Library/PreferencePanes/Network.prefPane")
        return speak("WiFi settings opened.")
    if "open notes" in command:
        os.system("open -a Notes")
        return speak("Opening Notes.")
    if "open finder" in command:
        os.system("open -a Finder")
        return speak("Opening Finder.")

    # -------- Utility --------
    if "translate" in command:
        words = command.split(" ")
        if "to" in words:
            lang = words[words.index("to") + 1]
            phrase = " ".join(words[1:words.index("to")])
            if lang in languages:
                translated = GoogleTranslator(source="auto", target=languages[lang]).translate(phrase)
                return speak(f"Translation: {translated}")
            else:
                return speak("I don't support that language yet.")
        return speak("Please specify a language to translate to.")

    if "search google for" in command:
        query = command.replace("search google for", "").strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return speak(f"Searching Google for {query}")

    if "play" in command:
        song = command.replace("play", "").strip()
        pywhatkit.playonyt(song)
        return speak(f"Playing {song} on YouTube.")

    if "time" in command:
        now = datetime.datetime.now().strftime("%H:%M %p")
        return speak(f"The time is {now}")

    if "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        return speak(f"Today's date is {today}")

    # -------- Wikipedia --------
    if "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            return speak(summary)
        except Exception:
            return speak("I couldn't fetch Wikipedia results.")

    return speak("Sorry, I couldn't execute the command.")

# ==========================
# Flask API Endpoint
# ==========================
@app.route("/api/jarvis", methods=["POST"])
def jarvis_api():
    data = request.json or {}
    command = data.get("command", "")
    print(f"Received: {command}")

    response = process_command(command)

    print(f"Responding: {response}")
    return jsonify({"response": response})

# ==========================
# Run App
# ==========================
if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host="0.0.0.0", port=JARVIS_PORT)
