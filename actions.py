import os
import pyautogui
import time

# Dictionary to map friendly names to system commands
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "chrome.exe",
    "browser": "chrome.exe",
    "excel": "excel.exe",
    "spotify": "spotify.exe" # This might require spotify to be in PATH
}

def open_app(app_name):
    """Opens an application using a predefined command mapping."""
    app_name = app_name.lower()
    command = APP_COMMANDS.get(app_name)
    
    if command:
        print(f"[Action] Executing command to open: {command}")
        try:
            os.system(f"start {command}")
            return f"I'm opening {app_name} for you."
        except Exception as e:
            print(f"Error opening app {app_name}: {e}")
            return f"Sorry, I had trouble opening {app_name}."
    else:
        return f"I don't know how to open {app_name}."

def type_text(text):
    """Types out the given text using pyautogui."""
    print(f"[Action] Typing text: {text}")
    try:
        # Give a moment for the user to switch to the correct window
        time.sleep(2)
        pyautogui.write(text, interval=0.05)
        return "I've typed out the text for you."
    except Exception as e:
        print(f"Error typing text: {e}")
        return "Sorry, I couldn't type the text."