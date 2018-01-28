import random
from tkinter import *

import os

from app import App
from empire import Empire
from map import Map
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("num_empires", help="number of empires to have in the simulation",
                        type=int)
    parser.add_argument("size", help="height of the square map", type=int)

    args = parser.parse_args()

    root = Tk()

    grid = Map(args.size)

    app = App(root, grid)

    Empire.APP = app

    names = None
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "empire_names.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path) as f_name:
        names = f_name.read().split("\n")

    num_empires = args.num_empires
    for _ in range(num_empires):
        app.add_empire(Empire(random.choice(names), grid.rand_select()))

    while True:
        app.turn()
        root.update()
    root.destroy()
