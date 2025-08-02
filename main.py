import ollama
from whisper_mic import WhisperMic
import edge_tts
import asyncio
import os
from playsound import playsound
import re
import json

# --- Configuration ---
VOICE = "en-US-GuyNeural"
AUDIO_FILE = "response.mp3"
MEMORY_FILE = "memory.json"
SYSTEM_PROMPT = "You are Obscure, a helpful AI assistant running locally on the user's computer. You must answer questions directly using only your internal knowledge. Do not generate code to answer a factual question. Do not pretend you have access to the internet or real-time data. If the user explicitly asks you to write a program or code, then you may do so."
CONTEXT_SIZE = 4

# --- Memory Functions ---
def save_memory(history):
    """Saves the conversation history to the JSON file."""
    with open(MEMORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def load_memory():
    """Loads the conversation history from the JSON file."""
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty/corrupt, start fresh
        return [{'role': 'system', 'content': SYSTEM_PROMPT}]

# --- Text-to-Speech Function ---
async def speak(text):
    """Generates speech from text and plays it."""
    text_for_speech = re.sub(r'```.*?```', '', text, flags=re.DOTALL).replace('*', '').strip()
    if not text_for_speech: return

    try:
        communicate = edge_tts.Communicate(text_for_speech, VOICE)
        await communicate.save(AUDIO_FILE)
        playsound(AUDIO_FILE)
    finally:
        if os.path.exists(AUDIO_FILE): os.remove(AUDIO_FILE)

# --- Model Initialization ---
print("Initializing models, please wait...")
try:
    whisper_mic = WhisperMic(model="tiny.en", pause=0.7, energy=300)
except Exception as e:
    print(f"Error initializing WhisperMic: {e}"); exit()
print("Models initialized. You can start talking now.")

# --- Main Chat Loop ---
messages = load_memory() # Load history from file

while True:
    print("\nAI: Listening...")
    try:
        user_input = whisper_mic.listen()
        print(f"You: {user_input}")

        if not user_input.strip(): continue

        if user_input.lower().strip() in ["exit.", "quit."]:
            print("AI: Exiting chat. Goodbye!")
            asyncio.run(speak("Exiting chat. Goodbye!"))
            break

        messages.append({'role': 'user', 'content': user_input})
        
        contextual_messages = [messages[0]] + messages[-CONTEXT_SIZE:] if len(messages) > CONTEXT_SIZE + 1 else messages
        
        print("AI: ", end="", flush=True)
        full_response = ""
        stream = ollama.chat(model='phi3:mini', messages=contextual_messages, stream=True)
        
        for chunk in stream:
            part = chunk['message']['content']
            print(part, end='', flush=True)
            full_response += part
        
        print() # Newline

        asyncio.run(speak(full_response))
        
        messages.append({'role': 'assistant', 'content': full_response})
        save_memory(messages) # Save history after every turn

    except Exception as e:
        print(f"An error occurred during the loop: {e}")
        break