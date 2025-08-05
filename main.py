import ollama
from whisper_mic import WhisperMic
import asyncio

# Import functions from our new modules
from config import CONTEXT_SIZE
from speech import speak
from vision import read_screen_content
from memory import load_memory, save_memory

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

        if not user_input.strip():
            continue

        if user_input.lower().strip() in ["exit.", "quit."]:
            print("AI: Exiting chat. Goodbye!")
            asyncio.run(speak("Exiting chat. Goodbye!"))
            break
        
        # --- Vision Trigger ---
        if "read the screen" in user_input.lower() or "what do you see" in user_input.lower():
            screen_text = read_screen_content()
            print(f"[Screen Content]:\n---_---\n{screen_text}\n---_---")
            vision_prompt = f"The user asked me to read the screen. I saw the following text. Please summarize it concisely.:\n\n{screen_text}"
            messages.append({'role': 'user', 'content': vision_prompt})
        else:
            messages.append({'role': 'user', 'content': user_input})
        
        # Determine the context for the model
        contextual_messages = [messages[0]] + messages[-CONTEXT_SIZE:] if len(messages) > CONTEXT_SIZE + 1 else messages
        
        # --- Streaming Response ---
        print("AI: ", end="", flush=True)
        full_response = ""
        stream = ollama.chat(model='phi3:mini', messages=contextual_messages, stream=True)
        
        for chunk in stream:
            part = chunk['message']['content']
            print(part, end='', flush=True)
            full_response += part
        
        print() # Newline after the full response is streamed
        asyncio.run(speak(full_response))
        
        messages.append({'role': 'assistant', 'content': full_response})
        save_memory(messages)

    except Exception as e:
        print(f"An error occurred during the loop: {e}")
        break