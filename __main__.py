from Tkinter import *
from app import App
from cell import Cell
from map import Map

if __name__ == '__main__':
    root = Tk()

    grid = Map(16)

    app = App(root, grid)

    for x in range(300):
        for y in range(300):
            # app[x, y] = "#00ff00"
            pass

    root.update()
    root.mainloop()
    root.destroy()
