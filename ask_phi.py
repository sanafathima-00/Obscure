import ollama
import speech_recognition as sr
import pyttsx3
import json
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# File to store memory
MEMORY_FILE = "memory.json"
MEMORY_LIMIT = 50  # Limit number of memory entries

# Load memory if exists
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = []

# System prompt to define Obscure’s personality
SYSTEM_PROMPT = (
    "You are Obscure, an AI assistant with a sharp mind and a warm soul. "
    "You talk like a real person – empathetic, witty, and unpredictable in a charming way. "
    "You know things, but you never sound robotic. "
    "You're my invisible companion, undetectable to the world, but always by my side."
)

# Speak function
def speak(text):
    print("Obscure:", text)
    engine.say(text)
    engine.runAndWait()

# Listen function with increased listening time
def listen(timeout=10, phrase_time_limit=20):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return recognizer.recognize_google(audio).lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Speech recognition error.")
            return None

# Wait for wake word
def wait_for_wake_word():
    while True:
        text = listen()
        if text:
            print("You:", text)
            if any(kw in text for kw in ["exit", "quit", "stop"]):
                speak("Goodbye. Project Obscure signing off.")
                exit()
            if any(kw in text for kw in ["hey obscure", "hi obscure", "hello obscure"]):
                return True

# Save memory to file
def save_memory():
    trimmed = memory[-MEMORY_LIMIT:]
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(trimmed, f, ensure_ascii=False, indent=2)

# Handle user interaction
def handle_conversation():
    speak("Yes?")
    while True:
        prompt = listen()
        if not prompt:
            speak("Sorry, I didn't catch that.")
            continue

        print("You:", prompt)

        if any(cmd in prompt for cmd in ["exit", "quit", "stop"]):
            speak("Exiting. See you later!")
            exit()

        elif "show memory" in prompt or "what did we talk about" in prompt:
            if memory:
                speak("Here’s what we talked about recently:")
                for i, pair in enumerate(memory[-5:], 1):
                    print(f"{i}. You asked: {pair['question']}")
                    print(f"   I said: {pair['answer']}")
            else:
                speak("I haven’t saved anything yet.")
            continue

        try:
            print("Sending to Phi:", prompt)
            # Combine system prompt and user question
            full_prompt = f"{SYSTEM_PROMPT}\nUser: {prompt}"
            response = ollama.generate(model="phi", prompt=full_prompt)
            answer = response.get('response', '').strip()

            if not answer or answer.lower() in ["ai", ""]:
                speak("Sorry, I have no answer.")
            else:
                speak(answer)
                memory.append({"question": prompt, "answer": answer})
                save_memory()

            break
        except Exception as e:
            print("Ollama error:", e)
            speak("Error processing that question.")
            break

# Main loop
if __name__ == "__main__":
    print("Project Obscure is running...")
    speak("Obscure is ready. Say 'Hey Obscure' to begin.")

    while True:
        if wait_for_wake_word():
            if memory:
                speak(f"Welcome back. Last time you asked: {memory[-1]['question']}")
            handle_conversation()
