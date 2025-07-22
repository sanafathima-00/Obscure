from PIL import Image
import pytesseract

# Set the path to your tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load your screenshot image
image = Image.open("screenshot_2025-06-14_09-30-20.png")  # Replace with your file name if needed

# Extract text from the image
text = pytesseract.image_to_string(image)

print("Text found on screen:")
print(text)
