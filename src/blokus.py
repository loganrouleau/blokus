import tkinter as tk

from . import constants, transformer, validator
from .model import Model
from .view import View


class BlokusApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.model = Model()
        self.view = View(self.model)
        self.bind_callbacks()

    def bind_callbacks(self):
        self.model.resign_button.configure(command=self.on_resign)
        self.model.canvas.bind("<Configure>", self.view.configure_canvas)
        self.model.canvas.bind("<Button-1>", self.on_block_selection)  # left click
        self.model.canvas.bind("<Button-2>", self.on_flip)  # middle click
        self.model.canvas.bind("<Button-3>", self.on_rotate)  # right click
        self.model.canvas.tag_bind("picker", '<Button1-Motion>', self.on_move)
        self.model.canvas.tag_bind("picker", '<ButtonRelease-1>', self.on_release)

    def switch_player(self):
        self.model.selected_block = "-1"
        if self.model.white_flag[0] and self.model.white_flag[1]:
            self.model.resign_button['state'] = 'disabled'
            win_team = constants.Player.red if self.model.score[0] > self.model.score[1] else constants.Player.green
            self.model.canvas.itemconfig(self.model.end_game_label,
                                         text="GG! Player " + win_team.name + " has won!")
            if self.model.score[0] == self.model.score[1]:
                self.model.canvas.itemconfig(self.model.end_game_label, text="constants.GG! It's a tie!")
            return
        if not self.model.white_flag[0] and not self.model.white_flag[1]:
            self.model.current_player = constants.Player.red if self.model.current_player == constants.Player.green else constants.Player.green
            return
        if not self.model.white_flag[0] and self.model.white_flag[1]:
            self.model.current_player = constants.Player.red
            return
        if not self.model.white_flag[1] and self.model.white_flag[0]:
            self.model.current_player = constants.Player.green
            return

    def on_block_selection(self, event):
        tags = self.model.canvas.gettags("current")
        if not tags or not tags[0].split("_")[0] == self.model.current_player.name:
            return
        self.model.mouse_xpos = event.x
        self.model.mouse_ypos = event.y
        self.model.selected_block = tags[0]
        self.model.selected_block_segment = tags[1]
        if event.x > constants.BOARD_SIZE_PX + constants.DIVIDER_WIDTH_PX:
            for item in self.model.canvas.find_withtag(self.model.selected_block):
                self.model.canvas.scale(item, event.x, event.y, 2, 2)

    def on_move(self, event):
        if self.model.move_flag:
            new_xpos, new_ypos = event.x, event.y
            for item in self.model.canvas.find_withtag(self.model.selected_block):
                if new_xpos <= 0 or new_xpos >= constants.CANVAS_WIDTH_PX - constants.PICKER_CELL_SIZE_PX or new_ypos <= 0 or new_ypos >= constants.CANVAS_HEIGHT_PX:
                    if new_xpos <= 0:
                        self.model.mouse_xpos = constants.DIVIDER_WIDTH_PX/2
                    if new_ypos <= 0:
                        self.model.mouse_ypos = constants.DIVIDER_WIDTH_PX/2
                    if new_xpos >= constants.CANVAS_WIDTH_PX:
                        self.model.mouse_xpos = constants.CANVAS_WIDTH_PX - constants.PICKER_CELL_SIZE_PX * 4
                    if new_ypos >= constants.CANVAS_HEIGHT_PX:
                        self.model.mouse_ypos = constants.CANVAS_HEIGHT_PX - constants.DIVIDER_WIDTH_PX
                    return

                if new_xpos > 0 and new_ypos > 0 and new_xpos < constants.CANVAS_WIDTH_PX - constants.PICKER_CELL_SIZE_PX and new_ypos < constants.CANVAS_HEIGHT_PX:
                    self.model.canvas.move(item, new_xpos-self.model.mouse_xpos, new_ypos-self.model.mouse_ypos)
            self.model.mouse_xpos = new_xpos
            self.model.mouse_ypos = new_ypos
        else:
            self.model.move_flag = True
            self.model.canvas.tag_raise(self.model.selected_block)
            self.model.mouse_xpos = event.x
            self.model.mouse_ypos = event.y

    def on_release(self, event):
        if self.model.selected_block == "-1":
            return
        if self.model.mouse_xpos > constants.BOARD_SIZE_PX + constants.DIVIDER_WIDTH_PX:
            for item in self.model.canvas.find_withtag(self.model.selected_block):
                self.model.canvas.scale(item, self.model.mouse_xpos, self.model.mouse_ypos, 0.5, 0.5)
        self.model.move_flag = False
        col = int(self.model.mouse_xpos/constants.CELL_SIZE_PX)
        row = int(self.model.mouse_ypos/constants.CELL_SIZE_PX)

        proposed_coordinates = []
        offset = self.model.picker_blocks[self.model.current_player
                                          ][self.model.get_selected_block()].coordinates[self.model.get_selected_block_segment()]
        for coord in self.model.picker_blocks[self.model.current_player][self.model.get_selected_block()].coordinates:
            proposed_coordinates.append([row + coord[0] - offset[0], col + coord[1] - offset[1]])
        if validator.placement_is_valid(self.model.tiles, proposed_coordinates, self.model.current_player.value):
            for coord in proposed_coordinates:
                self.model.tiles[coord[0]][coord[1]] = self.model.current_player.value
            for item in self.model.canvas.find_withtag(self.model.selected_block):
                self.model.canvas.delete(item)
            self.view.paint_board()
            current_tiles_for_player = 0
            for row in self.model.tiles:
                current_tiles_for_player += row.count(
                    self.model.current_player.value)
            self.model.score[self.model.current_player.value] = -89 + current_tiles_for_player
            self.view.update_score()
            self.switch_player()

    def on_resign(self):
        self.model.white_flag[self.model.current_player.value] = True
        self.switch_player()

    def on_rotate(self, event):
        self.update_selection(event)
        block_object = self.model.picker_blocks[self.model.current_player][self.model.get_selected_block()]
        rotated_block = transformer.rotate_90(block_object, self.model.get_selected_block_segment())
        self.model.picker_blocks[self.model.current_player][self.model.get_selected_block()] = rotated_block
        self.view.paint_transformed_block(rotated_block)

    def on_flip(self, event):
        self.update_selection(event)
        block_object = self.model.picker_blocks[self.model.current_player][self.model.get_selected_block()]
        flipped_block = transformer.flip(block_object, self.model.get_selected_block_segment())
        self.model.picker_blocks[self.model.current_player][self.model.get_selected_block()] = flipped_block
        self.view.paint_transformed_block(flipped_block)

    def update_selection(self, event):
        tags = self.model.canvas.gettags("current")
        if not tags or not tags[0].split("_")[0] == self.model.current_player.name:
            return
        self.model.mouse_xpos = event.x
        self.model.mouse_ypos = event.y
        self.model.selected_block = tags[0]
        self.model.selected_block_segment = tags[1]


root = tk.Tk()
root.title("Blokus Duo")
root.resizable(False, False)
app = BlokusApp(master=root)
app.mainloop()
