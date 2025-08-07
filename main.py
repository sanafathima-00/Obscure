import ollama
from whisper_mic import WhisperMic
import asyncio
import threading
import time
import json

# Import from our modules
from config import CONTEXT_SIZE, CHAT_SYSTEM_PROMPT, COMMAND_SYSTEM_PROMPT
from speech import speak
from vision import read_screen_content
from memory import load_memory, save_memory
import actions

# --- Keyword Triggers ---
COMMAND_TRIGGERS = ["open", "launch", "start", "execute", "type", "write"]

# (Keep the assistant_is_busy flag and process_vision_in_background function exactly as they were)
assistant_is_busy = False
def process_vision_in_background():
    global assistant_is_busy
    try:
        assistant_is_busy = True; print("\n[Vision Thread Started]")
        screen_text = read_screen_content(); print(f"[Screen Content]:\n---_---\n{screen_text}\n---_---")
        if not screen_text.strip(): asyncio.run(speak("I couldn't find any text on the screen.")); return
        vision_prompt = f"The user asked me to read the screen. I saw the following text. Please summarize it concisely.:\n\n{screen_text}"
        vision_messages = [{'role': 'system', 'content': CHAT_SYSTEM_PROMPT}, {'role': 'user', 'content': vision_prompt}]
        print("AI: [Summarizing screen...] ", end="", flush=True)
        full_response = ""; stream = ollama.chat(model='phi3:mini', messages=vision_messages, stream=True)
        for chunk in stream: part = chunk['message']['content']; print(part, end='', flush=True); full_response += part
        print(); asyncio.run(speak(full_response))
    finally:
        print("[Vision Thread Finished]"); assistant_is_busy = False

# --- Model Initialization ---
print("Initializing models, please wait...")
try: whisper_mic = WhisperMic(model="tiny.en", pause=0.7, energy=300)
except Exception as e: print(f"Error initializing WhisperMic: {e}"); exit()
print("Models initialized. You can start talking now.")

# --- Main Chat Loop ---
messages = load_memory() # Load history with the old CHAT_SYSTEM_PROMPT

while True:
    try:
        if assistant_is_busy: time.sleep(0.1); continue

        print("\nAI: Listening...")
        user_input = whisper_mic.listen()
        print(f"You: {user_input}")

        if not user_input.strip(): continue
        if user_input.lower().strip() in ["exit.", "quit."]: print("AI: Exiting chat. Goodbye!"); asyncio.run(speak("Exiting chat. Goodbye!")); break
        
        # --- Keyword-based Routing ---
        is_command = any(trigger in user_input.lower() for trigger in COMMAND_TRIGGERS)

        if is_command:
            # --- Handle as a Command ---
            print("[Intent] Command detected. Parsing...")
            intent_response = ollama.chat(
                model='phi3:mini',
                messages=[{'role': 'system', 'content': COMMAND_SYSTEM_PROMPT}, {'role': 'user', 'content': user_input}],
                stream=False, format='json'
            )
            try:
                intent_data = json.loads(intent_response['message']['content'])
                print(f"[Parsed Command]: {intent_data}")
                if 'actions' in intent_data and isinstance(intent_data['actions'], list):
                    for action in intent_data['actions']:
                        tool = action.get('tool')
                        if tool == "open_app":
                            feedback = actions.open_app(action.get('app_name', ''))
                        elif tool == "type_text":
                            feedback = actions.type_text(action.get('text', ''))
                        else:
                            feedback = "I understood the command, but I don't know how to perform that action."
                        asyncio.run(speak(feedback))
                        time.sleep(1) # Pause between actions
            except json.JSONDecodeError:
                asyncio.run(speak("I heard a command, but I couldn't figure out the details."))

        elif "read the screen" in user_input.lower() or "what do you see" in user_input.lower():
            # --- Handle Vision Command Separately ---
            asyncio.run(speak("Reading the screen now. One moment."))
            vision_thread = threading.Thread(target=process_vision_in_background)
            vision_thread.start()
        
        else:
            # --- Handle as a Chat ---
            messages.append({'role': 'user', 'content': user_input})
            contextual_messages = [messages[0]] + messages[-CONTEXT_SIZE:] if len(messages) > CONTEXT_SIZE + 1 else messages
            
            print("AI: ", end="", flush=True)
            full_response = ""; stream = ollama.chat(model='phi3:mini', messages=contextual_messages, stream=True)
            for chunk in stream:
                part = chunk['message']['content']; print(part, end='', flush=True); full_response += part
            print()

            asyncio.run(speak(full_response))
            messages.append({'role': 'assistant', 'content': full_response}); save_memory(messages)

    except Exception as e:
        print(f"An error occurred during the loop: {e}"); break