from polygons import *
from random import randrange

def top_row0(x0,y0,canvas):
    res = []
    for _ in range(5):
        gtbh = polygon_gtbh(x0,y0)
        res.append((draw_polygon(canvas, gtbh), 'gtbh'))
        ltbh = polygon_ltbh(gtbh[2],gtbh[3])
        res.append((draw_polygon(canvas, ltbh), 'ltbh'))
        x0, y0 = ltbh[2],ltbh[3]
    return res

def odd_row1(x0,y0,canvas):
    res = []
    for _ in range(5):
        lt = polygon_lt(x0,y0)
        res.append((draw_polygon(canvas, lt), 'lt'))
        gt = polygon_gt(lt[2],lt[3])
        res.append((draw_polygon(canvas, gt), 'gt'))
        x0, y0 = gt[2],gt[3]
    return res

def even_row2(x0,y0,canvas):
    res = []
    for _ in range(5):
        gt = polygon_gt(x0,y0)
        res.append((draw_polygon(canvas, gt), 'gt'))
        lt = polygon_lt(gt[2],gt[3])
        res.append((draw_polygon(canvas, lt), 'lt'))
        x0,y0 = lt[2],lt[3]
    return res

def bottom_row28(x0,y0,canvas):
    res = []
    for _ in range(5):
        gtth = polygon_gtth(x0,y0)
        res.append((draw_polygon(canvas, gtth), 'gtth'))
        ltth = polygon_ltth(gtth[2], gtth[3])
        res.append((draw_polygon(canvas, ltth), 'ltth'))
        x0,y0 = ltth[2],ltth[3]
    return res

def rc():
    return '#%06x' % randrange(0,0xffffff)

def draw_polygon(canvas, coords):
    polygon_id = canvas.create_polygon(coords, fill=rc(), dash=(5,2,5,4), outline='#ffffff')
    return polygon_id

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
