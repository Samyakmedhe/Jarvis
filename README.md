# 🤖 Jarvis – AI Assistant with Python + Angular

Jarvis is a voice-powered AI assistant built with a **Python backend (Flask)** and an **Angular frontend**.  
It can listen, process, and execute commands like controlling system functions, playing music, searching Google, translating text, and more.

---

## 🚀 Demo UI

Here’s how Jarvis looks in action:

![Jarvis AI UI](./Assets/jarvis_ui.png)

*(screenshot from the Angular frontend interface)*

---

## 📂 Project Structure

Jarvis/
│
├── Assets/ # Static assets (images, audio, etc.)
├── Engine/ # Core engine files
├── jarvis_api.py # Flask API layer
├── Jarvis.py # Main Jarvis script
├── jarvisModel/ # AI/ML models
├── main.js # Supporting JS script
├── script.js # Additional JS logic
├── voice.mp3 # Sample audio file
└── frontend/ # Angular frontend (separate folder)

## 🎤 Features
Voice Interaction (SpeechRecognition + pyttsx3)
System Control (shutdown, restart, sleep, brightness, volume, WiFi, Bluetooth, Finder, Notes, etc.)
Translation (using Google Translator API)
Google Search & YouTube Play
Date & Time Reporting
Cross-platform API for Angular frontend

## 🛠 Tech Stack
Backend: Python, Flask, Flask-CORS
Frontend: Angular, TypeScript
AI & Voice: pyttsx3, SpeechRecognition, OpenAI API, Deep Translator
Utilities: pywhatkit, Wikipedia, smtplib


