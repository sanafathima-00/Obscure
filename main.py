# main.py
import asyncio
import threading
import time
from whisper_mic import WhisperMic
import ollama

# Import from our modules
from config import CONTEXT_SIZE, CHAT_SYSTEM_PROMPT
from speech import speak
from vision import read_screen_content
from memory import load_memory, save_memory
from command_parser import parse_command
import actions # <-- THIS IS THE MISSING LINE

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
messages = load_memory()

while True:
    try:
        if assistant_is_busy: time.sleep(0.1); continue

        print("\nAI: Listening...")
        user_input = whisper_mic.listen()
        print(f"You: {user_input}")

        if not user_input.strip(): continue
        if user_input.lower().strip() in ["exit.", "quit."]: print("AI: Exiting chat. Goodbye!"); asyncio.run(speak("Exiting chat. Goodbye!")); break
        
        commands_to_run = parse_command(user_input)

        if commands_to_run:
            feedback = "" # Initialize feedback to store the expert answer if needed
            is_expert_command = False
            for command in commands_to_run:
                func = command['func']
                args = command['args']

                if func == 'vision_thread':
                    asyncio.run(speak("Reading the screen now. One moment."))
                    vision_thread = threading.Thread(target=process_vision_in_background)
                    vision_thread.start()
                else:
                    feedback = func(**args)
                    # If this was the expert AI, the feedback is the full answer
                    if func == actions.trigger_n8n_workflow:
                        is_expert_command = True
                        print(f"AI: {feedback}") # Print the expert answer
                    asyncio.run(speak(feedback))
                time.sleep(1)
            
            # Save the action to memory
            messages.append({'role': 'user', 'content': user_input})
            if is_expert_command:
                # If it was an expert command, save the actual answer to memory
                messages.append({'role': 'assistant', 'content': feedback})
            else:
                messages.append({'role': 'assistant', 'content': f'[Action Performed] I have executed the requested command(s).'})
            save_memory(messages)
            continue
        
        # --- Default to Chat if no command was found ---
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