from tkinter import Tk, Label, Canvas
from PIL import Image, ImageTk, ImageGrab, ImageChops, ImageDraw, ImageFont
import pyautogui
import winsound
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

range_tiles = []
click_counters = []
cap = ''
color = "yellow"
def draw_click_counter(image, x0, y0, x, y):
    global range_tiles, click_counters

    if len(range_tiles) == 0:
        print("Initializing tiles and counter.")
        w, h = image.size
        h_cells = 15
        v_cells = 11
        cell_w, cell_h = w / h_cells, h / v_cells
        for j in range(v_cells):
            for i in range(h_cells):
                range_tiles.append((x0+((i)*cell_w), y0+((j)*cell_h)))
                click_counters.append(0)
        print(range_tiles)
        print("Done initializing.")
    else:
        for i, tile in enumerate(range_tiles):
            try:
                if (tile[0] < x < range_tiles[i+1][0]) and (tile[1] < y < range_tiles[i+1][1]):
                    click_counters[i] += 1
                    print("Added counter")
            except IndexError:
                pass
        draw = ImageDraw.Draw(image)
        font_size = 9
        font = ImageFont.truetype("arial.ttf", font_size)
        for i, c in enumerate(click_counters):
            draw.text(range_tiles[i], str(c), fill="red", font=font)

def add_click_counter(result):
    global range_tiles, click_counters

    for tile in range_tiles:
        if abs(tile.left - result.left) <= 1 and abs(tile.top - result.top) <= 1:
            i = range_tiles.index(tile)
            click_counters[i] += 1
            change_cap_color()
            return
    range_tiles.append(result)
    click_counters.append(1)
    change_cap_color()

def draw_counter_on_image(image):
    if len(range_tiles) > 0:
        draw = ImageDraw.Draw(image)
        font_size = 22
        font = ImageFont.truetype("arial.ttf", font_size)
        for i, tile in enumerate(range_tiles):
            draw.text((tile.left+(tile.width/3),tile.top+(tile.height/3)), str(click_counters[i]), fill=color, font=font)

def check_cap():
    x0, y0, x1, y1 = -90, 322, -65, 335 # display 2 x(1870,1895), y(165,180)
    img = ImageGrab.grab(bbox=(x0, y0, x1, y1), all_screens=True)
    img = img.convert('L')
    img.save('test.png')
    custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789'
    cap = pytesseract.image_to_string(img, config='--psm 6', timeout=2)
    print(cap)
    return cap

def change_cap_color():
    global color, cap
    color = "yellow"
    if cap == '':
        cap = check_cap()
    else:
        new_cap = check_cap()
        if new_cap != cap:
            #color = "green"
            play_sound()
        cap = new_cap

def play_sound():
    winsound.PlaySound("./sounds/557297__c_rogers__cartoon_waterdrop.wav", winsound.SND_FILENAME)

sprite_img = Image.open("./images/fishing-sprite.png").convert('L')
#sprite_img = Image.open("./images/fishing-sprite.png")
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

def find_image_2(screenshot, sprite):
    try:
        sample = pyautogui.locate(sprite, screenshot, grayscale=True, confidence=0.5)
        return sample
    except pyautogui.ImageNotFoundException:
        return None

def update_image(label):
    x0, y0, x1, y1 = 960, 30, 1740, 610
    x0, y0, x1, y1 = (960-1920), 30, (1740-1920), 610 # display 2
    
    current_img = ImageGrab.grab(bbox=(x0, y0, x1, y1), all_screens=True)
    current_img_bw = current_img.convert('L')
    draw_grid_on_image(current_img)
    draw_counter_on_image(current_img)

    result = find_image_2(current_img_bw, sprite_img)
    
    if result:
        print(f"Template found at: {result}")
        draw = ImageDraw.Draw(current_img)
        draw.rectangle([(result.left, result.top), (result.left+result.width, result.top+result.height)], outline="green", width=5)
        add_click_counter(result)
    else:
        #print("Template not found.")
        pass
       
    img_tk = ImageTk.PhotoImage(image=current_img)
    
    label.config(image=img_tk)
    label.image = img_tk
    
    root.after(10, update_image, label)

root = Tk()
root.title("Screen Capture")

img_placeholder = ImageTk.PhotoImage(Image.new('RGB', (400, 300), 'white'))
label = Label(root, image=img_placeholder)
label.pack()

update_image(label)

root.mainloop()
