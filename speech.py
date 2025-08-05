import edge_tts
import asyncio
import os
from playsound import playsound
import re
from config import VOICE, AUDIO_FILE

async def speak(text):
    """
    Generates speech from text and plays it.
    Strips out code blocks and other markdown for cleaner speech.
    """
    text_for_speech = re.sub(r'```.*?```', '', text, flags=re.DOTALL).replace('*', '').strip()
    if not text_for_speech:
        return

    try:
        communicate = edge_tts.Communicate(text_for_speech, VOICE)
        await communicate.save(AUDIO_FILE)
        playsound(AUDIO_FILE)
    finally:
        if os.path.exists(AUDIO_FILE):
            os.remove(AUDIO_FILE)