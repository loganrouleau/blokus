import tkinter as tk
import block

GAMEBOARD_ROWS = 14
GAMEBOARD_COLS = 14
INTERVAL_UNIT = 35.7142857143
GAMEBOARD_WIDTH = GAMEBOARD_COLS * INTERVAL_UNIT
GAMEBOARD_HEIGHT = GAMEBOARD_ROWS * INTERVAL_UNIT
PICKER_ROWS = 12
PICKER_COLS = 23
PICKER_WIDTH_INTERVAL = 36.3405771017
PICKER_HEIGHT_INTERVAL = 36.1594202895
PICKER_WIDTH = PICKER_COLS * PICKER_WIDTH_INTERVAL
PICKER_HEIGHT = PICKER_ROWS * PICKER_HEIGHT_INTERVAL

token_colour = "red"
tiles = [[None for _ in range(GAMEBOARD_COLS)] for _ in range(GAMEBOARD_ROWS)]
picker_tiles = [[None for _ in range(PICKER_COLS)]
                for _ in range(PICKER_ROWS)]


# def create_blocks():
#     blocks = []
#     for i in range(5):
#         blocks.append(block.Block(i))
#         print(blocks[i].coordinates)


def finish_turn():
    global token_colour
    if token_colour == "red":
        token_colour = "green"
    elif token_colour == "green":
        token_colour = "red"
    else:
        print("Error")


def on_canvas_click(event):
    col_width = gameboard_canvas.winfo_width()/GAMEBOARD_COLS
    row_height = gameboard_canvas.winfo_height()/GAMEBOARD_ROWS
    col = int(event.x//col_width)
    row = int(event.y//row_height)
    # If the tile is not filled, create a rectangle
    if not tiles[row][col]:
        tiles[row][col] = gameboard_canvas.create_rectangle(
            col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill=token_colour)
        finish_turn()


def draw_gameboard_grid(event=None):
    w = gameboard_canvas.winfo_width()
    h = gameboard_canvas.winfo_height()
    print(GAMEBOARD_HEIGHT)
    print(GAMEBOARD_WIDTH)
    print(h)
    print(w)
    for i in range(0, w, int(w/GAMEBOARD_COLS)):
        gameboard_canvas.create_line(
            [(i, 0), (i, h)], tag='grid_line')
    for i in range(0, h, int(h/GAMEBOARD_ROWS)):
        gameboard_canvas.create_line(
            [(0, i), (w, i)], tag='grid_line')


def configure_picker(event=None):
    draw_picker_grid(event)
    draw_picker_blocks()


def draw_picker_grid(event=None):
    w = picker_canvas.winfo_width()
    h = picker_canvas.winfo_height()
    print(PICKER_HEIGHT)
    print(PICKER_WIDTH)
    print(h)
    print(w)
    for i in range(0,  w, int(w/PICKER_COLS)):
        picker_canvas.create_line([(i, 0), (i, h)], tag='grid_line')
    for i in range(0, h, int(h/PICKER_ROWS)):
        picker_canvas.create_line([(0, i), (w, i)], tag='grid_line')


def draw_picker_blocks():
    picker_blocks = [block.Block(0, [0, 3], [[0, 0]]),
                     block.Block(1, [0, 7], [[0, 0], [0, 1]]),
                     block.Block(2, [0, 12], [[0, 0], [0, 1], [1, 1]]),
                     block.Block(3, [0, 17], [[0, 0], [0, 1], [0, 2]]),
                     block.Block(4, [2, 0], [[0, 0], [0, 1], [1, 0], [1, 1]]),
                     block.Block(5, [2, 4], [[0, 1], [1, 0], [1, 1], [1, 2]]),
                     block.Block(5, [2, 9], [[0, 0], [0, 1], [0, 2], [0, 3]])]
    col_width = int(picker_canvas.winfo_width()/PICKER_COLS)
    row_height = int(picker_canvas.winfo_height()/PICKER_ROWS)
    for current_block in picker_blocks:
        for coord in current_block.coordinates:
            picker_canvas.create_rectangle(
                (current_block.position[1] + coord[1])*col_width,
                (current_block.position[0] + coord[0])*row_height,
                (current_block.position[1] + coord[1]+1)*col_width,
                (current_block.position[0] + coord[0]+1)*row_height,
                fill=token_colour)


root = tk.Tk()
root.title("Blokus Duo")
root.resizable(False, False)
gameboard_canvas = tk.Canvas(root, width=GAMEBOARD_WIDTH,
                             height=GAMEBOARD_HEIGHT, background='white')
gameboard_canvas.pack(side="left")
gameboard_canvas.bind("<Button-1>", on_canvas_click)
gameboard_canvas.bind('<Configure>', draw_gameboard_grid)
picker_canvas = tk.Canvas(root, width=PICKER_WIDTH,
                          height=PICKER_HEIGHT, background='white')
picker_canvas.pack(side="right")
picker_canvas.bind("<Configure>", configure_picker)

# create_blocks()

root.mainloop()
