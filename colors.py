import numpy as np
from colormath.color_diff import delta_e_cmc
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor
from constants import *

def rgbi(lst):
    return (int(lst[0]) << 16) + (int(lst[1]) << 8) + int(lst[2])

def color_distance(c1,c2):
    lab1 = convert_color(sRGBColor(*c1), LabColor)
    lab2 = convert_color(sRGBColor(*c2), LabColor)
    d = delta_e_cmc(lab1,lab2) / 10 # XXX
    return d

def count_colors(img):
    bar = img[color_bar_offset_y:,color_bar_offset_x:]   # rectangle height 100, width 675
    w       = color_bar_width
    tenth   = w // 10
    fifth   = w // 5
    quarter = w // 4
    third   = w // 3
    half    = w // 2
    sample1 = np.mean(bar[:, :tenth], axis=(0,1))    # minimum sample
    sample2 = np.mean(bar[:, third:half], axis=(0,1))
    cd = color_distance(sample1, sample2)
    if cd < color_distance_threshold:
        return 2
    sample3 = np.mean(bar[:, quarter:third], axis=(0,1))
    cd = color_distance(sample1, sample3)
    if cd < color_distance_threshold:
        return 3
    sample4 = np.mean(bar[:, fifth:quarter], axis=(0,1))
    cd = color_distance(sample1, sample4)
    if cd < color_distance_threshold:
        return 4
    sample5 = np.mean(bar[:, tenth:fifth], axis=(0,1))
    cd = color_distance(sample1, sample5)
    if cd < color_distance_threshold:
        return 5
    print('failed to detect number of colors')
    return None

def get_puzzle_colors(img):
    count = count_colors(img)
    if not count:
        return None
    res = []
    bar = img[color_bar_offset_y:,color_bar_offset_x:]
    w = color_bar_width // count
    for i in range(count):
        res.append(np.mean(bar[:, i*w:i*w+w], axis=(0,1)))
    return res
