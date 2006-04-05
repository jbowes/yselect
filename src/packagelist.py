import curses


class PackageView:

    def __init__(self, window):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(1))
        
        (height, width) = self.window.getmaxyx()

        self.list_window = ListView(window.derwin(1, 0))
        self.details_window = DetailsView(window.derwin(height / 2, 0))


    def update(self):
        self.list_window.update()
        self.details_window.update()

        (height, width) = self.window.getmaxyx()

        self.window.addstr(0, 0, "yselect - inspection of package states (avail., priority)")
        self.window.refresh()

    def run(self):

        while True:
            self.update()
            char = self.window.getch()

            if char == ord('q'):
                break


class ListView:

    def __init__(self, window):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(2))
        padwin = self.window.derwin(1,0)
        self.pad = padwin
        self.pad.bkgd(" ", curses.color_pair(0))

    def update(self):
        (height, width) = self.window.getmaxyx()
        self.window.addstr(0,0, "EIOM Pri Section\tPackage\tInst.ver\tAvail.ver\tDescription")
        self.add_menu_title(0, 5, "another sublist", 1)
        self.add_menu_title(1, 5, "another sublist", 2)
        self.add_menu_title(2, 5, "another sublist", 3)
        self.window.refresh()

    def add_menu_title(self, y, x, title, depth):
        """
        Draw a menu title on the screen.

        Starting at position x,y draw a menu title. depth indicates how many
        parents the menu has. Title is rendered in bold.
        """
        line_length = depth * 2 - 1
        
        self.pad.hline(y, x, curses.ACS_HLINE, line_length)
        self.pad.addstr(y, x + line_length + 1 , title, curses.A_BOLD)
        self.pad.hline(y, x + line_length + 2 + len(title), curses.ACS_HLINE,
            line_length)


class DetailsView:

    def __init__(self, window):
        self.window = window
        self.window.bkgd(" ", curses.color_pair(2))
        (height, width) = self.window.getmaxyx()
        self.details_pad = self.window.derwin(height - 2, 0, 1, 0) 
        self.details_pad.bkgd(" ", curses.color_pair(0))

    def update(self):
        (height, width) = self.window.getmaxyx()
        self.window.addstr(0,0, "bar!   Required")
        self.window.addstr(height - 1, 0, "press d for more.")
        self.details_pad.addstr(0,0, "DETAILS")


def main(window):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    packageView = PackageView(window)
    packageView.run()

curses.wrapper(main)
