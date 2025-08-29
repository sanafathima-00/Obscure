# actions.py
import os
import pyautogui
import time
import requests

# Dictionary to map friendly names to system commands
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "chrome.exe",
    "brave": "brave.exe",
    "excel": "excel.exe",
    "spotify": "spotify.exe"
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
        time.sleep(2)
        pyautogui.write(text, interval=0.05)
        return "I've typed out the text for you."
    except Exception as e:
        print(f"Error typing text: {e}")
        return "Sorry, I couldn't type the text."

# --- UPGRADED FUNCTION FOR N8N ---
def trigger_n8n_workflow(webhook_url, data):
    """
    Sends data to an n8n webhook, waits for the response, and returns the answer.
    """
    print(f"[Action] Triggering n8n workflow at {webhook_url}")
    try:
        # Send a POST request and wait for the response (long timeout)
        response = requests.post(webhook_url, json=data, timeout=120) 
        
        if response.status_code == 200:
            print("[Action] Received successful response from n8n.")
            try:
                # We expect the response to be a JSON object with an "answer" key
                response_json = response.json()
                return response_json.get("answer", "I received a response, but couldn't find the answer key.")
            except requests.exceptions.JSONDecodeError:
                return "I received a response, but it was not in the expected JSON format."
        else:
            return f"There was a problem communicating with your n8n workflow. It responded with status {response.status_code}."
    except requests.exceptions.ConnectionError:
        return "I couldn't connect to the n8n server. Please make sure it's running."
    except requests.exceptions.Timeout:
        return "The request to the n8n workflow timed out. It's taking too long to respond."
    except Exception as e:
        print(f"An unknown error occurred with the n8n workflow: {e}")
        return "An unknown error occurred while trying to trigger the workflow."