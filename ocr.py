import cv2
import numpy as np
import pytesseract
from RPA.core import notebook
import pyautogui
import regex
import time


# +
def search(pattern, distance=0):
    start = time.time()
    pattern = '(%s){e<=%d}' % (pattern, distance)
    result = []

    image, dx, dy = _screenshot()

    d = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    for text, conf, x, y, w, h in zip(d['text'], d['conf'], d['left'], d['top'], d['width'], d['height']):
        if int(conf) > 50:
            if len(text) > 0:
                if regex.search(pattern, text, flags=regex.IGNORECASE):
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (50, 50, 255), 2)
                    result.append({
                        "text": text,
                        "x": int(dx * (x + w // 2)), "y": int(dy * (y + h // 2))
                    })
                else:
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 50, 50), 2)

    cv2.imwrite("output/ocr_screen_shot.png", image)
    notebook.notebook_image("output/ocr_screen_shot.png")

    end = time.time()
    notebook.notebook_print("%f" % (end-start))

    return result


def click(x, y):
    notebook.notebook_print("x: %d, y: %d" % (x, y))
    pyautogui.click(x, y)


def click_text(text):
    results = search(text)
    if results:
        click(results[0]['x'], results[0]['y'])


def _screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # add here image preprocessing
    # image = _resize(image)
    # image = canny(image)

    # dx and dy are needed because screen scaling can make screen resolution 
    # different for screen shots and mouse coordinates
    dx = pyautogui.size().width / image.shape[1]
    dy = pyautogui.size().height / image.shape[0]

    return image, dx, dy


def _resize(image):
    d = 4000 / min(image.shape)
    if d > 1:
        return cv2.resize(image, None, fx=d, fy=d, interpolation=cv2.INTER_CUBIC)
    return cv2.resize(image, None, fx=d, fy=d, interpolation=cv2.INTER_AREA)


# get grayscale image
def _get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def _remove_noise(image):
    return cv2.medianBlur(image,5)


# dilation
def _dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)


# erosion
def _erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations = 1)


# opening - erosion followed by dilation
def _opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def _canny(image):
    return cv2.Canny(image, 100, 200)

