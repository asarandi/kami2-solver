#!/usr/bin/env python3

import numpy as np
import sys
from PIL import Image
from constants import *
import tkinter
from canvas import *
from colors import get_puzzle_colors as get_palette_from_image, color_distance, rgbi
from math import ceil
import argparse
import solver

def get_palette_indices_from_file(filename):
    indices = []
    csq = color_sample_square
    polygons = make_polygon_coords_array()
    img = np.array(Image.open(filename))
    blank = np.array(Image.open(blank_board_file))
    palette = get_palette_from_image(img)
    for p in polygons:
        coords = [ceil(x * scale_factor / 2) for x in p]
        xm = (coords[0] + coords[2]) / 2    #midpoint of 1st side
        ym = (coords[1] + coords[3]) / 2
        x = int((xm + coords[4]) / 2)      #half median
        y = int((ym + coords[5]) / 2)
        img_sq = img[y-csq:y+csq, x-csq:x+csq]
        img_sq_color = np.mean(img_sq, axis=(0,1))
        blank_sq = blank[y-csq:y+csq, x-csq:x+csq]
        blank_sq_color = np.mean(blank_sq, axis=(0,1))
        color_distances = []
        for color in palette:
            color_distances.append(color_distance(color, img_sq_color))
        blank_distance = color_distance(blank_sq_color, img_sq_color)
        if blank_distance < blank_distance_threshold:
            indices.append(-1)
        else:
            idx = color_distances.index(min(color_distances))
            indices.append(idx)
    return palette, indices

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='kami2 solver')
    parser.add_argument('-m', help='moves', type=int)
    parser.add_argument('file', help='input file', type=argparse.FileType('rb'))
    args = parser.parse_args()

    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, width=canvas_width, height=canvas_height, bg=canvas_bg_color, borderwidth=0, highlightthickness=0)
    canvas.pack()
    polygons = draw_polygons(canvas)
    palette, indices = get_palette_indices_from_file(args.file)
    solver.search(indices, args.m)

    for i, val in enumerate(indices):
        if val == -1:
            cell_fill = blank_cell_color
        else:
            cell_fill = rgbi(palette[val])
        canvas.itemconfig(polygons[i], fill='#%06x' % cell_fill)
    master.mainloop()
