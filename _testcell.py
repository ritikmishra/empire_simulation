from app import App
from cell import Cell
from empire import Empire
from map import Map
from tkinter import *

if __name__ == '__main__':

    root = Tk()
    size = 30
    grid = Map(size)



    app = App(root, grid)
    Empire.APP = app

    a = Empire("Good Morning", grid[29,15])
    a.color = "#00ff00"
    app.add_empire(a)

    # radi = grid.getAdjacentLocs([(size/2, size/2), (16, 15), (17, 16)])
    # for loc in radi:
    #     app[loc] = "#00FF00"

    root.update()
    while True:
        for point in app.empires[0].getBeyondBorders():
            app[point.properties["Location"]] = "#0f0f0f"
        if a.military_strength > 5000: a.military_strength = 5000
        root.update()

    root.destroy()
