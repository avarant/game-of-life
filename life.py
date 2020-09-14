import sys
import os
import argparse
from itertools import product
from time import sleep
import tkinter as tk
import tkinter.ttk as ttk
import copy

BLOCK_SIZE = 8  # cell dimensions
SIZE = 96   # board dimensions in terms of blocks
CANVAS_WIDTH, CANVAS_HEIGHT = SIZE * BLOCK_SIZE, SIZE * BLOCK_SIZE
# START_X, START_Y = SIZE // 2 - SIZE // 4, SIZE // 2 - SIZE // 4
START_X, START_Y = 10, 10

DELAY = 0.1  # time interval between steps

FILL_COLOR = "yellow"  # cell fill color
CANVAS_COLOR = "grey"

DELIMITERS = [' ', '.']  # empty space character


class Life(tk.Frame):
    def __init__(self, master=None, seed=None):
        super().__init__(master)
        self.master = master
        self.seed = copy.deepcopy(seed)

        self.master.maxsize(CANVAS_HEIGHT, CANVAS_WIDTH)
        self.master.minsize(CANVAS_HEIGHT, CANVAS_WIDTH)
        self.pack()

        self.create_widgets()
        self.reset()

    def create_widgets(self):
        self.canvas = tk.Canvas(
            self.master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background=CANVAS_COLOR)

        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.canvas.pack()

        self.buttonframe = ttk.Frame(self)
        self.buttonframe.grid(row=1, column=0, columnspan=4)

        self.next_btn = ttk.Button(
            self.buttonframe, text="next", command=self.step)
        self.next_btn.grid(row=0, column=1)

        self.start_btn = ttk.Button(
            self.buttonframe, text="start", command=self.start)
        self.start_btn.grid(row=0, column=2)

        self.reset_btn = ttk.Button(
            self.buttonframe, text="reset", command=self.reset)
        self.reset_btn.grid(row=0, column=3)

        self.quit_btn = ttk.Button(self.buttonframe, text="quit",
                                   command=self.master.destroy)
        self.quit_btn.grid(row=0, column=4)

        self.canvas.focus_set()

    def add_cell(self, cell):
        x, y = cell
        self.cells[cell] = self.canvas.create_rectangle(x*BLOCK_SIZE, y*BLOCK_SIZE,
                                            x*BLOCK_SIZE+BLOCK_SIZE, y*BLOCK_SIZE+BLOCK_SIZE, fill=FILL_COLOR)

    def delete_cell(self, cell):
        self.canvas.delete(self.cells[cell])
        self.cells.pop(cell)

    def toggle_cell(self, e):
        cell = (e.x // BLOCK_SIZE, e.y // BLOCK_SIZE)
        if cell not in self.cells.keys():
            self.add_cell(cell)
        else:
            self.delete_cell(cell)

    # https://stackoverflow.com/questions/1620940/determining-neighbours-of-cell-two-dimensional-list
    def neighbors(self, cell):
        for c in product(*(range(n-1, n+2) for n in cell)):
            if c != cell and all(0 <= n < SIZE for n in c):
                yield c

    def step(self):
        live = list(self.cells.keys())

        all_cells = set([])
        for cell in live:
            all_cells.add(cell)
            for neighbor in self.neighbors(cell):
                all_cells.add(neighbor)

        for cell in all_cells:
            n = sum(1 for x in self.neighbors(cell) if x in live)
            if cell in live:
                if not (n == 2 or n == 3):
                    self.delete_cell(cell)
            elif n == 3:
                self.add_cell(cell)

        self.canvas.update()

    def start(self):
        self.start_btn.config(text="stop")
        self.start_btn.config(command=self.stop)

        self.canvas.pack()
        self.isRunning = True

        prev = None
        while self.isRunning and len(self.seed) > 0 and prev != list(self.cells.keys()):
            sleep(DELAY)
            prev = list(self.cells.keys())
            self.step()

        self.stop()

    def stop(self):
        self.isRunning = False
        self.start_btn.config(text="start")
        self.start_btn.config(command=self.start)

    def reset(self):
        self.stop()
        self.canvas.delete("all")
        self.cells = {}
        for cell in self.seed:
          self.add_cell(cell)


def read_txt(path, start=(START_X, START_Y)):
    if not os.path.isfile(path):
        print("Error: %s not found" % path)
        sys.exit()

    x, y = start
    seed = []
    with open(path) as f:
        reader = f.readlines()

        for i, row in enumerate(reader):
            row = row.strip('\n')
            # print(row)
            for j, c in enumerate(row):
                if c not in DELIMITERS:
                    seed.append((x+j, y+i))
        # print(seed)

    return seed


def main():
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life")
    parser.add_argument(
        "-s", "--seed", help="path to iniitial pattern (spaces are treated as empty space. all other characters are considered cells)")
    args = parser.parse_args()

    path = args.seed
    x, y = START_X, START_Y  # start coords

    if path:
        seed = read_txt(path)

    else:  # default pattern (glider)
        seed = [(x, y), (x+1, y+1), (x+1, y+2), (x, y+2), (x-1, y+2)]

    root = tk.Tk()
    app = Life(master=root, seed=seed)
    app.mainloop()


if __name__ == "__main__":
    main()
