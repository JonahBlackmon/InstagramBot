from pytesseract import pytesseract
from PIL import Image
import pyautogui
import time
import os
from pathConfig import get_default
def screenShot():
    pyautogui.hotkey("win", "shift", "s")
    pyautogui.moveTo(1295, 440, duration = 1)
    
    pyautogui.dragRel(2024-1295, 517-440, duration = 1)

def textExtractor():
    default_path = get_default()
    recent = get_most_recent_file('C:\\Users\\Jonah\\OneDrive\\Pictures\\Screenshots')
    print(recent)
    with open(f'{default_path}/AIChatbot/textFiles/commentFile.txt', 'w') as f:
        f.write(recent)
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    image_path = recent
    img = Image.open(image_path)

    pytesseract.tesseract_cmd = path_to_tesseract

    text = pytesseract.image_to_string(img)

    text = text[2:(text[1:].find('likes') - 7)]
    username = text[:text.find(' ')]
    comment = text[text.find(' ') + 1:]
    
    with open(f'{default_path}/AIChatbot/textFiles/question.txt', 'w') as f:
        f.write(comment)
    print(username)
    print(comment)

def get_most_recent_file(folder_path):
    # List all files in the directory with full path
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
    
    # Filter out directories
    files = [file for file in files if os.path.isfile(file)]
    
    # Sort files by modification time in descending order
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # Return the most recent file
    if files:
        return files[0]
    else:
        return None

time.sleep(3)
textExtractor()








