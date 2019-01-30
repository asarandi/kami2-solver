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

#def get_colors_from_file(polygons, canvas, filename):
#    #expecting polygons to be a 2d array or canvas elements
#
#    img = cv2.imread(filename)
#    res = []
#    for row in polygons:
#        for p in row:
#            # coords[] = [x0,y0, x1,y1, x2,y2]
#            coords = [ceil(x * scale_factor / 2) for x in canvas.coords(p)]
#            # get distance between x0,y0 and x1,y1 and find middle xM,yM
#            # from xM,yM get distance to third corner of triangle x2,y2 and find middle
#            xm = (coords[0] + coords[2]) / 2
#            ym = (coords[1] + coords[3]) / 2
#            xp = int((xm + coords[4]) / 2)
#            yp = int((ym + coords[5]) / 2)
#
#            square = img[yp-5:yp+5, xp-5:xp+5]
#            mean = np.mean(square, axis=(0,1))
#            res.append(mean)
#            c = (int(mean[2]) << 16) + (int(mean[1]) << 8) + int(mean[0])
#            canvas.itemconfig(p, fill='#%06x' % c)
#    return res

def mouse_click(event):
    global canvas
    print('clicked at', event.x, event.y)
    print(canvas.find_closest(event.x, event.y))


def board_put_colors(polygons, canvas, filename):
    img = cv2.imread(filename)
    blank = cv2.imread('blank.png')
    pc = get_puzzle_colors(img)    
    if not pc:
        return None
#    for choice in pc:
#        print('choice #%06x' % rgbi(choice))
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
#            why = [1,10]
#            if p in why:
#                print('square', square)
#                print('square color', square_color, '#%06x' % rgbi(square_color))
#                for similarity, color in color_choices:
#                    print('similarity', similarity, 'color #%06x' % rgbi(color))
#                print('color_choices', color_choices)

            blank_similarity = color_distance(blank_color, square_color)

#            if p in why:
#                print('blank similarity', blank_similarity)
            if blank_similarity < 1: #color_choices[0][0]:
#                print('blank similarity', blank_similarity)
                c = 0xffffff
            else:
                c = rgbi(color_choices[0][1])



#            res.append(mean)
#            c = (int(mean[2]) << 16) + (int(mean[1]) << 8) + int(mean[0])
            canvas.itemconfig(p, fill='#%06x' % c)

master = Tk()
canvas = Canvas(master, width=canvas_width, height=canvas_height, bg=canvas_bg_color, borderwidth=0, highlightthickness=0)
canvas.pack()
master.bind('<Q>', gui_close)
master.bind('<q>', gui_close)
master.bind('<Button-1>', mouse_click)
polygons = board.draw_board(0,0,canvas)
if len(sys.argv) > 1:
#    mean_colors = get_colors_from_file(polygons, canvas, sys.argv[1])
    board_put_colors(polygons, canvas, sys.argv[1])
#    for r,g,b in mean_colors:
#        print(colorsys.rgb_to_hls(r,g,b))




master.mainloop()
