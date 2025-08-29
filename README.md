# Obscure 🤫

*An AI that thinks locally, acts silently, and adapts personally.*

**Obscure** is a stealthy, voice-first AI desktop assistant that runs locally on your machine. It is designed to be a private, powerful, and integrated companion that can see your screen, control your applications, and delegate complex tasks to web services and powerful AI models, all while respecting your privacy.

-----

## ✨ Core Capabilities

  - **🗣️ Voice-First Interaction:** Fully operated by voice with high-quality, real-time speech recognition and natural text-to-speech output.
  - **🖥️ Screen-Aware Vision:** Can read the content of your active window, providing summaries or answering questions about what's on screen.
  - **🦾 System & App Control:** Executes commands to open local applications (Notepad, Chrome, Spotify) and perform UI automation like typing text.
  - **🧠 Hybrid AI Brain:**
      - Uses a fast, local LLM (**Phi-3 Mini**) for instant, private tasks.
      - Delegates complex questions to a powerful external AI (**Google Gemini**) for expert-level answers.
  - **🔌 Extensible Automation via n8n:** Connects to a local [n8n](https://n8n.io/) server, giving it the ability to control hundreds of web services and APIs (e.g., Google Calendar, Slack, Notion) through webhook-driven workflows.
  - **📝 Persistent Memory:** Remembers past conversations using a local `memory.json` file, allowing for contextual follow-up questions.

-----

## 🛠️ Tech Stack

| Component                | Technology                                                                          |
| ------------------------ | ----------------------------------------------------------------------------------- |
| **Language** | Python 3.10+                                                                        |
| **Local LLM Runtime** | Ollama                                                                              |
| **Local LLM** | `phi3:mini`                                                                         |
| **Voice Input (STT)** | `whisper-mic` (based on OpenAI's Whisper)                                           |
| **Voice Output (TTS)** | `edge-tts`                                                                          |
| **UI Automation** | `pyautogui`                                                                         |
| **Screen Vision (OCR)** | `pytesseract` + Tesseract OCR Engine                                                |
| **Web Automation** | n8n (self-hosted)                                                                   |
| **Web Requests** | `requests`                                                                          |
| **UI Framework** | `customtkinter` (for the upcoming Stealth Mode UI)                                  |
| **Windows API Control** | `pywin32` (for the upcoming Stealth Mode features)                                  |
| **Command Parsing** | `thefuzz` (for fuzzy string matching)                                               |

-----

## 🚀 Installation and Setup

### Prerequisites

  - Python 3.10+
  - [Ollama](https://ollama.com/) installed and running.
  - [Tesseract OCR Engine](https://www.google.com/search?q=https://github.com/UB-Mannheim/tesseract/wiki) installed.
  - [Node.js](https://nodejs.org/) installed (preferably using NVM).
  - An n8n server (see instructions below).

### Steps

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/Obscure.git
    cd Obscure
    ```

2.  **Pull the Local AI Model**

    ```bash
    ollama pull phi3:mini
    ```

3.  **Install Python Dependencies**

    ```bash
    # Create and activate a virtual environment
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

    # Install packages
    pip install -r requirements.txt
    ```

4.  **Set Up and Run n8n (for Web Automation)**

    ```bash
    # Install n8n globally
    npm install -g n8n

    # Start the server
    n8n
    ```

5.  **Run Obscure**

    ```bash
    python main.py
    ```

-----

## 📁 Project Structure

```
Obscure/
├── actions.py          # Executes commands (open apps, type text)
├── command_parser.py   # Parses user voice commands
├── config.py           # Stores configuration and API keys
├── main.py             # Main application loop and entry point
├── memory.py           # Manages conversation history
├── speech.py           # Handles text-to-speech
├── vision.py           # Handles screen reading (OCR)
└── requirements.txt    # Lists all Python dependencies
```

-----

## 🚧 Future Improvements (Roadmap)

  - **✅ True Stealth Mode:** Implement the `CustomTkinter` + `pywin32` UI that runs as a background process and is invisible to screen captures.
  - **Hotkey Activation:** Trigger the assistant with a global keyboard shortcut instead of running it in a terminal.
  - **Complex UI Automation:** Build advanced `pyautogui` actions for multi-step tasks (e.g., controlling Spotify playback).
  - **Expanded n8n Workflows:** Add more skills by building workflows for Google Calendar, email, to-do lists, and more.
  - **Code Execution Agent:** Implement the "run and debug" feature for generated code.

-----

## 📄 License

This project is licensed under the **MIT License**.
