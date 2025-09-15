import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import subprocess
import smtplib
import requests
import json
import speech_recognition as sr
from deep_translator import GoogleTranslator
import openai
import random
import webbrowser
from bs4 import BeautifulSoup
import time
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask App
app = Flask(__name__)
CORS(app)

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"

# ---------------- SPEAK FIX ---------------- #
def speak(text, voice="Samantha"):
    """Cross-platform safe TTS with threading."""
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.setProperty('volume', 1)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"Speak error: {e}")

    threading.Thread(target=_speak).start()
    return text  # also return text so Flask can respond


# ---------------- LISTEN ---------------- #
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣️ You said: {command}")
        return command
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Speech service error."


# ---------------- FEATURES ---------------- #
def open_whatsapp():
    speak("Opening WhatsApp")
    subprocess.run(["open", "-a", "WhatsApp"])


def get_weather(city="India"):
    API_KEY = "your_openweathermap_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]
            return f"The temperature in {city} is {temp}°C with {weather_desc}"
        else:
            return "Sorry, I couldn't fetch the weather."
    except Exception as e:
        return f"Weather error: {str(e)}"


def send_email(to_email, subject, message):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_email, email_message)
        server.quit()
        return "Email sent successfully."
    except:
        return "Failed to send email."


def control_mac(command):
    if "shutdown" in command:
        os.system("sudo shutdown -h now")
        return "Shutting down system."
    elif "restart" in command:
        os.system("sudo shutdown -r now")
        return "Restarting system."
    elif "sleep" in command:
        os.system("pmset sleepnow")
        return "System going to sleep."
    elif "increase volume" in command:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
        return "Volume increased."
    elif "decrease volume" in command:
        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
        return "Volume decreased."
    elif "mute" in command:
        os.system("osascript -e 'set volume output muted true'")
        return "Muted."
    elif "unmute" in command:
        os.system("osascript -e 'set volume output muted false'")
        return "Unmuted."
    else:
        return "Sorry, I couldn't execute that command."


def translate_text(text, target_language="es"):
    try:
        translated_text = GoogleTranslator(source="auto", target=target_language).translate(text)
        return translated_text
    except Exception as e:
        return f"Translation error: {e}"


def get_news_gnews():
    API_KEY = "your_gnews_api_key"
    url = f"https://gnews.io/api/v4/top-headlines?country=in&token={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "articles" in data and data["articles"]:
            headlines = [a.get("title", "No title") for a in data["articles"][:5]]
            return headlines
        else:
            return ["No news found."]
    except Exception as e:
        return [f"News error: {e}"]


def chat_with_ai(prompt):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response["choices"][0]["message"]["content"]
        return reply
    except Exception as e:
        return f"AI Chat error: {e}"


# ---------------- PROCESS COMMAND ---------------- #
def process_command(command):
    if "hello" in command:
        return speak("Hello! How can I assist you?")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return speak(f"The current time is {now}")
    elif "play" in command:
        song = command.replace("play", "").strip()
        pywhatkit.playonyt(song)
        return speak(f"Playing {song} on YouTube")
    elif "weather" in command:
        city = command.replace("weather", "").strip() or "India"
        return speak(get_weather(city))
    elif "news" in command:
        news_list = get_news_gnews()
        for i, n in enumerate(news_list, 1):
            speak(f"News {i}: {n}")
        return "News fetched."
    elif "translate" in command:
        return speak(translate_text("Hello, how are you?", "fr"))
    elif "chat" in command:
        return speak(chat_with_ai("Tell me a joke"))
    elif "control" in command:
        return speak(control_mac(command))
    elif "open whatsapp" in command:
        open_whatsapp()
        return speak("Opening WhatsApp")
    else:
        return speak("Sorry, I couldn't execute the command.")


# ---------------- FLASK ROUTE ---------------- #
@app.route("/api/jarvis", methods=["POST"])
def jarvis_api():
    data = request.json
    command = data.get("command", "").lower()
    print(f"Received: {command}")
    response = process_command(command)
    return jsonify({"response": response})


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    speak("Jarvis API server started.")
    app.run(host="0.0.0.0", port=5001, debug=True)
