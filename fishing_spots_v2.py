from PIL import ImageGrab, ImageDraw
import cv2
import numpy as np
import time

# TODO:
# - docstrings
# - parameters
# - encapsulation
# - unit tests
# - asset links
# - os monitor info
# - relative positioning by pyautogui

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

def find_template_continuous(template_path, threshold=0.53):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    while True:

        x0, y0, x1, y1 = (960-1920), 30, (1740-1920), 610 # display 2
        screenshot = ImageGrab.grab(bbox=(x0, y0, x1, y1), all_screens=True)
        draw_grid_on_image(screenshot)
        screenshot_np = np.array(screenshot)

        target_image = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        target_image_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(target_image_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]): 
            cv2.rectangle(target_image, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)

        cv2.imshow('Detected', target_image)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.0005)

    cv2.destroyAllWindows()


find_template_continuous("./images/fishing-sprite.png")
