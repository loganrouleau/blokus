import tkinter as tk
import block


def main():
    print("Entering main")


if __name__ == "__main__":
    main()


ROWS = 14
COLS = 14
WIDTH = 500
HEIGHT = 500

token_colour = "red"
tiles = [[None for _ in range(COLS)] for _ in range(ROWS)]


def create_blocks():
    blocks = []
    for i in range(0, 5):
        blocks.append(block.Block(i))
        print(blocks[i].coordinates)


create_blocks()


def finish_turn():
    global token_colour
    if token_colour == "red":
        token_colour = "green"
    elif token_colour == "green":
        token_colour = "red"
    else:
        print("Error")


def on_canvas_click(event):
    col_width = c.winfo_width()/COLS
    row_height = c.winfo_height()/ROWS
    col = int(event.x//col_width)
    row = int(event.y//row_height)
    # If the tile is not filled, create a rectangle
    if not tiles[row][col]:
        tiles[row][col] = c.create_rectangle(
            col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill=token_colour)
        finish_turn()


def create_grid(event=None):
    w = c.winfo_width()
    h = c.winfo_height()
    for i in range(0,  w, int(w/COLS)):
        c.create_line([(i, 0), (i, h)], tag='grid_line')
    for i in range(0, h, int(h/ROWS)):
        c.create_line([(0, i), (w, i)], tag='grid_line')


def create_grid_d(event=None):
    print("binding d")
    w = d.winfo_width()
    h = d.winfo_height()
    for i in range(0,  w, int(w/COLS)):
        d.create_line([(i, 0), (i, h)], tag='grid_line')
    for i in range(0, h, int(h/ROWS)):
        d.create_line([(0, i), (w, i)], tag='grid_line')


root = tk.Tk()
root.title("Blokus Duo")
root.resizable(False, False)
c = tk.Canvas(root, width=WIDTH, height=HEIGHT, background='white')
d = tk.Canvas(root, width=WIDTH, height=HEIGHT, background='white')
c.pack(side="left")
d.pack(side="right")
c.bind("<Button-1>", on_canvas_click)
c.bind('<Configure>', create_grid)
d.bind("<Configure>", create_grid_d)
root.mainloop()
