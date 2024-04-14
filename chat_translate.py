from PIL import Image, ImageGrab
import re
import time
import pytesseract
from googletrans import Translator
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# TODO:
# - docstrings
# - parameters
# - encapsulation
# - unit tests
# - tesseract url
# - os monitor info
# - relative positioning by pyautogui

def get_image():
    x0, y0, x1, y1 = 960, 650, 1740, 1050
    x0, y0, x1, y1 = -960, 650, -180, 1050 # display 2
    img = ImageGrab.grab(bbox=(x0, y0, x1, y1), all_screens=True)
    img = img.convert('L')
    img.save('test.png')
    return img

def get_text(img):
    config = '--psm 6'
    try:
        #print(pytesseract.image_to_string(Image.open('test.png'), lang='pol', config=config, timeout=10))
        #print(pytesseract.image_to_string(img, timeout=2)) # Timeout after 2 seconds
        return pytesseract.image_to_string(Image.open('test.png'), lang='pol', config=config, timeout=10)
    except RuntimeError as timeout_error:
        pass

def clean_text(txt):
    pattern = r'([0-9]+:[0-9]+\s.+:)'
    cleaned_txt = re.sub(pattern, '', txt)
    splitted_text = cleaned_txt.split('\n')
    unnspaced_text = list(filter(lambda x : x != '', splitted_text))
    return unnspaced_text

def translate_text(txt_list):
    translator = Translator()
    translations = translator.translate(txt_list, dest='en')
    print('--------------------------------------------')
    for translation in translations:
        print('TEXT: ', translation.origin, ' -> ', translation.text)

while True:
    img = get_image()
    txt = get_text(img)
    txt_list = clean_text(txt)
    translate_text(txt_list)
    time.sleep(10)