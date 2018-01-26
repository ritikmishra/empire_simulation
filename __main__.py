from tkinter import *
from app import App
from empire import Empire
from map import Map

if __name__ == '__main__':
    root = Tk()

    grid = Map(48)

    app = App(root, grid)

    Empire.APP = app

    romans = Empire("Roman", grid.rand_select())

    ottomans = Empire("Ottoman", grid.rand_select())

    egyptians = Empire("Egyptian", grid.rand_select())

    greek = Empire("Greek", grid.rand_select())

    app.add_empire(romans)
    app.add_empire(ottomans)
    app.add_empire(egyptians)
    app.add_empire(greek)

    for x in range(300):
        for y in range(300):
            # app[x, y] = "#00ff00"
            pass

    root.update()
    root.mainloop()
    root.destroy()
