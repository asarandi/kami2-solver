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
import astar
import search

from heapq import heappush, heappop
from copy import deepcopy
from constants import *
from math import inf

blank_idx = -1
def get_cell_group_index(cell, all_groups):
    for i, group in enumerate(all_groups):
        if cell in group:
            return i
    return None

def get_group_neighbors(board, all_groups, current_group):

    #given a group G, return its neighboring groups
    #returns a list of indices

    result = []
    for cell in current_group:
        for n in neighbors[cell]:
            if board[n] != blank_idx and n not in current_group:
                ng = get_cell_group_index(n, all_groups)
                if ng != None and ng not in result:
                    result.append(ng)
    return result

def make_group_neighbors_list(board, all_groups):
    result = []
    for current_group in all_groups:
        result.append(get_group_neighbors(board, all_groups, current_group))
    return result

def make_groups_list(board):
    all_groups = []
    for i, val in enumerate(board):
        if val == blank_idx:
            continue
        if get_cell_group_index(i, all_groups) != None:
            continue
        current_group = []
        stack = [i]
        while stack:
            current_cell = stack.pop()
            if current_cell not in current_group:
                current_group.append(current_cell)
            for n in neighbors[current_cell]:
                if board[n] == board[current_cell]:
                    if n not in current_group:
                        stack.append(n)
        all_groups.append(current_group)
    return all_groups

def get_groups_and_color_counts(board, all_groups):
    counts = {}
    for current_group in all_groups:
        color = board[current_group[0]]
        if color not in counts:
            counts[color] = 0
        counts[color] += 1
    result = {}
    for current_group in all_groups:
        color = board[current_group[0]]
        result[tuple(current_group)] = counts[color]
    return result

def list_all_groups_by_color_rating(board):
    all_groups = make_groups_list(board)
    color_counts = get_groups_and_color_counts(board, all_groups)
    sorted_groups = sorted(color_counts.items(), key=lambda kv: kv[1])
    all_groups = []
    for group, rating in sorted_groups:
        all_groups.append(group)
    return all_groups

def get_color_options_for_each_group(board, all_groups):
    all_neighbors = make_group_neighbors_list(board, all_groups)
    result = []
    for i, current_group in enumerate(all_groups):
        color_options = []
        for neighbor in all_neighbors[i]:
            n = all_groups[neighbor]
            color = board[n[0]]
            if color not in color_options:
                color_options.append(color)
        result.append(color_options)
    return result

def get_distances_for_each_group(board):
    def distance_between_groups(root):
        distances = [inf for x in range(len(all_neighbors))]
        queue = [root]
        distances[root] = 0
        while queue:
            current_node = queue.pop()            
            for n in all_neighbors[current_node]:
                if distances[n] == inf:
                    distances[n] = distances[current_node] + 1
                    queue.append(n)
        return distances
    all_groups = make_groups_list(board)#list_all_groups_by_color_rating(board)
    all_neighbors = make_group_neighbors_list(board, all_groups)
    result = []
    for i in range(len(all_groups)):
        dist = distance_between_groups(i)
        result.append(dist)
    return result

def get_moves(board):
    result1 = []
    result2 = []
    result3 = []
    all_groups = list_all_groups_by_color_rating(board)
    board_color_counts = len(get_color_counts(board))
    board_distance = get_max_distance(board)
    color_options = get_color_options_for_each_group(board, all_groups)
    for i, current_group in enumerate(all_groups):
        for color in color_options[i]:
            clone = deepcopy(board)
            for cell in current_group:
                clone[cell] = color
            if len(get_color_counts(clone)) < board_color_counts:
                result1.append(tuple(clone))
            else:
                clone_distance = get_max_distance(clone)
                if clone_distance < board_distance:
                    heappush(result2, (clone_distance, tuple(clone)))
                else:
                    result3.append(tuple(clone))
    if result1:
        return result1
    elif result2:
        res = []
        while result2:
            d, clone = heappop(result2)
            res.append(clone)
        return res    
    else:
        return result3

def get_color_counts(board):
    color_counts = {}
    for cell in board:
        if cell == blank_idx:
            continue
        if cell not in color_counts:
            color_counts[cell] = 0
        color_counts[cell] += 1
    return color_counts

def is_game_over(board):
    color_counts = {}
    for cell in board:
        if cell == blank_idx:
            continue
        if cell not in color_counts:
            color_counts[cell] = 0
        color_counts[cell] += 1
        if len(color_counts) > 1:
            return False
    return True

def print_board_color(board):
    def cc(color_idx, cell_idx):
        color_names = ['red2','green2','yellow2','blue2','magenta2','cyan2','white2']
        color_codes = ['\033[1;31m','\033[1;32m','\033[1;33m','\033[1;34m','\033[1;35m','\033[1;36m','\033[1;37m']
        row = cell_idx // cells_per_row
        col = cell_idx % cells_per_row
        if row % 2 == col % 2:
            c = '\u25b6'    #utf8 right pointing triangle
        else:
            c = '\u25c0'    #utf8 left pointing triangle
        return color_codes[color_idx] + c + '\033[0;00m';
    cpr = cells_per_row
    idx = 0
    for i in range(cells_per_column):
        row = board[i*cpr:i*cpr+cpr]
        for cell in row:
            print(cc(cell, idx), end=' ')
            idx += 1
        print()
    print('-----------------------------------------')

def search(root, max_g=None):
    print('number of color groups', len(make_groups_list(root)))
    queue = [(0, 0, tuple(root), None)]
    closed_set = {}
    enqueued = set()
    current_depth = -1
    evaluated = 0

#    moves = get_moves(list(root))
#    i = 0
#    print_board_color
#    for m in moves:
#        print_board_color(m)
#        print(i)
#        i += 1
#
#    moves.insert(0, root)
#    return 0,moves



    while queue:
        evaluated += 1
        f, g, current, parent = heappop(queue)
        if g > current_depth:
            print_board_color(current)
            print('current depth', g, 'closed set count', len(closed_set), 'queue count', len(queue))
            print('max distance', get_max_distance(current))
            current_depth = g
        if is_game_over(current):
            result = [current]
            while parent:
                result.append(parent)
                parent = closed_set[parent]
            for board in result:
                print_board_color(board)
            print('solution of length', len(result) - 1)
            print('evaluated nodes', evaluated)
            result.reverse()
            return 0, result
        if current in closed_set:
            continue
        closed_set[current] = parent
        moves = get_moves(list(current))
        for m in moves:
            if m in closed_set:
                continue
            if m in enqueued:
                continue
            cc = len(get_color_counts(m))
            if max_g != None and cc + g > max_g:
                continue
            enqueued.add(m)
            mf = g + cc + get_max_distance(m) # + len(make_groups_list(m))
            heappush(queue, (mf, g + 1, m, current))
            
    print('solution not found')
    return 0, [root]




########################################################################################

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

def board_set_colors(indices):
    for i, val in enumerate(indices):
        if val == -1:
            cell_fill = blank_cell_color
        else:
            cell_fill = rgbi(palette[val])
        canvas.itemconfig(polygons[i], fill='#%06x' % cell_fill)

def floodfill_adjacent_cells(cell_idx, color_idx):
    current_color = canvas.itemcget(polygons[cell_idx], 'fill')
    new_color = '#%06x' % rgbi(palette[color_idx])
    if current_color != new_color:
        canvas.itemconfig(polygons[cell_idx], fill=new_color)
        for n in neighbors[cell_idx]:
            neighbor_color = canvas.itemcget(polygons[n], 'fill')
            if neighbor_color == current_color:
                master.after(50, floodfill_adjacent_cells, n, color_idx)

def solution_next_step():
    global solution_index
    if solution_index + 1 < len(solution):
        solution_index += 1 # XXX
        board_set_colors(solution[solution_index])
#        solution_index += 1        
#        for i in range(len(solution[solution_index])):
#            if solution[solution_index][i] != solution[solution_index-1][i]:
#                return floodfill_adjacent_cells(i, solution[solution_index][i])
    else:
        print('no next frame')

def solution_previous_step():
    global solution_index
    if solution_index > 0:
        solution_index -= 1
        board_set_colors(solution[solution_index])
    else:
        print('no previous frame')

def user_keyrelease(event):
    global solution_index
    key = event.keysym.lower()
    if key in ['q', 'escape']:
        sys.exit(0)
    elif key == 'right':
        solution_next_step()
    elif key == 'left':
        solution_previous_step()
    elif key == 'r':
        solution_index = 0
        board_set_colors(indices)

def mouse_button_one(event):
    elements_tuple = canvas.find_closest(event.x, event.y)
    if len(elements_tuple) < 1:
        return
        
    distances = get_distances_for_each_group(indices)
    for dist in distances:
        print(sum(dist), dist)
    element_id = elements_tuple[0]
    cell = polygons.index(element_id)
    print('you clicked cell idx', cell)
    all_groups = make_groups_list(indices)
    for i, group in enumerate(all_groups):
        if cell in group:
            print('cell',cell,'belongs in group idx', i)
            print(sum(distances[i]), distances[i])
            break

#    print('left mouse button clicked at', event.x, event.y, 'element id', elements_tuple[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='kami2 solver')
    parser.add_argument('-a', help='exhaustive search', action='store_true')
    parser.add_argument('-m', help='moves limit', type=int)
    parser.add_argument('file', help='input file', type=argparse.FileType('rb'))
    args = parser.parse_args()

    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, width=canvas_width, height=canvas_height, bg=canvas_bg_color, borderwidth=0, highlightthickness=0)
    canvas.pack()    
    polygons = draw_polygons(canvas)
    palette, indices = get_palette_indices_from_file(args.file)
    board_set_colors(indices)
#    if args.a:
#        starting_cell, solution = search.search(indices, args.m)
#    else:
#        starting_cell, solution = solver.search(indices, args.m)
#    solution_index = 0
    master.bind('<KeyRelease>', user_keyrelease)
    master.bind('<ButtonPress>', mouse_button_one)
    
    master.mainloop()
