from . import block_generator
import tkinter as tk
from tkinter import W, NW
from . import constants


class Model:
    def __init__(self):
        self.current_player = 0
        self.selected_block = "-1"
        self.selected_block_segment = "-1"
        self.tiles = [[None for _ in range(constants.BOARD_SIZE_CELLS)]
                      for _ in range(constants.BOARD_SIZE_CELLS)]
        self.picker_tiles = [[None for _ in range(constants.PICKER_COLS)]
                             for _ in range(constants.PICKER_ROWS)]
        self.picker_blocks = {"red": block_generator.generate_blocks(),
                              "green": block_generator.generate_blocks()}
        self.move_flag = False
        self.mouse_xpos = -1
        self.mouse_ypos = -1
        self.white_flag = {0: False, 1: False}
        self.score = {0: -89, 1: -89}

        self.canvas = tk.Canvas(None, width=constants.CANVAS_WIDTH_PX - 4, height=constants.CANVAS_HEIGHT_PX - 4)
        self.canvas.pack()

        self.red_score_label = self.canvas.create_text(
            600, 20, font="Times 16", text="Red Score: " + str(self.score[0]))
        self.green_score_label = self.canvas.create_text(
            750, 20, font="Times 16", text="Green Score: " + str(self.score[1]))

        self.end_game_label = self.canvas.create_text(700, 50, font="Times 16", text="")

        self.resign_button = tk.Button(self.canvas, text='White Flag', anchor=W)
        self.resign_button.configure(width=8, activebackground="#33B5E5", font="Times 12")
        self.canvas.create_window(constants.CANVAS_WIDTH_PX - 100, 5, anchor=NW, window=self.resign_button)
    

    def get_selected_block_segment(self):
        return int(self.selected_block_segment.split("_")[2])


    def get_selected_block(self):
        return int(self.selected_block.split("_")[2])
