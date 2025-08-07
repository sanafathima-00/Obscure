import json
# We now import CHAT_SYSTEM_PROMPT instead of the old name
from config import MEMORY_FILE, CHAT_SYSTEM_PROMPT

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
        # We now use the correct variable when creating a new memory file
        return [{'role': 'system', 'content': CHAT_SYSTEM_PROMPT}]