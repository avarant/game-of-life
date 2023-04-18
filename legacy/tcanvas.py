import curses

class TCanvas:

    def __init__(self, width, height):
        self.stdscr = curses.initscr()

        width = width * 2
        max_y, max_x = self.stdscr.getmaxyx()
        start_y, start_x = (max_y - height) // 2, (max_x - width) // 2
        # start_x, start_y = 0, 0

        win = curses.newwin(height+2, width+2, start_y-1, start_x-1)
        win.border()

        self.win = curses.newwin(height, width, start_y, start_x)

        max_y, max_x = self.win.getmaxyx()
        self.max_y = max_y
        self.max_x = max_x

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)

        self.win.nodelay(1)
        self.win.clear()
        win.refresh()


    def fill(self, x, y, c=1):
        if c == 0:
            c = 2
        elif c != 1:
            c = 1

        if x < 0 or y < 0:
            return
        if x * 2 >= self.max_x or y >= self.max_y:
            return

        x = x*2

        self.win.attron(curses.color_pair(c))
        self.win.addch(y, x, ' ')
        self.win.addch(y, x+1, ' ')
        self.win.attroff(curses.color_pair(c))

    def refresh(self):
        self.win.move(self.max_y-1, 0)
        self.win.refresh()
        return self.win.getch()

    def clear(self):
        self.win.clear()

    def exit(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.endwin()
