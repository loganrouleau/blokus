from . import block_generator
#from . import blokus
import tkinter as tk
from tkinter import W, NW

# TODO: Extract constants that are duplicated here and in blokus.py
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


class GameState:
    def __init__(self):
        self.current_player = 0
        self.selected_block = "-1"
        self.selected_block_segment = "-1"
        self.tiles = [[None for _ in range(BOARD_SIZE_CELLS)]
                      for _ in range(BOARD_SIZE_CELLS)]
        self.picker_tiles = [[None for _ in range(PICKER_COLS)]
                             for _ in range(PICKER_ROWS)]
        self.picker_blocks = {"red": block_generator.generate_blocks(),
                              "green": block_generator.generate_blocks()}
        self.move_flag = False
        self.mouse_xpos = -1
        self.mouse_ypos = -1
        self.white_flag = {0: False, 1: False}
        self.score = {0: -89, 1: -89}

        self.canvas = tk.Canvas(None, width=CANVAS_WIDTH_PX - 4,
                                height=CANVAS_HEIGHT_PX - 4)
        self.canvas.pack()

        self.red_score_label = self.canvas.create_text(
            600, 20, font="Times 16", text="Red Score: " + str(self.score[0]))
        self.green_score_label = self.canvas.create_text(
            750, 20, font="Times 16", text="Green Score: " + str(self.score[1]))

        self.end_game_label = self.canvas.create_text(
            700, 50, font="Times 16", text="")

        self.resign_button = tk.Button(
            self.canvas, text='White Flag', anchor=W)
        self.resign_button.configure(
            width=8, activebackground="#33B5E5", font="Times 12")
        self.canvas.create_window(CANVAS_WIDTH_PX - 100, 5,
                                  anchor=NW, window=self.resign_button)
