from constants import *
from random import randrange

def get_coords_for_shape(s,x,y):
    w = cell_width
    h = cell_height
    shapes = {
        'gt'    : [    x, y,    x+w, y+h/2,     x,   y+h      ],
        'gtth'  : [    x, y,    x+w, y+h/2,     x,   y+h/2    ],
        'gtbh'  : [    x, y,    x+w, y,         x,   y+h/2    ],
        'lt'    : [    x, y,    x+w, y-h/2,     x+w, y+h/2    ],
        'ltth'  : [    x, y,    x+w, y-h/2,     x+w, y        ],
        'ltbh'  : [    x, y,    x+w, y,         x+w, y+h/2    ]
    }
    return shapes[s]

def get_shape_at_index(idx):
    row = idx // cells_per_row
    col = idx % cells_per_row
    if row % 2 == col % 2:
        if row == 0:
            return 'gtbh'
        elif row == cells_per_column - 1:
            return 'gtth'
        else:
            return 'gt'
    else:
        if row == 0:
            return 'ltbh'
        elif row == cells_per_column - 1:
            return 'ltth'
        else:
            return 'lt'

def random_color():
    return '#%06x' % randrange(0,0xffffff)

def make_polygon_coords_array():
    result = []
    y = 0
    for i in range(cells_per_column):
        x = 0
        for j in range(cells_per_row):
            s = get_shape_at_index(i * cells_per_row + j)
            coords = get_coords_for_shape(s,x,y)
            result.append(coords)
            x,y = coords[2], coords[3]
        if i % 2 == 0:
            if i == 0:
                y = cell_height / 2
            else:
                y += cell_height
    return result

def draw_polygons(canvas):
    result = []
    coords = make_polygon_coords_array()
    for c in coords:
        polygon_id = canvas.create_polygon(c, fill=random_color(), dash=cell_dash, outline=cell_outline)
        result.append(polygon_id)
    return result
