import pytesseract

# --- Core Settings ---
VOICE = "en-US-GuyNeural"
MEMORY_FILE = "memory.json"
AUDIO_FILE = "response.mp3"
CONTEXT_SIZE = 4

# --- System Prompt ---
SYSTEM_PROMPT = "You are Obscure, a helpful AI assistant running locally on the user's computer. You must answer questions directly using only your internal knowledge. Do not generate code to answer a factual question. Do not pretend you have access to the internet or real-time data. If the user explicitly asks you to write a program or code, then you may do so."

# --- Tesseract Configuration ---
# IMPORTANT: Update this path if you installed Tesseract somewhere else.
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'