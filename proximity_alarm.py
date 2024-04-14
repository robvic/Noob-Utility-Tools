from tkinter import Tk, Label, Canvas
from PIL import Image, ImageTk, ImageGrab, ImageChops, ImageDraw, ImageFont
import numpy as np
import winsound

# TODO:
# - docstrings
# - parameters
# - encapsulation
# - unit tests
# - tesseract url
# - os monitor info
# - relative positioning by pyautogui
# - removal of difference function
# - external utility class
# - configurable .wav files

def calculate_difference_percentage(img1, img2):
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    img1 = img1.resize((img2.width, img2.height))
    
    diff = ImageChops.difference(img1, img2)
    diff = diff.convert('RGB')
    
    hist = diff.histogram()
    
    num_diff_pixels = sum(i * n for i, n in enumerate(hist) if i > 0)
    
    max_diff = diff.width * diff.height * 255
    
    percentage_diff = ((num_diff_pixels / max_diff) * 100)/3 - 100
    
    return percentage_diff

previous_img = None

def update_image(label):
    global previous_img
    x0, y0, x1, y1 = 1740, 365, 1920, 490 # display 1
    x0, y0, x1, y1 = -180, 365, 0, 490 # display 2
    
    current_img = ImageGrab.grab(bbox=(x0, y0, x1, y1), all_screens=True)

    if previous_img is not None:
            percentage_diff = calculate_difference_percentage(previous_img, current_img)
            print(f"The images are {percentage_diff:.2f}% different.")

            if percentage_diff > 1:
                current_img.save("screenshots/detected.jpg")
                draw = ImageDraw.Draw(current_img)
                draw.rectangle([(0, 0), (current_img.width, current_img.height)], outline="red", width=5)
                font_size = 18
                font = ImageFont.truetype("arial.ttf", font_size)
                draw.text((10, 10), "Change Detected", fill="red", font=font)

                winsound.PlaySound("./sounds/418900__lynx_5969__short-beep.wav", winsound.SND_FILENAME)
                
                root.after(3000, lambda: label.config(image=ImageTk.PhotoImage(current_img)))

    img_tk = ImageTk.PhotoImage(image=current_img)
    
    label.config(image=img_tk)
    label.image = img_tk

    previous_img = current_img
    
    root.after(1000, update_image, label)

root = Tk()
root.title("Screen Capture")

img_placeholder = ImageTk.PhotoImage(Image.new('RGB', (400, 300), 'white'))
label = Label(root, image=img_placeholder)
label.pack()

update_image(label)

root.mainloop()