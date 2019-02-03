from constants import *
from math import inf
from heapq import heappush, heappop
from copy import deepcopy
from astar import get_groups

def is_in_group(idx, groups):
    for group in groups:
        if idx in group:
            return True
    return False

def aget_groups(board):
    result = []
    for i, val in enumerate(board):
        if val == blank_idx:
            continue
        if is_in_group(i, result):
            continue
        group = []
        stack = [i]
        while stack:
            current = stack.pop()
            if current not in group:
                group.append(current)
            for n in neighbors[current]:
                if n not in group:
                    if board[n] == board[current]:
                        stack.append(n)
        result.append(group)
#    return result
    return sorted(result, key=lambda x: len(x))

def get_color_set(board):
    result = []
    for i, val in enumerate(board):
        if val != blank_idx:
            if val not in result:
                result.append(val)
    return result

def is_game_over(board):
    return False if len(get_color_set(board)) > 1 else True

def get_moves(board):
    result1 = []
    groups = get_groups(board)
    color_set = get_color_set(board)
    result2 = []

    for group in groups:
        for color in color_set:
            if color != board[group[0]]:
                clone = deepcopy(board)
                for i in group:
                    clone[i] = color
                if len(get_groups(clone)) < len(groups):
                    if len(get_color_set(board)) < len(color_set):
                        result2.append(tuple(clone))
                    else:
                        result1.append(tuple(clone))
    if result2:
        return result2
    else:
        return result1


color_names = ['red2',      'green2',       'yellow2',      'blue2',        'magenta2',     'cyan2',        'white2']
color_codes = ['\033[1;31m','\033[1;32m',   '\033[1;33m',   '\033[1;34m',   '\033[1;35m',   '\033[1;36m',   '\033[1;37m']

def cc(color_idx, cell_idx):
    row = cell_idx // cells_per_row
    col = cell_idx % cells_per_row
    if row % 2 == col % 2:
        c = '\u25b6'
    else:
        c = '\u25c0'
    return color_codes[color_idx] + c + '\033[0;00m';

def print_board_color(board):    
    cpr = cells_per_row
    triangle = 0
    for i in range(cells_per_column):
        row = board[i*cpr:i*cpr+cpr]
        for cell in row:
            print(cc(cell, triangle), end=' ')
            triangle += 1
        print()
    print('-----------------------------------------')

#,'eoc','black','red','green','yellow','blue','magenta','cyan','white']
#,'\033[0;00m','\033[0;30m','\033[0;31m','\033[0;32m','\033[0;33m','\033[0;34m','\033[0;35m','\033[0;36m','\033[0;37m']

def print_board(board):
    cpr = cells_per_row
    for i in range(cells_per_column):
        print(board[i*cpr:i*cpr+cpr])
    print('-----------------------------------------')

def floodfill(board, idx, color):
    group = []
    stack = [idx]
    while stack:
        current = stack.pop()
        if current not in group:
            group.append(current)
        for n in neighbors[current]:
            if n not in group:
                if board[n] == board[current]:
                    stack.append(n)
    result = list(board)
    for i in group:
        result[i] = color
    return tuple(result)

def get_moves_idx(board, idx):
    result = []
    color_set = get_color_set(board)
    for color in color_set:
        if color != board[idx]:
            result.append(floodfill(board, idx, color))
    return result

def a_star_search(root, idx, max_g):
    queue = [(0, 0, tuple(root), None)]
    closed_set = {}
    enqueued = set()
    saved_g = 0
    evaluated = 0
    while queue:
        evaluated += 1
        f, g, current, parent = heappop(queue)
#        if g > saved_g:
#            print('current g', g, 'len closed_set', len(closed_set), 'len queue', len(queue))
#            saved_g = g
        if g + len(get_color_set(current)) -1 >= max_g:
            return None
        if is_game_over(current):
#            print('evaluated',evaluated,'nodes')
            result = []
            result.append(current)
            while parent:
                result.append(parent)
                parent = closed_set[parent]
            return result
        if current in closed_set:
            continue
        closed_set[current] = parent
        moves = get_moves_idx(current, idx)
        for m in moves:
            if m in closed_set:
                continue
            if m in enqueued:
                continue
            enqueued.add(m)
            groups = aget_groups(m)
            mf = (g + 1 + len(get_color_set(m))) * 1000 + len(groups)
            heappush(queue, (mf, g + 1, m, current))
    return None

def search(root, limit=None):
    groups = get_groups(root)
    print('number of color groups', len(groups))
    max_g = inf
    result = None
    start_idx = None
    for group in groups:
        steps = a_star_search(root, group[0], max_g)
        if steps and len(steps) < max_g:
            start_idx = group[0]
            max_g = len(steps)
            result = steps
            print('found solution of length', max_g-1)    # minus one because includes root
            if limit and max_g-1 <= limit:
                break
    for step in result:
        print_board_color(step)
    print('solution of length', len(result) - 1)
    result.reverse()
    return start_idx, result


