#!/usr/bin/env python3

from tkinter import *
import sys
from random import randrange
import numpy as np
import cv2
from math import ceil, sqrt
import colorsys
import board
from constants import *
from colors import *

def gui_close(event):
    sys.exit(0)

def board_reset(event):
    global canvas
    global board_config
    print('resetting board to original colors')
    for k,v in board_config.items():
        canvas.itemconfig(k, fill='#%06x' % v)

def mouse_button_one(event):
    global canvas
    global selected_color
    print('left mouse button clicked at', event.x, event.y)
    elements_tuple = canvas.find_closest(event.x, event.y)
    if len(elements_tuple) < 1:
        return
    if selected_color:
        e = elements_tuple[0]
        canvas.itemconfig(e, fill=selected_color)
        print('setting color to %s for element %d' % (selected_color, e))

def mouse_button_two(event):
    global canvas
    global selected_color
    print('right mouse button clicked at', event.x, event.y)
    elements_tuple = canvas.find_closest(event.x, event.y)
    if len(elements_tuple) < 1:
        return
    selected_color = canvas.itemcget(elements_tuple[0], 'fill')
    print('selected color is now', selected_color)

def board_put_colors(polygons, canvas, filename):
    img = cv2.imread(filename)
    blank = cv2.imread('blank.png')
    pc = get_puzzle_colors(img)
    res = {}
    if not pc:
        return None
    for row in polygons:
        for p in row:
            coords = [ceil(x * scale_factor / 2) for x in canvas.coords(p)]
            xm = (coords[0] + coords[2]) / 2
            ym = (coords[1] + coords[3]) / 2
            xp = int((xm + coords[4]) / 2)
            yp = int((ym + coords[5]) / 2)
            square = img[yp-5:yp+5, xp-5:xp+5]
            square_color = np.mean(square, axis=(0,1))
            blank_square = blank[yp-5:yp+5, xp-5:xp+5]
            blank_color = np.mean(blank_square, axis=(0,1))
            color_choices = []
            for candidate in pc:
                color_choices.append((color_distance(candidate, square_color), candidate))
            color_choices.sort()
            blank_similarity = color_distance(blank_color, square_color)
            if blank_similarity < 1:
                c = 0xffffff
            else:
                c = rgbi(color_choices[0][1])
            canvas.itemconfig(p, fill='#%06x' % c)
            res[p] = c
    return res

selected_color = None
board_config = None
master = Tk()
canvas = Canvas(master, width=canvas_width, height=canvas_height, bg=canvas_bg_color, borderwidth=0, highlightthickness=0)
canvas.pack()
master.bind('<Q>', gui_close)
master.bind('<q>', gui_close)
master.bind('<r>', board_reset)
master.bind('<Button-1>', mouse_button_one)
master.bind('<Button-2>', mouse_button_two)
polygons = board.draw_board(0,0,canvas)
if len(sys.argv) > 1:
    board_config = board_put_colors(polygons, canvas, sys.argv[1])
else:
    board_config = {}
    for row in polygons:
        for p in row:
            board_config[p] = int(canvas.itemcget(p, 'fill')[1:], 16)


master.mainloop()
