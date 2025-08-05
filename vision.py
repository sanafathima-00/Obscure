import pytesseract
from mss import mss
from PIL import Image
import os
import pygetwindow as gw

def read_screen_content():
    """Captures and crops the active window to focus on the content area."""
    print("\n[Reading active window content...]")
    try:
        # Get the active window
        active_window = gw.getActiveWindow()
        if not active_window or active_window.width <= 0 or active_window.height <= 0:
            return "No active window found or window is minimized."

        # --- Cropping Logic ---
        # Define how much to crop from the edges (e.g., 10% from the top)
        top_crop_percent = 0.15  # Crop 15% from the top to remove title/menu bars
        side_crop_percent = 0.02 # Crop 2% from the sides
        bottom_crop_percent = 0.1 # Crop 10% from the bottom for status bars

        # Calculate the pixel values for cropping
        left = active_window.left + int(active_window.width * side_crop_percent)
        top = active_window.top + int(active_window.height * top_crop_percent)
        right = active_window.right - int(active_window.width * side_crop_percent)
        bottom = active_window.bottom - int(active_window.height * bottom_crop_percent)
        
        # Define the new, smaller bounding box
        bbox = {"top": top, "left": left, "width": right - left, "height": bottom - top}
        
        if bbox["width"] <= 0 or bbox["height"] <= 0:
            return "Window is too small to read."

        with mss() as sct:
            # Grab the data from the cropped bounding box
            sct_img = sct.grab(bbox)
            # Convert to a PIL Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # Use OCR to extract text
            text = pytesseract.image_to_string(img)
            return text

    except Exception as e:
        # Catch specific pygetwindow error if no window is active
        if "No active window found" in str(e):
            return "No active window found."
        print(f"[Vision Error]: {e}")
        return "I was unable to read the screen."