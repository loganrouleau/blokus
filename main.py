import tkinter as tk
import block
import block_generator

INTERVAL_UNIT = 36
GAMEBOARD_ROWS = 14
GAMEBOARD_COLS = 14
GAMEBOARD_WIDTH = GAMEBOARD_COLS * INTERVAL_UNIT
GAMEBOARD_HEIGHT = GAMEBOARD_ROWS * INTERVAL_UNIT
PICKER_ROWS = 12
PICKER_COLS = 23
PICKER_WIDTH = PICKER_COLS * INTERVAL_UNIT
PICKER_HEIGHT = PICKER_ROWS * INTERVAL_UNIT
PLAYERS = {0: "red", 1: "green"}

current_player = 0
tiles = [[None for _ in range(GAMEBOARD_COLS)] for _ in range(GAMEBOARD_ROWS)]
picker_tiles = [[None for _ in range(PICKER_COLS)]
                for _ in range(PICKER_ROWS)]


def switch_player():
    global current_player
    if current_player == 0:
        current_player = 1
    else:
        current_player = 0


def on_canvas_click(event):
    col = int(event.x/INTERVAL_UNIT)
    row = int(event.y/INTERVAL_UNIT)
    # If the tile is not filled, create a rectangle
    if not tiles[row][col]:
        tiles[row][col] = gameboard_canvas.create_rectangle(
            col*INTERVAL_UNIT,
            row*INTERVAL_UNIT,
            (col+1)*INTERVAL_UNIT,
            (row+1)*INTERVAL_UNIT, fill=PLAYERS[current_player])
        switch_player()


def draw_gameboard_grid(event=None):
    for i in range(0, GAMEBOARD_WIDTH, INTERVAL_UNIT):
        gameboard_canvas.create_line(
            [(i, 0), (i, GAMEBOARD_HEIGHT)])
    for i in range(0, GAMEBOARD_HEIGHT, INTERVAL_UNIT):
        gameboard_canvas.create_line(
            [(0, i), (GAMEBOARD_WIDTH, i)])


def configure_picker(event=None):
    draw_picker_grid(event)
    draw_picker_blocks()


def draw_picker_grid(event=None):
    for i in range(0,  PICKER_WIDTH, INTERVAL_UNIT):
        picker_canvas.create_line(
            [(i, 0), (i, PICKER_HEIGHT)])
    for i in range(0, PICKER_HEIGHT, INTERVAL_UNIT):
        picker_canvas.create_line(
            [(0, i), (PICKER_WIDTH, i)])


def draw_picker_blocks():
    picker_blocks = block_generator.generate_blocks()
    for current_block in picker_blocks:
        for coord in current_block.coordinates:
            picker_canvas.create_rectangle(
                (current_block.position[1] + coord[1])*INTERVAL_UNIT,
                (current_block.position[0] + coord[0])*INTERVAL_UNIT,
                (current_block.position[1] + coord[1] + 1)*INTERVAL_UNIT,
                (current_block.position[0] + coord[0] + 1)*INTERVAL_UNIT,
                fill=PLAYERS[current_player], tag=current_block.index)


def on_block_selection(event=None):
    tags = picker_canvas.gettags("current")
    if not tags:
        return
    item = tags[0]
    print("selected item " + item)


root = tk.Tk()
root.title("Blokus Duo")
root.resizable(False, False)
gameboard_canvas = tk.Canvas(root, width=GAMEBOARD_WIDTH - 4,
                             height=GAMEBOARD_HEIGHT - 4, background='white')
gameboard_canvas.pack(side="left")
gameboard_canvas.bind("<Button-1>", on_canvas_click)
gameboard_canvas.bind('<Configure>', draw_gameboard_grid)
picker_canvas = tk.Canvas(root, width=PICKER_WIDTH - 4,
                          height=PICKER_HEIGHT - 4, background='black')
picker_canvas.pack(side="right")
picker_canvas.bind("<Button-1>", on_block_selection)
picker_canvas.bind("<Configure>", configure_picker)

root.mainloop()
