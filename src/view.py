from . import constants


class View:
    def __init__(self, model):
        self.model = model

    def configure_canvas(self, event=None):
        self.draw_board_grid()
        self.draw_picker_blocks()

    def draw_board_grid(self):
        for i in range(0, constants.BOARD_SIZE_PX + 1, constants.CELL_SIZE_PX):
            self.model.canvas.create_line([(i, 0), (i, constants.BOARD_SIZE_PX)])
        for i in range(0, constants.BOARD_SIZE_PX, constants.CELL_SIZE_PX):
            self.model.canvas.create_line([(0, i), (constants.BOARD_SIZE_PX, i)])

    def draw_picker_blocks(self):
        height_offset = constants.PICKER_HEIGHT_OFFSET_PX
        for player in constants.Player:
            for current_block in self.model.picker_blocks[player]:
                block_segment = 0
                for coord in current_block.coordinates:
                    self.model.canvas.create_rectangle(
                        constants.PICKER_WIDTH_OFFSET_PX + (
                            current_block.position[1] + coord[1])*constants.PICKER_CELL_SIZE_PX,
                        height_offset + (
                            current_block.position[0] + coord[0])*constants.PICKER_CELL_SIZE_PX,
                        constants.PICKER_WIDTH_OFFSET_PX + (
                            current_block.position[1] + coord[1] + 1)*constants.PICKER_CELL_SIZE_PX,
                        height_offset + (
                            current_block.position[0] + coord[0] + 1)*constants.PICKER_CELL_SIZE_PX,
                        fill=player.name,
                        tags=(player.name + "_block_" + str(current_block.index),
                              "block_segment_" + str(block_segment), "picker"))
                    block_segment += 1
            height_offset += constants.PICKER_HEIGHT_PX

    def paint_board(self):
        for row in range(constants.BOARD_SIZE_CELLS):
            for col in range(constants.BOARD_SIZE_CELLS):
                if self.model.tiles[row][col] == 0 or self.model.tiles[row][col] == 1:
                    self.model.canvas.create_rectangle(
                        (col)*constants.CELL_SIZE_PX,
                        (row)*constants.CELL_SIZE_PX,
                        (col + 1)*constants.CELL_SIZE_PX,
                        (row + 1)*constants.CELL_SIZE_PX,
                        fill=constants.Player(int(self.model.tiles[row][col])).name)

    def update_score(self):
        self.model.canvas.itemconfig(self.model.red_score_label, text="Red Score: " + str(self.model.score[0]))
        self.model.canvas.itemconfig(self.model.green_score_label, text="Green Score: " + str(self.model.score[1]))
