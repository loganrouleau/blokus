import tkinter as tk
from tkinter import W, NW
from . import block
from . import block_generator
from . import validator
from . import transformer


class BlokusApp(tk.Frame):
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

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.current_player = 0
        self.selected_block = "-1"
        self.selected_block_segment = "-1"
        self.tiles = [[None for _ in range(self.BOARD_SIZE_CELLS)]
                      for _ in range(self.BOARD_SIZE_CELLS)]
        self.picker_tiles = [[None for _ in range(self.PICKER_COLS)]
                             for _ in range(self.PICKER_ROWS)]
        self.picker_blocks = {"red": block_generator.generate_blocks(),
                              "green": block_generator.generate_blocks()}
        self.move_flag = False
        self.mouse_xpos = -1
        self.mouse_ypos = -1
        self.white_flag = {0: False, 1: False}
        self.score = {0: -89, 1: -89}

        self.canvas = tk.Canvas(master, width=self.CANVAS_WIDTH_PX - 4,
                                height=self.CANVAS_HEIGHT_PX - 4)
        self.canvas.pack()

        self.canvas.bind("<Configure>", self.configure_canvas)
        self.canvas.bind("<Button-1>", self.on_block_selection)  # left click
        self.canvas.bind("<Button-2>", self.on_flip)  # middle click
        self.canvas.bind("<Button-3>", self.on_rotate)  # right click
        self.canvas.tag_bind("picker", '<Button1-Motion>', self.on_move)
        self.canvas.tag_bind("picker", '<ButtonRelease-1>', self.on_release)

        self.red_score_label = self.canvas.create_text(
            600, 20, font="Times 16", text="Red Score: " + str(self.score[0]))
        self.green_score_label = self.canvas.create_text(
            750, 20, font="Times 16", text="Green Score: " + str(self.score[1]))

        self.end_game_label = self.canvas.create_text(
            700, 50, font="Times 16", text="")

        self.resign_button = tk.Button(self.canvas, text='White Flag',
                                       command=self.on_resign, anchor=W)
        self.resign_button.configure(
            width=8, activebackground="#33B5E5", font="Times 12")
        self.canvas.create_window(self.CANVAS_WIDTH_PX - 100, 5,
                                  anchor=NW, window=self.resign_button)

    def switch_player(self):
        self.selected_block = "-1"
        if self.white_flag[0] and self.white_flag[1]:
            self.current_player = None  # end of the game
            self.resign_button['state'] = 'disabled'
            # resign_button['text']='Restart'
            win_team = self.PLAYERS[0] if self.score[0] > self.score[1] else self.PLAYERS[1]
            self.canvas.itemconfig(
                self.end_game_label, text="GG! Player " + win_team + " has won!")
            if self.score[0] == self.score[1]:
                self.canvas.itemconfig(
                    self.end_game_label, text="GG! It's a tie!")
            return
        if not self.white_flag[0] and not self.white_flag[1]:
            self.current_player = 1 if self.current_player == 0 else 0
            return
        if not self.white_flag[0] and self.white_flag[1]:
            self.current_player = 0
            return
        if not self.white_flag[1] and self.white_flag[0]:
            self.current_player = 1
            return

    def paint_board(self):
        for row in range(self.BOARD_SIZE_CELLS):
            for col in range(self.BOARD_SIZE_CELLS):
                if self.tiles[row][col] == 0 or self.tiles[row][col] == 1:
                    self.canvas.create_rectangle(
                        (col)*self.CELL_SIZE_PX,
                        (row)*self.CELL_SIZE_PX,
                        (col + 1)*self.CELL_SIZE_PX,
                        (row + 1)*self.CELL_SIZE_PX,
                        fill=self.PLAYERS[int(self.tiles[row][col])])

    def configure_canvas(self, event=None):
        self.draw_board_grid()
        self.draw_picker_blocks()

    def draw_board_grid(self):
        for i in range(0, self.BOARD_SIZE_PX + 1, self.CELL_SIZE_PX):
            self.canvas.create_line(
                [(i, 0), (i, self.BOARD_SIZE_PX)])
        for i in range(0, self.BOARD_SIZE_PX, self.CELL_SIZE_PX):
            self.canvas.create_line(
                [(0, i), (self.BOARD_SIZE_PX, i)])

    def draw_picker_blocks(self):
        height_offset = self.PICKER_HEIGHT_OFFSET_PX
        for player in self.PLAYERS:
            for current_block in self.picker_blocks[self.PLAYERS[player]]:
                block_segment = 0
                for coord in current_block.coordinates:
                    self.canvas.create_rectangle(
                        self.PICKER_WIDTH_OFFSET_PX + (
                            current_block.position[1] + coord[1])*self.PICKER_CELL_SIZE_PX,
                        height_offset + (
                            current_block.position[0] + coord[0])*self.PICKER_CELL_SIZE_PX,
                        self.PICKER_WIDTH_OFFSET_PX + (
                            current_block.position[1] + coord[1] + 1)*self.PICKER_CELL_SIZE_PX,
                        height_offset + (
                            current_block.position[0] + coord[0] + 1)*self.PICKER_CELL_SIZE_PX,
                        fill=self.PLAYERS[player], tags=(self.PLAYERS[player] + "_block_" + str(current_block.index), "block_segment_" + str(block_segment), "picker"))
                    block_segment += 1
            height_offset += self.PICKER_HEIGHT_PX

    def on_block_selection(self, event):
        tags = self.canvas.gettags("current")
        if self.current_player == None:
            return
        if not tags or not tags[0].split("_")[0] == self.PLAYERS[self.current_player]:
            return
        self.mouse_xpos = event.x
        self.mouse_ypos = event.y
        self.selected_block = tags[0]
        self.selected_block_segment = tags[1]
        if event.x > self.BOARD_SIZE_PX + self.DIVIDER_WIDTH_PX:
            for item in self.canvas.find_withtag(self.selected_block):
                self.canvas.scale(item, event.x, event.y, 2, 2)

    def on_move(self, event):
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y
            for item in self.canvas.find_withtag(self.selected_block):
                if new_xpos <= 0 or new_xpos >= self.CANVAS_WIDTH_PX - self.PICKER_CELL_SIZE_PX or new_ypos <= 0 or new_ypos >= self.CANVAS_HEIGHT_PX:
                    if new_xpos <= 0:
                        self.mouse_xpos = self.DIVIDER_WIDTH_PX/2
                    if new_ypos <= 0:
                        self.mouse_ypos = self.DIVIDER_WIDTH_PX/2
                    if new_xpos >= self.CANVAS_WIDTH_PX:
                        self.mouse_xpos = self.CANVAS_WIDTH_PX - self.PICKER_CELL_SIZE_PX * 4
                    if new_ypos >= self.CANVAS_HEIGHT_PX:
                        self.mouse_ypos = self.CANVAS_HEIGHT_PX - self.DIVIDER_WIDTH_PX
                    return

                if new_xpos > 0 and new_ypos > 0 and new_xpos < self.CANVAS_WIDTH_PX - self.PICKER_CELL_SIZE_PX and new_ypos < self.CANVAS_HEIGHT_PX:
                    self.canvas.move(item, new_xpos-self.mouse_xpos,
                                     new_ypos-self.mouse_ypos)
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.selected_block)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def on_release(self, event):
        if self.selected_block == "-1":
            return
        if self.mouse_xpos > self.BOARD_SIZE_PX + self.DIVIDER_WIDTH_PX:  # replace event.x with mouse_xpos
            for item in self.canvas.find_withtag(self.selected_block):
                # replace event.x with mouse_xpos
                self.canvas.scale(item, self.mouse_xpos,
                                  self.mouse_ypos, 0.5, 0.5)
        self.move_flag = False
        # replace event.x with mouse_xpos
        col = int(self.mouse_xpos/self.CELL_SIZE_PX)
        row = int(self.mouse_ypos/self.CELL_SIZE_PX)

        proposed_coordinates = []
        offset = self.picker_blocks[self.PLAYERS[self.current_player]][int(self.selected_block.split(
            "_")[2])].coordinates[int(self.selected_block_segment.split("_")[2])]
        for coord in self.picker_blocks[self.PLAYERS[self.current_player]][int(self.selected_block.split("_")[2])].coordinates:
            proposed_coordinates.append(
                [row + coord[0] - offset[0], col + coord[1] - offset[1]])
        if validator.placement_is_valid(self.tiles, proposed_coordinates, self.current_player):
            for coord in proposed_coordinates:
                self.tiles[coord[0]][coord[1]] = self.current_player
            for item in self.canvas.find_withtag(self.selected_block):
                self.canvas.delete(item)
            self.paint_board()
            current_tiles_for_player = 0
            for row in self.tiles:
                current_tiles_for_player += row.count(self.current_player)
            self.score[self.current_player] = - \
                89 + current_tiles_for_player
            self.update_score()
            self.switch_player()

    def on_resign(self):
        self.white_flag[self.current_player] = True
        self.switch_player()

    def on_rotate(self, event):
        tags = self.canvas.gettags("current")
        if self.current_player == None:
            return
        if not tags or not tags[0].split("_")[0] == self.PLAYERS[self.current_player]:
            return
        self.mouse_xpos = event.x
        self.mouse_ypos = event.y
        self.selected_block = tags[0]
        self.selected_block_segment = tags[1]

        segments = self.canvas.find_withtag(self.selected_block)
        seg = None
        for segment in segments:
            if self.selected_block_segment in self.canvas.gettags(segment):
                seg = segment
        coords = self.canvas.coords(seg)
        selected_block_coords = [coords[0], coords[1]]
        block_object = self.picker_blocks[self.PLAYERS[self.current_player]][int(self.selected_block.split(
            "_")[2])]
        rotated_block = transformer.rotate_90(
            block_object, self.selected_block_segment)
        self.picker_blocks[self.PLAYERS[self.current_player]][int(self.selected_block.split(
            "_")[2])] = rotated_block

        self.canvas.delete(self.selected_block)
        block_segment = 0
        for coord in rotated_block.coordinates:
            self.canvas.create_rectangle(
                selected_block_coords[0] + coord[1]*self.PICKER_CELL_SIZE_PX,
                selected_block_coords[1] + coord[0]*self.PICKER_CELL_SIZE_PX,
                selected_block_coords[0] +
                (coord[1] + 1)*self.PICKER_CELL_SIZE_PX,
                selected_block_coords[1] +
                (coord[0] + 1)*self.PICKER_CELL_SIZE_PX,
                fill=self.PLAYERS[self.current_player], tags=(self.PLAYERS[self.current_player] + "_block_" + str(rotated_block.index), "block_segment_" + str(block_segment), "picker"))
            block_segment += 1

    def on_flip(self, event):
        tags = self.canvas.gettags("current")
        if self.current_player == None:
            return
        if not tags or not tags[0].split("_")[0] == self.PLAYERS[self.current_player]:
            return
        self.mouse_xpos = event.x
        self.mouse_ypos = event.y
        self.selected_block = tags[0]
        self.selected_block_segment = tags[1]

        segments = self.canvas.find_withtag(self.selected_block)
        seg = None
        for segment in segments:
            if self.selected_block_segment in self.canvas.gettags(segment):
                seg = segment
        coords = self.canvas.coords(seg)
        selected_block_coords = [coords[0], coords[1]]
        block_object = self.picker_blocks[self.PLAYERS[self.current_player]][int(self.selected_block.split(
            "_")[2])]
        flipped_block = transformer.flip(
            block_object, self.selected_block_segment)
        self.picker_blocks[self.PLAYERS[self.current_player]][int(self.selected_block.split(
            "_")[2])] = flipped_block

        self.canvas.delete(self.selected_block)
        block_segment = 0
        for coord in flipped_block.coordinates:
            self.canvas.create_rectangle(
                selected_block_coords[0] + coord[1]*self.PICKER_CELL_SIZE_PX,
                selected_block_coords[1] + coord[0]*self.PICKER_CELL_SIZE_PX,
                selected_block_coords[0] +
                (coord[1] + 1)*self.PICKER_CELL_SIZE_PX,
                selected_block_coords[1] +
                (coord[0] + 1)*self.PICKER_CELL_SIZE_PX,
                fill=self.PLAYERS[self.current_player], tags=(self.PLAYERS[self.current_player] + "_block_" + str(flipped_block.index), "block_segment_" + str(block_segment), "picker"))
            block_segment += 1

    def update_score(self):
        self.canvas.itemconfig(self.red_score_label,
                               text="Red Score: " + str(self.score[0]))
        self.canvas.itemconfig(self.green_score_label,
                               text="Green Score: " + str(self.score[1]))


root = tk.Tk()
root.title("Blokus Duo")
root.resizable(False, False)
app = BlokusApp(master=root)
app.mainloop()
