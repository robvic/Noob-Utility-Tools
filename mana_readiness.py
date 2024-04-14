import time
from PIL import Image, ImageGrab
import winsound
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# TODO:
# - docstrings
# - parameters
# - encapsulation
# - unit tests
# - tesseract url
# - os monitor info
# - relative positioning by pyautogui

def update_image():
    x0, y0, x1, y1 = 1740, 365, 1920, 490 # display 1
    x0, y0, x1, y1 = -50, 165, -25, 180 # display 2 x(1870,1895), y(165,180)

    img = ImageGrab.grab(bbox=(x0, y0, x1, y1), all_screens=True)
    img = img.convert('L')
    img.save('test.png')

def get_text(img):
    config = '--psm 6'
    return pytesseract.image_to_string(Image.open('test.png'), lang='pol', config=config, timeout=10)

def check_readiness(txt):
    print("Mana level is: ",txt)
    try:
        mana_qty = int(txt)
        if (mana_qty % 70) == 0:
            winsound.PlaySound("./sounds/124898__greencouch__beeps-17.wav", winsound.SND_FILENAME)
    except:
        pass

while True:
    img = update_image()
    txt = get_text(img)
    check_readiness(txt)
    time.sleep(3)