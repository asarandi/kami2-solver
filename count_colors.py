#!/usr/bin/env python3

import sys
import cv2
import numpy as np
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor


def rgbi(lst):
    return (int(lst[2]) << 16) + (int(lst[1]) << 8) + int(lst[0])

def color_distance(c1,c2):
    print('color_distance(): #%06x, #%06x' % (rgbi(c1), rgbi(c2)))
    lab1 = convert_color(sRGBColor(*c1), LabColor)
    lab2 = convert_color(sRGBColor(*c2), LabColor)
    return delta_e_cie2000(lab1,lab2)


def count_colors(img):
    bar = img[1901:,450:]   # rectangle height 100, width 675
#    check if 5 colors


    w       = 675
    fifth   = w // 5
    quarter = w // 4
    third   = w // 3
    half    = w // 2
    color_threshold = 10

    sample1 = np.mean(bar[:, :fifth//2], axis=(0,1))    # minimum sample
    sample2 = np.mean(bar[:, third:half], axis=(0,1))
    cd = color_distance(sample1, sample2)
    print('cd2',cd)
    if cd < color_threshold:
        return 2
    sample3 = np.mean(bar[:, quarter:third], axis=(0,1))
    cd = color_distance(sample1, sample3)
    print('cd3',cd)
    if cd < color_threshold:
        return 3
    sample4 = np.mean(bar[:, fifth:quarter], axis=(0,1))
    cd = color_distance(sample1, sample4)
    print('cd4',cd)
    if cd < color_threshold:
        return 4
    sample5 = np.mean(bar[:, fifth//2:fifth], axis=(0,1))
    cd = color_distance(sample1, sample5)
    print('cd5',cd)
    if cd < color_threshold:
        return 5

    print('failed to detect number of colors')
    return None




if len(sys.argv) == 2:
    img = cv2.imread(sys.argv[1])
    print(count_colors(img))



