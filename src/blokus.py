import tkinter as tk
from . import block
from . import block_generator
from . import validator
from . import transformer
from . import game_state

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


class BlokusApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.state = game_state.GameState()
        self.state.resign_button.configure(command=self.on_resign)
        self.state.canvas.bind("<Configure>", self.configure_canvas)
        self.state.canvas.bind(
            "<Button-1>", self.on_block_selection)  # left click
        self.state.canvas.bind(
            "<Button-2>", self.on_flip)  # middle click
        self.state.canvas.bind(
            "<Button-3>", self.on_rotate)  # right click
        self.state.canvas.tag_bind(
            "picker", '<Button1-Motion>', self.on_move)
        self.state.canvas.tag_bind(
            "picker", '<ButtonRelease-1>', self.on_release)

    def switch_player(self):
        self.state.selected_block = "-1"
        if self.state.white_flag[0] and self.state.white_flag[1]:
            self.state.current_player = None  # end of the game
            self.state.resign_button['state'] = 'disabled'
            # resign_button['text']='Restart'
            win_team = PLAYERS[0] if self.state.score[0] > self.state.score[1] else PLAYERS[1]
            self.state.canvas.itemconfig(
                self.state.end_game_label, text="GG! Player " + win_team + " has won!")
            if self.state.score[0] == self.state.score[1]:
                self.state.canvas.itemconfig(
                    self.state.end_game_label, text="GG! It's a tie!")
            return
        if not self.state.white_flag[0] and not self.state.white_flag[1]:
            self.state.current_player = 1 if self.state.current_player == 0 else 0
            return
        if not self.state.white_flag[0] and self.state.white_flag[1]:
            self.state.current_player = 0
            return
        if not self.state.white_flag[1] and self.state.white_flag[0]:
            self.state.current_player = 1
            return

    def paint_board(self):
        for row in range(BOARD_SIZE_CELLS):
            for col in range(BOARD_SIZE_CELLS):
                if self.state.tiles[row][col] == 0 or self.state.tiles[row][col] == 1:
                    self.state.canvas.create_rectangle(
                        (col)*CELL_SIZE_PX,
                        (row)*CELL_SIZE_PX,
                        (col + 1)*CELL_SIZE_PX,
                        (row + 1)*CELL_SIZE_PX,
                        fill=PLAYERS[int(self.state.tiles[row][col])])

    def configure_canvas(self, event=None):
        self.draw_board_grid()
        self.draw_picker_blocks()

    def draw_board_grid(self):
        for i in range(0, BOARD_SIZE_PX + 1, CELL_SIZE_PX):
            self.state.canvas.create_line(
                [(i, 0), (i, BOARD_SIZE_PX)])
        for i in range(0, BOARD_SIZE_PX, CELL_SIZE_PX):
            self.state.canvas.create_line(
                [(0, i), (BOARD_SIZE_PX, i)])

    def draw_picker_blocks(self):
        height_offset = PICKER_HEIGHT_OFFSET_PX
        for player in PLAYERS:
            for current_block in self.state.picker_blocks[PLAYERS[player]]:
                block_segment = 0
                for coord in current_block.coordinates:
                    self.state.canvas.create_rectangle(
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

    def on_block_selection(self, event):
        tags = self.state.canvas.gettags("current")
        if self.state.current_player == None:
            return
        if not tags or not tags[0].split("_")[0] == PLAYERS[self.state.current_player]:
            return
        self.state.mouse_xpos = event.x
        self.state.mouse_ypos = event.y
        self.state.selected_block = tags[0]
        self.state.selected_block_segment = tags[1]
        if event.x > BOARD_SIZE_PX + DIVIDER_WIDTH_PX:
            for item in self.state.canvas.find_withtag(self.state.selected_block):
                self.state.canvas.scale(item, event.x, event.y, 2, 2)

    def on_move(self, event):
        if self.state.move_flag:
            new_xpos, new_ypos = event.x, event.y
            for item in self.state.canvas.find_withtag(self.state.selected_block):
                if new_xpos <= 0 or new_xpos >= CANVAS_WIDTH_PX - PICKER_CELL_SIZE_PX or new_ypos <= 0 or new_ypos >= CANVAS_HEIGHT_PX:
                    if new_xpos <= 0:
                        self.state.mouse_xpos = DIVIDER_WIDTH_PX/2
                    if new_ypos <= 0:
                        self.state.mouse_ypos = DIVIDER_WIDTH_PX/2
                    if new_xpos >= CANVAS_WIDTH_PX:
                        self.state.mouse_xpos = CANVAS_WIDTH_PX - \
                            PICKER_CELL_SIZE_PX * 4
                    if new_ypos >= CANVAS_HEIGHT_PX:
                        self.state.mouse_ypos = CANVAS_HEIGHT_PX - DIVIDER_WIDTH_PX
                    return

                if new_xpos > 0 and new_ypos > 0 and new_xpos < CANVAS_WIDTH_PX - PICKER_CELL_SIZE_PX and new_ypos < CANVAS_HEIGHT_PX:
                    self.state.canvas.move(item, new_xpos-self.state.mouse_xpos,
                                           new_ypos-self.state.mouse_ypos)
            self.state.mouse_xpos = new_xpos
            self.state.mouse_ypos = new_ypos
        else:
            self.state.move_flag = True
            self.state.canvas.tag_raise(self.state.selected_block)
            self.state.mouse_xpos = event.x
            self.state.mouse_ypos = event.y

    def on_release(self, event):
        if self.state.selected_block == "-1":
            return
        if self.state.mouse_xpos > BOARD_SIZE_PX + DIVIDER_WIDTH_PX:  # replace event.x with mouse_xpos
            for item in self.state.canvas.find_withtag(self.state.selected_block):
                # replace event.x with mouse_xpos
                self.state.canvas.scale(item, self.state.mouse_xpos,
                                        self.state.mouse_ypos, 0.5, 0.5)
        self.state.move_flag = False
        # replace event.x with mouse_xpos
        col = int(self.state.mouse_xpos/CELL_SIZE_PX)
        row = int(self.state.mouse_ypos/CELL_SIZE_PX)

        proposed_coordinates = []
        offset = self.state.picker_blocks[PLAYERS[self.state.current_player]][int(self.state.selected_block.split(
            "_")[2])].coordinates[int(self.state.selected_block_segment.split("_")[2])]
        for coord in self.state.picker_blocks[PLAYERS[self.state.current_player]][int(self.state.selected_block.split("_")[2])].coordinates:
            proposed_coordinates.append(
                [row + coord[0] - offset[0], col + coord[1] - offset[1]])
        if validator.placement_is_valid(self.state.tiles, proposed_coordinates, self.state.current_player):
            for coord in proposed_coordinates:
                self.state.tiles[coord[0]][coord[1]
                                           ] = self.state.current_player
            for item in self.state.canvas.find_withtag(self.state.selected_block):
                self.state.canvas.delete(item)
            self.paint_board()
            current_tiles_for_player = 0
            for row in self.state.tiles:
                current_tiles_for_player += row.count(
                    self.state.current_player)
            self.state.score[self.state.current_player] = - \
                89 + current_tiles_for_player
            self.update_score()
            self.switch_player()

    def on_resign(self):
        self.state.white_flag[self.state.current_player] = True
        self.switch_player()

    def on_rotate(self, event):
        tags = self.state.canvas.gettags("current")
        if self.state.current_player == None:
            return
        if not tags or not tags[0].split("_")[0] == PLAYERS[self.state.current_player]:
            return
        self.state.mouse_xpos = event.x
        self.state.mouse_ypos = event.y
        self.state.selected_block = tags[0]
        self.state.selected_block_segment = tags[1]

        segments = self.state.canvas.find_withtag(self.state.selected_block)
        seg = None
        for segment in segments:
            if self.state.selected_block_segment in self.state.canvas.gettags(segment):
                seg = segment
        coords = self.state.canvas.coords(seg)
        selected_block_coords = [coords[0], coords[1]]
        block_object = self.state.picker_blocks[PLAYERS[self.state.current_player]][int(self.state.selected_block.split(
            "_")[2])]
        rotated_block = transformer.rotate_90(
            block_object, self.state.selected_block_segment)
        self.state.picker_blocks[PLAYERS[self.state.current_player]][int(self.state.selected_block.split(
            "_")[2])] = rotated_block

        self.state.canvas.delete(self.state.selected_block)
        block_segment = 0
        for coord in rotated_block.coordinates:
            self.state.canvas.create_rectangle(
                selected_block_coords[0] + coord[1] *
                PICKER_CELL_SIZE_PX,
                selected_block_coords[1] + coord[0] *
                PICKER_CELL_SIZE_PX,
                selected_block_coords[0] +
                (coord[1] + 1)*PICKER_CELL_SIZE_PX,
                selected_block_coords[1] +
                (coord[0] + 1)*PICKER_CELL_SIZE_PX,
                fill=PLAYERS[self.state.current_player], tags=(PLAYERS[self.state.current_player] + "_block_" + str(rotated_block.index), "block_segment_" + str(block_segment), "picker"))
            block_segment += 1

    def on_flip(self, event):
        tags = self.state.canvas.gettags("current")
        if self.state.current_player == None:
            return
        if not tags or not tags[0].split("_")[0] == PLAYERS[self.state.current_player]:
            return
        self.state.mouse_xpos = event.x
        self.state.mouse_ypos = event.y
        self.state.selected_block = tags[0]
        self.state.selected_block_segment = tags[1]

        segments = self.state.canvas.find_withtag(self.state.selected_block)
        seg = None
        for segment in segments:
            if self.state.selected_block_segment in self.state.canvas.gettags(segment):
                seg = segment
        coords = self.state.canvas.coords(seg)
        selected_block_coords = [coords[0], coords[1]]
        block_object = self.state.picker_blocks[PLAYERS[self.state.current_player]][int(self.state.selected_block.split(
            "_")[2])]
        flipped_block = transformer.flip(
            block_object, self.state.selected_block_segment)
        self.state.picker_blocks[PLAYERS[self.state.current_player]][int(self.state.selected_block.split(
            "_")[2])] = flipped_block

        self.state.canvas.delete(self.state.selected_block)
        block_segment = 0
        for coord in flipped_block.coordinates:
            self.state.canvas.create_rectangle(
                selected_block_coords[0] + coord[1] *
                PICKER_CELL_SIZE_PX,
                selected_block_coords[1] + coord[0] *
                PICKER_CELL_SIZE_PX,
                selected_block_coords[0] +
                (coord[1] + 1)*PICKER_CELL_SIZE_PX,
                selected_block_coords[1] +
                (coord[0] + 1)*PICKER_CELL_SIZE_PX,
                fill=PLAYERS[self.state.current_player], tags=(PLAYERS[self.state.current_player] + "_block_" + str(flipped_block.index), "block_segment_" + str(block_segment), "picker"))
            block_segment += 1

    def update_score(self):
        self.state.canvas.itemconfig(self.state.red_score_label,
                                     text="Red Score: " + str(self.state.score[0]))
        self.state.canvas.itemconfig(self.state.green_score_label,
                                     text="Green Score: " + str(self.state.score[1]))


root = tk.Tk()
root.title("Blokus Duo")
root.resizable(False, False)
app = BlokusApp(master=root)
app.mainloop()
