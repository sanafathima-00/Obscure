# command_parser.py

import re
import actions
from thefuzz import process
from config import GEMINI_WEBHOOK_URL

def parse_command(user_input):
    """
    Parses user input using both keyword and fuzzy matching to identify commands.
    Returns a list of actions to be executed.
    """
    user_input_lower = user_input.lower()
    actions_to_perform = []

    # --- 1. Check for "Open" Actions with Fuzzy Matching ---
    open_triggers = ["open", "launch", "start"]
    if any(trigger in user_input_lower for trigger in open_triggers):
        potential_app_name = user_input_lower
        for trigger in open_triggers:
            if trigger in potential_app_name:
                potential_app_name = potential_app_name.split(trigger, 1)[1].strip()
                break
        best_match, score = process.extractOne(potential_app_name, actions.APP_COMMANDS.keys())
        if score > 75:
            app_to_open = best_match
            print(f"[Parser] Detected 'open' command. Best match: '{app_to_open}' (Confidence: {score}%)")
            actions_to_perform.append({'func': actions.open_app, 'args': {'app_name': app_to_open}})

    # --- 2. Check for "Type" Actions ---
    type_triggers = ["type", "write", "enter"]
    if any(trigger in user_input_lower for trigger in type_triggers):
        text_to_type = None
        for trigger in type_triggers:
            if trigger in user_input_lower:
                try:
                    text_to_type = user_input.split(trigger, 1)[1].strip()
                    if text_to_type.startswith(('"', "'")) and text_to_type.endswith(('"', "'")):
                         text_to_type = text_to_type[1:-1]
                    break
                except IndexError:
                    continue
        if text_to_type:
            print(f"[Parser] Detected 'type' command with text: '{text_to_type}'")
            actions_to_perform.append({'func': actions.type_text, 'args': {'text': text_to_type}})

    # --- 3. Check for Vision Actions ---
    if "read the screen" in user_input_lower or "what do you see" in user_input_lower:
        print("[Parser] Detected 'vision' command.")
        actions_to_perform.append({'func': 'vision_thread', 'args': {}})
        
    # --- 4. Check for Expert AI Delegation (with case-insensitive fix) ---
    expert_triggers = ["ask the expert", "ask gemini"]
    if any(trigger in user_input_lower for trigger in expert_triggers):
        question = None
        for trigger in expert_triggers:
            # Use re.split for a robust, case-insensitive split
            parts = re.split(f'(?i){re.escape(trigger)}', user_input, 1)
            if len(parts) > 1: # If the split was successful
                question = parts[1].strip()
                break
        if question:
            print(f"[Parser] Detected 'Expert AI' command with question: '{question}'")
            actions_to_perform.append({
                'func': actions.trigger_n8n_workflow,
                'args': {
                    'webhook_url': GEMINI_WEBHOOK_URL,
                    'data': {'prompt': question}
                }
            })

    return actions_to_perform