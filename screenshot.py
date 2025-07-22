from PIL import ImageGrab
import datetime

# Generate a timestamped file name
filename = datetime.datetime.now().strftime("screenshot_%Y-%m-%d_%H-%M-%S.png")

# Capture the screen
image = ImageGrab.grab()

# Save the screenshot
image.save(filename)

print(f"Screenshot saved as {filename}")
