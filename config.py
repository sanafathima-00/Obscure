import pytesseract

# --- Core Settings ---
VOICE = "en-US-GuyNeural"
MEMORY_FILE = "memory.json"
AUDIO_FILE = "response.mp3"
CONTEXT_SIZE = 4

# --- NEW: Webhook URLs ---
# Paste the Production URL from your n8n Gemini workflow here
GEMINI_WEBHOOK_URL = "YOUT_WEBHOOK_URL_HERE"

# --- System Prompt ---
CHAT_SYSTEM_PROMPT = "You are Obscure, a helpful AI assistant running locally on the user's computer. Keep your responses concise and to the point."

# --- Tesseract Configuration ---
# Note: Using a raw string (r'') or forward slashes is good practice for paths
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'