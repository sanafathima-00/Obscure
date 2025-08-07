# **Project Obscure**



## 🕵️ Project Overview

**Project Obscure** is a stealthy, lightweight AI-powered desktop assistant that runs locally and interacts with the user through real-time voice-based conversations. It is screen-aware and privacy-friendly, built for smooth performance on low-resource systems.

---

## ✨ Features

- 🧠 Runs local LLM (Phi 3 mini via Ollama)
- 🗣️ Real-time speech-to-text input
- 🗨️ Natural voice responses using text-to-speech
- 🧾 JSON-based short-term memory for contextual awareness
- 🧰 Prompt engineering for refined assistant behavior
- 🖥️ Screen-aware through image or OCR hooks
- 💻 <5% CPU usage on modest hardware (16GB RAM, i7 CPU)

---

## 🛠️ Tech Stack

- **Language**: Python
- **LLM Runtime**: Ollama
- **Model**: Phi 3 mini (Lightweight LLM)
- **Voice Input**: `speech_recognition`
- **Voice Output**: `pyttsx3` / `edge-tts`
- **Memory**: Local JSON files
- **Screen Hook**: `pyautogui`, `pytesseract`

---

## 🚀 Installation and Setup

### Prerequisites
- Python 3.10+
- Ollama installed and running
- Phi model pulled via Ollama: `ollama run phi3 mini`

### Steps

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/project-obscure.git
cd project-obscure
```

2. **Install Python Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Assistant**
```bash
python main.py
```

4. Speak to your assistant — it responds with contextual awareness and continues the conversation naturally.

---

## 📁 Project Structure

```
project-obscure/
├── congig.py
├── main.py
├── memory.py
├── speech.py
└── vision.py
```

---

## 📦 Dependencies

- `ollama`
- `requests`
- `speech_recognition`
- `pyttsx3` or `edge-tts`
- `pyaudio`
- `json`
- `pyautogui` 
- `pytesseract` 

---

## 🔧 Customization

- Edit the prompt logic in `config.py`
- Tweak voice engine in `config.py`
- Extend memory logic via `memory.py`
- Add screen awareness using `vision.py`

---

## 🐞 Known Issues

- Initial load time may vary based on Ollama start
- Speech recognition depends on mic quality
- No GUI – runs via terminal for now

---

## 🚧 Future Improvements

- GUI-based launcher for assistant
- OCR-based screen reading
- Task automation from spoken commands
- Plugin system for modular tools

---

## 📄 License

Licensed under the **MIT License**.

---

## 🙌 Acknowledgments

- [Ollama](https://ollama.com/) for local LLM hosting
- [Phi](https://huggingface.co/microsoft/phi-2) for an efficient model
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) and [pyttsx3](https://pypi.org/project/pyttsx3/) for voice interaction
- The open-source community for enabling accessible AI
