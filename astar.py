from heapq import heappush, heappop
from copy import deepcopy
from constants import *

def is_in_group(idx, groups):
    for group in groups:
        if idx in group:
            return True
    return False

def get_groups(board):
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
    result = []
    groups = get_groups(board)
    color_set = get_color_set(board)
    for group in groups:
        for color in color_set:
            if color != board[group[0]]:
                clone = deepcopy(board)
                for i in group:
                    clone[i] = color
                result.append(tuple(clone))
    return result


color_names = ['red2',      'green2',       'yellow2',      'blue2',        'magenta2',     'cyan2',        'white2']
color_codes = ['\033[1;31m','\033[1;32m',   '\033[1;33m',   '\033[1;34m',   '\033[1;35m',   '\033[1;36m',   '\033[1;37m']

def cc(idx):
    return color_codes[idx] + 'o' + '\033[0;00m';
def print_board_color(board):    
    cpr = cells_per_row
    for i in range(cells_per_column):
        row = board[i*cpr:i*cpr+cpr]
        for cell in row:
            print(cc(cell), end=' ')
        print()
    print('-----------------------------------------')

#,'eoc','black','red','green','yellow','blue','magenta','cyan','white']
#,'\033[0;00m','\033[0;30m','\033[0;31m','\033[0;32m','\033[0;33m','\033[0;34m','\033[0;35m','\033[0;36m','\033[0;37m']

def print_board(board):
    cpr = cells_per_row
    for i in range(cells_per_column):
        print(board[i*cpr:i*cpr+cpr])
    print('-----------------------------------------')
    

def search(root, max_g=None):
#    print(len(root))
#    print(root)
#    print(neighbors)
#    groups = get_groups(root)
#    print('count of groups', len(groups))
#    for g in groups:
#        print(len(g))
#    moves = get_moves(root)
#    for m in moves:
#        print_board(m)
#        print()

    queue = [(0, len(get_groups(root)), 0, tuple(root), None)]
    print('number of groups', queue[0][1])
    closed_set = {}
    enqueued = set()
    saved_g = -1
    while queue:
        f, len_groups, g, current, parent = heappop(queue)
        if g > saved_g:
            print('current g', g, 'len closed_set', len(closed_set), 'len queue', len(queue))
            saved_g = g
        if is_game_over(current):
            result = [current]
            while parent:
                result.append(parent)
                parent = closed_set[parent]
            for board in result:
                print_board_color(board)
            print('solution of length', len(result) - 1)
            result.reverse()
            return 'done', result
        if current in closed_set:
            continue
        closed_set[current] = parent
        moves = get_moves(list(current))
        for m in moves:
            if m in closed_set:
                continue
            if m in enqueued:
                continue
            enqueued.add(m)
            groups = get_groups(m)
            mf = (g + 1 + len(get_color_set(m))) * 1000 + len(groups)

            heappush(queue, (mf, len(groups), g + 1, m, current))
    return 'solution not found'
