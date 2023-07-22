import re
import pygetwindow as gw
import numpy as np
from PIL import ImageGrab

def get_window(_process_name):
    all_windows = gw.getAllWindows()
    pattern = re.compile(_process_name, re.IGNORECASE)
    window = [window for window in all_windows if pattern.search(window.title)]
    if window:
        print("找到进程: {}".format(pattern.search(window[0].title)))
        return window[0]
    return None
    print(" 查找不到进程: {}".format(pattern))
    return None

def get_image_array(_window):
        left, top, right, bottom = _window.left, _window.top, _window.right, _window.bottom
        image = ImageGrab.grab(bbox=(left, top, right, bottom))
        return np.array(image)
