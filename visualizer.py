#!/usr/bin/env python3

from tkinter import *
import sys
import numpy as np
import cv2
from math import ceil, sqrt
import colorsys
import board
from constants import *
from colors import *
import solver

def gui_close(event):
    sys.exit(0)

def board_reset(event):
    global canvas
    global board_config
    global nodes
    print('resetting board to original colors')
    for k,v in board_config.items():
        canvas.itemconfig(k, fill='#%06x' % v)
    for row in nodes:
        for node in row:
            node.color = node.color_copy

def floodfill_adjacent_nodes(node, color):
    global canvas
    global master
    if node.color == color:
        return
    current_color = node.color
    node.color = color
    canvas.itemconfig(node.canvas_id, fill='#%06x' % color)
    for n in node.neighbors:
        if n and n.color == current_color:
            master.after(50, floodfill_adjacent_nodes, n, color)

def find_node_by_canvas_id(canvas_id):
    global nodes
    for row in nodes:
        for node in row:
            if node.canvas_id == canvas_id:
                return node
    return None

def mouse_button_one(event):
    global canvas
    global selected_color
    elements_tuple = canvas.find_closest(event.x, event.y)
    if len(elements_tuple) < 1:
        return
    print('left mouse button clicked at', event.x, event.y, 'element id', elements_tuple[0])
    if selected_color:
        e = elements_tuple[0]
        node = find_node_by_canvas_id(e)
        if node:
            print('floodfill =))')
            floodfill_adjacent_nodes(node, selected_color)

def mouse_button_two(event):
    global canvas
    global selected_color
    print('right mouse button clicked at', event.x, event.y)
    elements_tuple = canvas.find_closest(event.x, event.y)
    if len(elements_tuple) < 1:
        return
    selected_color = int(canvas.itemcget(elements_tuple[0], 'fill')[1:], 16)
    print('selected color is now #%06x' % selected_color)

def board_put_colors(polygons, canvas, filename):
    img = cv2.imread(filename)
    blank = cv2.imread('blank.png')
    pc = get_puzzle_colors(img)
    res = {}
    if not pc:
        return None
    for row in polygons:
        for p, shape in row:
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

class node:
    def __init__ (self, canvas_id, shape, color):
        self.canvas_id = canvas_id
        self.shape = shape
        self.color = color
        self.color_copy = color #for resetting board to original state
        self.neighbors = [None, None, None]

def create_nodes(polygons, board_config):
    nodes = []
    for row in polygons:
        node_row = []
        for p, shape in row:
            node_row.append(node(p, shape, board_config[p]))
        nodes.append(node_row)
    gt = ['gt', 'gtth', 'gtbh']
    lt = ['lt', 'ltth', 'ltbh']
    i = 0
    while i < len(nodes):
        j = 0
        while j < len(nodes[i]):
            n = nodes[i][j]
            if n.shape in gt:
                if j > 0:
                    n.neighbors[0] = nodes[i][j-1]
                if n.shape is not 'gtbh':                  #only in top row, no above neighbor
                    n.neighbors[1] = nodes[i-1][j]
                if n.shape is not 'gtth':                  #only in bottom row, no bottom neighbor
                    n.neighbors[2] = nodes[i+1][j]
            elif n.shape in lt:
                if n.shape is not 'ltbh':                  #only in top row, no top neighbor
                    n.neighbors[0] = nodes[i-1][j]
                if j + 1 < len(nodes[i]):
                    n.neighbors[1] = nodes[i][j+1]
                if n.shape is not 'ltth':                  #only in bottom row, no bottom neighbor
                    n.neighbors[2] = nodes[i+1][j]
            else:
                print('wtf', n.shape)
            j += 1
        i += 1
    return nodes

def get_color_set():
    global nodes
    colors = []
    for row in nodes:
        for node in row:
            if node.color != blank_color:
                if node.color not in colors:
                    colors.append(node.color)
    return colors


def run_solver():
    global nodes
    colors = get_color_set()
    print(colors)
    solver_input = []
    for row in nodes:
        for node in row:
            if node.color == blank_color:
                solver_input.append(-1)
            else:
                solver_input.append(colors.index(node.color))
    return solver.search(solver_input)

blank_color = 0xffffff
selected_color = None
selected_node = None
board_config = None
master = Tk()
canvas = Canvas(master, width=canvas_width, height=canvas_height, bg=canvas_bg_color, borderwidth=0, highlightthickness=0)
canvas.pack()
master.bind('<Q>', gui_close)
master.bind('<q>', gui_close)
master.bind('<r>', board_reset)
master.bind('<Button-1>', mouse_button_one)
master.bind('<Button-2>', mouse_button_two)
master.bind('<Button-3>', mouse_button_two)
polygons = board.draw_board(0,0,canvas)
if len(sys.argv) > 1:
    board_config = board_put_colors(polygons, canvas, sys.argv[1])
else:
    board_config = {}
    for row in polygons:
        for p, shape in row:
            board_config[p] = int(canvas.itemcget(p, 'fill')[1:], 16)
nodes = create_nodes(polygons, board_config)
run_solver()
master.mainloop()
