scale_factor = 5
cell_width = 225 / scale_factor
cell_height = 259 / scale_factor
cells_per_row = 10
cells_per_column = 29
board_size = cells_per_row * cells_per_column
canvas_width = cell_width * cells_per_row
canvas_height = cell_height * (cells_per_column // 2)
canvas_bg_color = '#00ff00'
cell_outline = '#fff'
cell_dash = (5,2,5,4)
color_bar_offset_y = 1901
color_bar_offset_x = 450
color_bar_width = 675
color_distance_threshold = 10
blank_board_file = 'blank.png'
color_sample_square = 5
blank_distance_threshold = 1
blank_cell_color = 0xffffff

#neighbors[idx] will be a list of cells adjacted to idx
neighbors = []
for idx in range(board_size):
    adjacent = []
    row = idx // cells_per_row
    col = idx % cells_per_row
    if row % 2 == col % 2:  #gt
        if col > 0:
            adjacent.append(idx-1)  #left neighbor
        if row > 0:
            adjacent.append(idx-cells_per_row)  #above
        if row + 1 < cells_per_column:
            adjacent.append(idx+cells_per_row)  #below
    else:   #lt
        if row > 0:
            adjacent.append(idx-cells_per_row)  #above
        if col + 1 < cells_per_row: #right neighbor
            adjacent.append(idx+1)
        if row + 1 < cells_per_column:  #below
            adjacent.append(idx+cells_per_row)
    neighbors.append(adjacent)
