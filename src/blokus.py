import tkinter as tk
from tkinter import W, NW
import block
import block_generator
import validator

CELL_SIZE_PX = 36
BOARD_SIZE_CELLS = 14
BOARD_SIZE_PX = BOARD_SIZE_CELLS * CELL_SIZE_PX
DIVIDER_WIDTH_PX = 36
PICKER_HEIGHT_OFFSET_PX = 2 * CELL_SIZE_PX
PICKER_WIDTH_OFFSET_PX = BOARD_SIZE_PX + DIVIDER_WIDTH_PX
PICKER_CELL_SIZE_PX = 18
PICKER_ROWS = 12
PICKER_COLS = 23
PICKER_HEIGHT_PX = PICKER_ROWS * PICKER_CELL_SIZE_PX
PICKER_WIDTH_PX = PICKER_COLS * PICKER_CELL_SIZE_PX
CANVAS_WIDTH_PX = (BOARD_SIZE_CELLS * CELL_SIZE_PX) + \
    (PICKER_COLS * PICKER_CELL_SIZE_PX) + DIVIDER_WIDTH_PX
CANVAS_HEIGHT_PX = BOARD_SIZE_CELLS * CELL_SIZE_PX
PLAYERS = {0: "red", 1: "green"}

current_player = 0
selected_block = "-1"
selected_block_segment = "-1"
tiles = [[None for _ in range(BOARD_SIZE_CELLS)]
         for _ in range(BOARD_SIZE_CELLS)]
picker_tiles = [[None for _ in range(PICKER_COLS)]
                for _ in range(PICKER_ROWS)]
picker_blocks = {"red": block_generator.generate_blocks(),
                 "green": block_generator.generate_blocks()}

move_flag = False
mouse_xpos = -1
mouse_ypos = -1

white_flag = {0: False, 1: False}
score = {0: -89, 1: -89}


def switch_player():
    global selected_block
    selected_block = "-1"

    global current_player
    if white_flag[0] and white_flag[1]:
        current_player = None  # end of the game
        return
    if not white_flag[0] and not white_flag[1]:
        current_player = 1 if current_player == 0 else 0
        return
    if not white_flag[0] and white_flag[1]:
        current_player = 0
        return
    if not white_flag[1] and white_flag[0]:
        current_player = 1
        return


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
    draw_picker_blocks()


def draw_board_grid():
    for i in range(0, BOARD_SIZE_PX + 1, CELL_SIZE_PX):
        canvas.create_line(
            [(i, 0), (i, BOARD_SIZE_PX)])
    for i in range(0, BOARD_SIZE_PX, CELL_SIZE_PX):
        canvas.create_line(
            [(0, i), (BOARD_SIZE_PX, i)])


def draw_picker_blocks():
    height_offset = PICKER_HEIGHT_OFFSET_PX
    for player in PLAYERS:
        for current_block in picker_blocks[PLAYERS[player]]:
            block_segment = 0
            for coord in current_block.coordinates:
                canvas.create_rectangle(
                    PICKER_WIDTH_OFFSET_PX + (
                        current_block.position[1] + coord[1])*PICKER_CELL_SIZE_PX,
                    height_offset + (
                        current_block.position[0] + coord[0])*PICKER_CELL_SIZE_PX,
                    PICKER_WIDTH_OFFSET_PX + (
                        current_block.position[1] + coord[1] + 1)*PICKER_CELL_SIZE_PX,
                    height_offset + (
                        current_block.position[0] + coord[0] + 1)*PICKER_CELL_SIZE_PX,
                    fill=PLAYERS[player], tags=(PLAYERS[player] + "_block_" + str(current_block.index), "block_segment_" + str(block_segment), "picker"))
                block_segment += 1
        height_offset += PICKER_HEIGHT_PX


def on_block_selection(event):
    tags = canvas.gettags("current")
    if not tags or not tags[0].split("_")[0] == PLAYERS[current_player]:
        return
    global selected_block, selected_block_segment, mouse_xpos, mouse_ypos
    mouse_xpos = event.x
    mouse_ypos = event.y
    selected_block = tags[0]
    selected_block_segment = tags[1]
    if event.x > BOARD_SIZE_PX + DIVIDER_WIDTH_PX:
        for item in canvas.find_withtag(selected_block):
            canvas.scale(item, event.x, event.y, 2, 2)


def on_move(event):
    global move_flag, mouse_xpos, mouse_ypos, selected_block
    if move_flag:
        new_xpos, new_ypos = event.x, event.y
        for item in canvas.find_withtag(selected_block):
            if new_xpos <= 0 or new_xpos >= CANVAS_WIDTH_PX - PICKER_CELL_SIZE_PX or new_ypos <= 0 or new_ypos >= CANVAS_HEIGHT_PX:
                if new_xpos <= 0:
                    mouse_xpos = DIVIDER_WIDTH_PX/2
                if new_ypos <= 0:
                    mouse_ypos = DIVIDER_WIDTH_PX/2
                if new_xpos >= CANVAS_WIDTH_PX:
                    mouse_xpos = CANVAS_WIDTH_PX - PICKER_CELL_SIZE_PX * 4
                if new_ypos >= CANVAS_HEIGHT_PX:
                    mouse_ypos = CANVAS_HEIGHT_PX - DIVIDER_WIDTH_PX
                return

            if new_xpos > 0 and new_ypos > 0 and new_xpos < CANVAS_WIDTH_PX - PICKER_CELL_SIZE_PX and new_ypos < CANVAS_HEIGHT_PX:
                canvas.move(item, new_xpos-mouse_xpos, new_ypos-mouse_ypos)

        mouse_xpos = new_xpos
        mouse_ypos = new_ypos
    else:
        move_flag = True
        canvas.tag_raise(selected_block)
        mouse_xpos = event.x
        mouse_ypos = event.y


def on_release(event):
    if selected_block == "-1":
        return
    if mouse_xpos > BOARD_SIZE_PX + DIVIDER_WIDTH_PX:  # replace event.x with mouse_xpos
        for item in canvas.find_withtag(selected_block):
            # replace event.x with mouse_xpos
            canvas.scale(item, mouse_xpos, mouse_ypos, 0.5, 0.5)

    global move_flag
    move_flag = False
    col = int(mouse_xpos/CELL_SIZE_PX)  # replace event.x with mouse_xpos
    row = int(mouse_ypos/CELL_SIZE_PX)

    proposed_coordinates = []
    offset = picker_blocks[PLAYERS[current_player]][int(selected_block.split(
        "_")[2])].coordinates[int(selected_block_segment.split("_")[2])]
    for coord in picker_blocks[PLAYERS[current_player]][int(selected_block.split("_")[2])].coordinates:
        proposed_coordinates.append(
            [row + coord[0] - offset[0], col + coord[1] - offset[1]])
    global tiles
    if validator.placement_is_valid(tiles, proposed_coordinates, current_player):
        for coord in proposed_coordinates:
            tiles[coord[0]][coord[1]] = current_player
        for item in canvas.find_withtag(selected_block):
            canvas.delete(item)
        paint_board()
        global score
        current_tiles_for_player = 0
        for row in tiles:
            current_tiles_for_player += row.count(current_player)
        score[current_player] = -89 + current_tiles_for_player
        update_score()
        switch_player()


def on_resign():
    global white_flag
    white_flag[current_player] = True
    switch_player()


def update_score():
    canvas.itemconfig(red_score_label, text="Red Score: " + str(score[0]))
    canvas.itemconfig(green_score_label, text="Green Score: " + str(score[1]))


root = tk.Tk()
root.title("Blokus Duo")
root.resizable(False, False)
canvas = tk.Canvas(root, width=CANVAS_WIDTH_PX - 4,
                   height=CANVAS_HEIGHT_PX - 4)
canvas.pack()

canvas.bind("<Configure>", configure_canvas)
canvas.bind("<Button-1>", on_block_selection)
# canvas.bind("<Button-3>", on_canvas_click) Todo: bind to rotate?
canvas.tag_bind("picker", '<Button1-Motion>', on_move)
canvas.tag_bind("picker", '<ButtonRelease-1>', on_release)

red_score_label = canvas.create_text(
    600, 20, font="Times 16", text="Red Score: " + str(score[0]))
green_score_label = canvas.create_text(
    750, 20, font="Times 16", text="Green Score: " + str(score[1]))
resign_button = tk.Button(root, text='White Flag', command=on_resign, anchor=W)
resign_button.configure(width=8, activebackground="#33B5E5", font="Times 12")
canvas.create_window(CANVAS_WIDTH_PX - 100, 10,
                     anchor=NW, window=resign_button)
root.mainloop()
