from tkinter import Tk, Label
from PIL import Image, ImageTk, ImageGrab, ImageChops, ImageDraw, ImageFont
import winsound
from screeninfo import get_monitors

# TODO:
# - docstrings
# - parameters
# - encapsulation
# - unit tests
# - relative positioning by pyautogui
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

monitors = []
monitor_names = []
print("Select one of the following displays by its number:")
for i, m in enumerate(get_monitors()):
    monitors.append(m)
    monitor_names.append(m.name)
    print(f"{i} : {m.name}")
selection = input()
CURRENT_MONITOR = monitors[int(selection)]
x0, y0, x1, y1 = (CURRENT_MONITOR.x+1740), (CURRENT_MONITOR.y+365), (CURRENT_MONITOR.x+1740+180), (CURRENT_MONITOR.y+365+125)
reference_img = ImageGrab.grab(bbox=(x0, y0, x1, y1), all_screens=True)

def update_image(label):
    global reference_img, x0, y0, x1, y1
    current_img = ImageGrab.grab(bbox=(x0, y0, x1, y1), all_screens=True)

    percentage_diff = calculate_difference_percentage(reference_img, current_img)
    print(f"The images are {percentage_diff:.2f}% different.")
        
    if percentage_diff > 1:
        current_img.save("screenshots/detected.jpg")
        draw = ImageDraw.Draw(current_img)
        draw.rectangle([(0, 0), (current_img.width, current_img.height)], outline="red", width=5)
        font_size = 18
        font = ImageFont.truetype("arial.ttf", font_size)
        draw.text((10, 10), "Change Detected", fill="red", font=font)

        winsound.PlaySound("./sounds/418900__lynx_5969__short-beep.wav", winsound.SND_FILENAME)

    img_tk = ImageTk.PhotoImage(image=current_img)
        
    label.config(image=img_tk)
    label.image = img_tk
       
    root.after(1000, update_image, label)

root = Tk()
root.title("Proximity Alarm")

img_placeholder = ImageTk.PhotoImage(Image.new('RGB', (400, 300), 'white'))
label = Label(root, image=img_placeholder)
label.pack()

update_image(label)

root.mainloop()