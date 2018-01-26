import random
from tkinter import *
from app import App
from empire import Empire
from map import Map

if __name__ == '__main__':
    root = Tk()

    grid = Map(48)

    app = App(root, grid)

    Empire.APP = app

    names = None
    with open("empire_names.txt") as f_name:
        names = f_name.read().split("\n")

    num_empires = 8
    for _ in range(num_empires):
        app.add_empire(Empire(random.choice(names), grid.rand_select()))

    for x in range(300):
        for y in range(300):
            # app[x, y] = "#00ff00"
            pass

    root.update()
    root.mainloop()
    root.destroy()
