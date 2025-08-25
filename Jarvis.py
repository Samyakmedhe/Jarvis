import os
import subprocess
import time
import requests
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import smtplib
import json
import speech_recognition as sr
from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
import openai
import webbrowser
import socket

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize Voice Engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1)

# OpenAI API Key (Replace with your actual key)
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

# Define Supported Languages for Translation
languages = {
    "spanish": "es", "french": "fr", "german": "de", "hindi": "hi",
    "chinese": "zh-cn", "japanese": "ja", "italian": "it",
    "russian": "ru", "arabic": "ar", "portuguese": "pt"
}

def speak(text, voice="Samantha"):
    """Converts text to speech on macOS."""
    os.system(f'say -v {voice} "{text}"')
    return text

def listen():
    """Capture voice input and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return ""
    except sr.RequestError:
        print("Could not request results.")
        return ""

def process_command(command):
    """Handles various voice commands and performs actions."""
    command = command.lower()

    if "hello" in command:
        return speak("Hello! How can I assist you?")

    elif "shutdown" in command:
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

    elif "increase brightness" in command:
        os.system("osascript -e 'tell application \"System Events\" to key code 144'")
        return speak("Brightness increased.")

    elif "decrease brightness" in command:
        os.system("osascript -e 'tell application \"System Events\" to key code 145'")
        return speak("Brightness decreased.")

    elif "increase volume" in command:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
        return speak("Volume increased.")

    elif "decrease volume" in command:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
        return speak("Volume decreased.")

    elif "mute" in command:
        os.system("osascript -e 'set volume output muted true'")
        return speak("Muted.")

    elif "unmute" in command:
        os.system("osascript -e 'set volume output muted false'")
        return speak("Unmuted.")

    elif "open bluetooth" in command:
        os.system("open -a 'Bluetooth File Exchange'")
        return speak("Bluetooth settings opened.")

    elif "open wi-fi settings" in command:
        os.system("open /System/Library/PreferencePanes/Network.prefPane")
        return speak("WiFi settings opened.")

    elif "turn on wi-fi" in command:
        os.system("networksetup -setairportpower en0 on")
        return speak("WiFi turned on.")

    elif "turn off wi-fi" in command:
        os.system("networksetup -setairportpower en0 off")
        return speak("WiFi turned off.")

    elif "open notes" in command:
        os.system("open -a Notes")
        return speak("Opening Notes.")

    elif "open finder" in command:
        os.system("open -a Finder")
        return speak("Opening Finder.")

    elif "show desktop" in command:
        os.system("osascript -e 'tell application \"System Events\" to key code 103'")
        return speak("Showing desktop.")

    elif "hide all windows" in command:
        os.system("osascript -e 'tell application \"System Events\" to key code 36'")
        return speak("Hiding all windows.")

    elif "translate" in command:
        words = command.split(" ")
        if "to" in words:
            lang = words[words.index("to") + 1]
            phrase = " ".join(words[1:words.index("to")])
            if lang in languages:
                
                translated = GoogleTranslator(source='auto', target=languages[lang]).translate(phrase)
                return speak(f"Translation: {translated}")
            else:
                return speak("I don't support that language yet.")
        else:
            return speak("Please specify a language to translate to.")

    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return speak(f"Searching Google for {query}")

    elif "play" in command:
        song = command.replace("play", "").strip()
        pywhatkit.playonyt(song)
        return speak(f"Playing {song} on YouTube.")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M %p")
        return speak(f"The time is {now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        return speak(f"Today's date is {today}")

    else:
        return speak("Sorry, I couldn't execute the command.")

@app.route("/api/jarvis", methods=["POST"])
def jarvis_api():
    """API endpoint to receive commands from Angular and return responses."""
    data = request.json
    print(f"Received request: {data}")  # Debugging

    command = data.get("command", "")
    
    if not command:
        return jsonify({"response": "No command received."})

    response = process_command(command)
    
    print(f"Sending response: {response}")  # Debugging
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
  # Ensure Flask runs on port 5001
