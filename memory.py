import json
from config import MEMORY_FILE, SYSTEM_PROMPT

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