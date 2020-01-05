import tkinter as tk
import block
import block_generator
import validator

CELL_SIZE_PX = 36
BOARD_SIZE_CELLS = 14
BOARD_SIZE_PX = BOARD_SIZE_CELLS * CELL_SIZE_PX
DIVIDER_WIDTH_PX = 9
PICKER_HEIGHT_OFFSET_PX = 2 * CELL_SIZE_PX
PICKER_WIDTH_OFFSET_PX = BOARD_SIZE_PX + DIVIDER_WIDTH_PX
PICKER_ROWS = 12
PICKER_COLS = 23
PICKER_HEIGHT_PX = PICKER_ROWS * CELL_SIZE_PX
PICKER_WIDTH_PX = PICKER_COLS * CELL_SIZE_PX
CANVAS_WIDTH_PX = (BOARD_SIZE_CELLS + PICKER_COLS) * \
    CELL_SIZE_PX + DIVIDER_WIDTH_PX
CANVAS_HEIGHT_PX = BOARD_SIZE_CELLS * CELL_SIZE_PX
PLAYERS = {0: "red", 1: "green"}

current_player = 0
selected_block = "-1"
tiles = [[None for _ in range(BOARD_SIZE_CELLS)]
         for _ in range(BOARD_SIZE_CELLS)]
picker_tiles = [[None for _ in range(PICKER_COLS)]
                for _ in range(PICKER_ROWS)]
picker_blocks = block_generator.generate_blocks()


def switch_player():
    global current_player
    if current_player == 0:
        current_player = 1
    else:
        current_player = 0
    global selected_block
    selected_block = "-1"
    for item in canvas.find_withtag("picker"):
        canvas.itemconfig(item, fill=PLAYERS[current_player])


def on_canvas_click(event):
    col = int(event.x/CELL_SIZE_PX)
    row = int(event.y/CELL_SIZE_PX)

    if int(selected_block) > -1 and int(selected_block) < len(picker_blocks):
        proposed_coordinates = []
        for coord in picker_blocks[int(selected_block)].coordinates:
            proposed_coordinates.append([row + coord[0], col + coord[1]])
        global tiles
        if validator.placement_is_valid(tiles, proposed_coordinates, current_player):
            for coord in proposed_coordinates:
                tiles[coord[0]][coord[1]] = current_player
            paint_board()
            switch_player()


def paint_board():
    for row in range(BOARD_SIZE_CELLS):
        for col in range(BOARD_SIZE_CELLS):
            if tiles[row][col] == 0 or tiles[row][col] == 1:
                canvas.create_rectangle(
                    (col)*CELL_SIZE_PX,
                    (row)*CELL_SIZE_PX,
                    (col + 1)*CELL_SIZE_PX,
                    (row + 1)*CELL_SIZE_PX,
                    fill=PLAYERS[int(tiles[row][col])])


def configure_canvas(event=None):
    draw_board_grid()
    draw_picker_grid()
    draw_divider()
    draw_picker_blocks()


def draw_board_grid():
    for i in range(0, BOARD_SIZE_PX, CELL_SIZE_PX):
        canvas.create_line(
            [(i, 0), (i, BOARD_SIZE_PX)])
    for i in range(0, BOARD_SIZE_PX, CELL_SIZE_PX):
        canvas.create_line(
            [(0, i), (BOARD_SIZE_PX, i)])


def draw_picker_grid():
    for i in range(PICKER_WIDTH_OFFSET_PX,  PICKER_WIDTH_OFFSET_PX + PICKER_WIDTH_PX, CELL_SIZE_PX):
        canvas.create_line(
            [(i, PICKER_HEIGHT_OFFSET_PX), (i, PICKER_HEIGHT_OFFSET_PX + PICKER_HEIGHT_PX)])
    for i in range(PICKER_HEIGHT_OFFSET_PX, PICKER_HEIGHT_OFFSET_PX + PICKER_HEIGHT_PX, CELL_SIZE_PX):
        canvas.create_line(
            [(PICKER_WIDTH_OFFSET_PX, i), (PICKER_WIDTH_OFFSET_PX + PICKER_WIDTH_PX, i)])


def draw_divider():
    canvas.create_rectangle(
        BOARD_SIZE_PX, 0, BOARD_SIZE_PX + DIVIDER_WIDTH_PX, BOARD_SIZE_PX, fill="gray")


def draw_picker_blocks():
    for current_block in picker_blocks:
        for coord in current_block.coordinates:
            canvas.create_rectangle(
                PICKER_WIDTH_OFFSET_PX + (
                    current_block.position[1] + coord[1])*CELL_SIZE_PX,
                PICKER_HEIGHT_OFFSET_PX + (
                    current_block.position[0] + coord[0])*CELL_SIZE_PX,
                PICKER_WIDTH_OFFSET_PX + (
                    current_block.position[1] + coord[1] + 1)*CELL_SIZE_PX,
                PICKER_HEIGHT_OFFSET_PX + (
                    current_block.position[0] + coord[0] + 1)*CELL_SIZE_PX,
                fill=PLAYERS[current_player], tags=(current_block.index, "picker"))


def on_block_selection(event=None):
    tags = canvas.gettags("current")
    if not tags:
        return
    global selected_block
    selected_block = tags[0]


root = tk.Tk()
root.title("Blokus Duo")
root.resizable(False, False)
canvas = tk.Canvas(root, width=CANVAS_WIDTH_PX - 4,
                   height=CANVAS_HEIGHT_PX - 4)
canvas.pack()
canvas.bind("<Button-1>", on_block_selection)
canvas.bind("<Button-3>", on_canvas_click)
canvas.bind("<Configure>", configure_canvas)

root.mainloop()
