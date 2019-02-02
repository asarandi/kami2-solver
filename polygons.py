from constants import *

def polygon_gt(x0,y0):    
    res = [x0,y0]

    res.append(x0 + cell_width)
    res.append(y0 + cell_height / 2)

    res.append(x0)
    res.append(y0 + cell_height)
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



def polygon_lt(x0,y0):
    res = [x0,y0]
    res.append(x0 + cell_width)
    res.append(y0 - cell_height / 2)

    res.append(x0 + cell_width)
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
