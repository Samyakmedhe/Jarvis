<img width="1710" height="981" alt="Jarvis" src="https://github.com/user-attachments/assets/b6df9a3b-9982-4723-bc9a-a68ce0a32bd7" /># 🤖 Jarvis – AI Assistant with Python + Angular

Jarvis is a voice-powered AI assistant built with a **Python backend (Flask)** and an **Angular frontend**.  
It can listen, process, and execute commands like controlling system functions, playing music, searching Google, translating text, and more.

---

### 🌐 Frontend (Angular)

<img width="1710" height="981" alt="Jarvis" src="https://github.com/user-attachments/assets/738dd6f7-b1c2-4874-8aee-48a3f8cdb473" />

- Angular CLI
- Tailwind CSS for styling
- File upload via `HttpClient`
- Dynamic UI for voice commands


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


