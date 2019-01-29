#!/usr/bin/env python3

from tkinter import *
import sys
from random import randrange
import numpy as np
import cv2
from math import ceil, sqrt


def polygon_gt(x0,y0):
    res = [x0,y0]
    res.append(x0 + cell_width)
    res.append(y0 + cell_height / 2)
    res.append(x0)
    res.append(y0 + cell_height)
    return res

def polygon_lt(x0,y0):
    res = [x0,y0]
    res.append(x0 + cell_width)
    res.append(y0 - cell_height / 2)
    res.append(x0 + cell_width)
    res.append(y0 + cell_height / 2)
    return res

def polygon_gtth(x0,y0):
    res = [x0,y0]
    res.append(x0 + cell_width)
    res.append(y0 + cell_height / 2)
    res.append(x0)
    res.append(y0 + cell_height / 2)
    return res

def polygon_gtbh(x0,y0):
    res = [x0,y0]
    res.append(x0 + cell_width)
    res.append(y0)
    res.append(x0)
    res.append(y0 + cell_height / 2)
    return res


def polygon_ltth(x0,y0):
    res = [x0,y0]
    res.append(x0 + cell_width)
    res.append(y0 - cell_height / 2)
    res.append(x0 + cell_width)
    res.append(y0)
    return res

def polygon_ltbh(x0,y0):
    res = [x0,y0]
    res.append(x0 + cell_width)
    res.append(y0)
    res.append(x0 + cell_width)
    res.append(y0 + cell_height / 2)
    return res

def gui_close(event):
    sys.exit(0)

def rc():
    return '#%06x' % randrange(0,0xffffff)


def draw_polygon(canvas, coords):
    polygon_id = canvas.create_polygon(coords, fill=rc()) #, dash=(5,2,5,4), outline='#00ff00')
    return polygon_id

def top_row0(x0,y0,canvas):
    res = []
    for _ in range(5):
        gtbh = polygon_gtbh(x0,y0)
        res.append(draw_polygon(canvas, gtbh))
        ltbh = polygon_ltbh(gtbh[2],gtbh[3])
        res.append(draw_polygon(canvas, ltbh))
        x0, y0 = ltbh[2],ltbh[3]
    return res


def odd_row1(x0,y0,canvas):
    res = []
    for _ in range(5):
        lt = polygon_lt(x0,y0)
        res.append(draw_polygon(canvas, lt))
        gt = polygon_gt(lt[2],lt[3])
        res.append(draw_polygon(canvas, gt))
        x0, y0 = gt[2],gt[3]
    return res

def even_row2(x0,y0,canvas):
    res = []
    for _ in range(5):
        gt = polygon_gt(x0,y0)
        res.append(draw_polygon(canvas, gt))
        lt = polygon_lt(gt[2],gt[3])
        res.append(draw_polygon(canvas, lt))
        x0,y0 = lt[2],lt[3]
    return res

def bottom_row28(x0,y0,canvas):
    res = []
    for _ in range(5):
        gtth = polygon_gtth(x0,y0)
        res.append(draw_polygon(canvas, gtth))
        ltth = polygon_ltth(gtth[2], gtth[3])
        res.append(draw_polygon(canvas, ltth))
        x0,y0 = ltth[2],ltth[3]
    return res

def draw_board(x0,y0,canvas):
    res = []
    res.append(top_row0(0,0,canvas))
    x0 = 0
    y0 = cell_height / 2
    for _ in range(13):
      res.append(odd_row1(x0,y0,canvas))
      res.append(even_row2(x0,y0,canvas))
      y0 += cell_height
    res.append(odd_row1(x0,y0,canvas))
    res.append(bottom_row28(x0,y0,canvas))
    return res

def get_colors_from_file(polygons, canvas, filename):
    #expecting polygons to be a 2d array or canvas elements

    img = cv2.imread(filename)
    for row in polygons:
        for p in row:
            # coords[] = [x0,y0, x1,y1, x2,y2]
            coords = [ceil(x * scale_factor / 2) for x in canvas.coords(p)]
            # get distance between x0,y0 and x1,y1 and find middle xM,yM
            # from xM,yM get distance to third corner of triangle x2,y2 and find middle
            xm = (coords[0] + coords[2]) / 2
            ym = (coords[1] + coords[3]) / 2
            xp = (xm + coords[4]) / 2
            yp = (ym + coords[5]) / 2
            cl = img[int(yp)][int(xp)]
            c = (cl[2] << 16) + (cl[1] << 8) + cl[0]
            canvas.itemconfig(p, fill='#%06x' % c)


    



scale_factor = 5
cell_width = 225 / scale_factor
cell_height = 259 / scale_factor
cells_per_row = 10
cells_per_column = 14
canvas_width = cell_width * cells_per_row
canvas_height = cell_height * cells_per_column
canvas_bg_color = '#00ff00'

master = Tk()
canvas = Canvas(master, width=canvas_width, height=canvas_height, bg=canvas_bg_color, borderwidth=0, highlightthickness=0)
canvas.pack()
master.bind('<Q>', gui_close)
master.bind('<q>', gui_close)
polygons = draw_board(0,0,canvas)
if len(sys.argv) > 1:
    get_colors_from_file(polygons, canvas, sys.argv[1])
master.mainloop()
