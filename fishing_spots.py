from tkinter import Tk, Label, Canvas
from PIL import Image, ImageTk, ImageGrab, ImageChops, ImageDraw, ImageFont
import pyautogui
import numpy as np
import winsound

# TODO:
# - docstrings
# - parameters
# - encapsulation
# - unit tests
# - external color dict
# - random pooling timer
# - variable renaming

def draw_grid_on_image(image):
    draw = ImageDraw.Draw(image)
    w, h = image.size
    h_cells = 15
    v_cells = 11
    num_cells = 8
    cell_w, cell_h = w / h_cells, h / v_cells
    
    for i in range(1, h_cells):
        line_x = i * cell_w
        draw.line((line_x, 0, line_x, h), fill="gray", width=1)
    
    for i in range(1, v_cells):
        line_y = i * cell_h
        draw.line((0, line_y, w, line_y), fill="gray", width=1)

sprite_img = Image.open("./images/fishing-sprite.png").convert('L')
def find_image(target, sprite):
    target = target.convert('L')

    t_width, t_height = target.size
    s_width, s_height = sprite.size

    for x in range(t_width - s_width + 1):
        for y in range(t_height - s_height + 1):
            box = (x, y, x + s_width, y + s_height)
            region = target.crop(box)
            
            difference = ImageChops.difference(region, sprite)
            if not difference.getbbox():
                return x, y
    
    return None

def update_image(label):
    x0, y0, x1, y1 = 960, 30, 1740, 610
    x0, y0, x1, y1 = (960-1920), 30, (1740-1920), 610 # display 2
    
    current_img = ImageGrab.grab(bbox=(x0, y0, x1, y1), all_screens=True)
    draw_grid_on_image(current_img)

    result = find_image(current_img,sprite_img)
    if result:
        print(f"Template found at: {result}")
    else:
        print("Template not found.")
       
    img_tk = ImageTk.PhotoImage(image=current_img)
    
    label.config(image=img_tk)
    label.image = img_tk
    
    root.after(1000, update_image, label)

root = Tk()
root.title("Screen Capture")

img_placeholder = ImageTk.PhotoImage(Image.new('RGB', (400, 300), 'white'))
label = Label(root, image=img_placeholder)
label.pack()

update_image(label)

root.mainloop()
