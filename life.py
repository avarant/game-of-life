import sys
import os
import argparse
from itertools import product
from time import sleep
import tkinter as tk


BLOCK_SIZE = 10  # cell dimensions
SIZE = 80   # board dimensions in terms of blocks
WINDOW_WIDTH, WINDOW_HEIGHT = SIZE * BLOCK_SIZE, SIZE * BLOCK_SIZE
START_X, START_Y = SIZE // 2 - SIZE // 4, SIZE // 2 - SIZE // 4

DELAY = 0.1  # time interval between steps

FILL_COLOR = "yellow"  # cell fill color

DELIMITERS = [' ', '.']  # empty space character


class App(tk.Frame):
    def __init__(self, master=None, seed=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.seed = seed
        self.og_seed = seed
        self.draw()

    def create_widgets(self):
        self.canvas = tk.Canvas(
            self.master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, background='black')
        self.canvas.pack()

        hl_color = '#3E4149'

        self.buttonframe = tk.Frame(self)
        self.buttonframe.grid(row=1, column=0, columnspan=4)

        self.next_btn = tk.Button(
            self.buttonframe, text="next", command=self.step, highlightbackground=hl_color)
        self.next_btn.grid(row=0, column=1)

        self.start_btn = tk.Button(
            self.buttonframe, text="start", command=self.start, highlightbackground=hl_color)
        self.start_btn.grid(row=0, column=2)

        self.reset_btn = tk.Button(
            self.buttonframe, text="reset", command=self.reset, highlightbackground=hl_color)
        self.reset_btn.grid(row=0, column=3)

        self.quit_btn = tk.Button(self.buttonframe, text="quit",
                                  command=self.master.destroy, highlightbackground=hl_color)
        self.quit_btn.grid(row=0, column=4)

    def draw_cell(self, cell):
        x, y = cell
        self.canvas.create_rectangle(x*BLOCK_SIZE, y*BLOCK_SIZE,
                                     x*BLOCK_SIZE+BLOCK_SIZE, y*BLOCK_SIZE+BLOCK_SIZE, fill=FILL_COLOR)

    def draw(self):
        self.canvas.delete("all")
        for cell in self.seed:
            self.draw_cell(cell)

    # https://stackoverflow.com/questions/1620940/determining-neighbours-of-cell-two-dimensional-list
    def neighbors(self, cell):
        for c in product(*(range(n-1, n+2) for n in cell)):
            if c != cell and all(0 <= n < SIZE for n in c):
                yield c

    def step(self):
        res = []

        for i in range(SIZE):
            for j in range(SIZE):
                cell = (i, j)
                n = sum(1 for x in self.neighbors(cell) if x in self.seed)

                if cell in self.seed:
                    if n == 2 or n == 3:
                        res.append(cell)
                else:
                    if n == 3:
                        res.append(cell)

        self.seed = res
        self.draw()

    def start(self):
        self.start_btn.config(text="stop")
        self.start_btn.config(command=self.stop)

        self.canvas.pack()
        self.isRunning = True

        while self.isRunning and len(self.seed) > 0:
            sleep(DELAY)
            self.step()
            self.canvas.update()

    def stop(self):
        self.isRunning = False
        self.start_btn.config(text="start")
        self.start_btn.config(command=self.start)

    def reset(self):
        self.stop()
        self.seed = self.og_seed
        self.draw()


def main():
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life")
    parser.add_argument(
        "-s", "--seed", help="path to iniitial pattern (spaces are treated as empty space. all other characters are considered cells)")
    args = parser.parse_args()

    path = args.seed
    x, y = START_X, START_Y  # start coords

    if path:
        if not os.path.isfile(path):
            print("Error: %s not found" % path)
            sys.exit()

        with open(path) as f:
            reader = f.readlines()
            seed = []
            for i, row in enumerate(reader):
                row = row.strip('\n')
                # print(row)
                for j, c in enumerate(row):
                    if c not in DELIMITERS:
                        seed.append((x+j, y+i))
            # print(seed)

    else:
        # glider pattern
        seed = [(x, y), (x+1, y+1), (x+1, y+2), (x, y+2), (x-1, y+2)]

    root = tk.Tk()
    app = App(master=root, seed=seed)
    app.mainloop()


if __name__ == "__main__":
    main()
