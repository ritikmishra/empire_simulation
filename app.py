import math
from tkinter import *

from map import Map

WIDTH, HEIGHT = 1336, 200

MAP_SIZE = 600
SIDEBAR_WIDTH = 200

SIDEBAR_X = MAP_SIZE + 25
SIDEBAR_DY = 25

NUM_COLUMNS = WIDTH / 4
COLUMN_WIDTH = WIDTH / NUM_COLUMNS
COLUMN_DY = HEIGHT / NUM_COLUMNS


class App:
    def __init__(self, master, map):

        self.empires = {}

        self.frame = Frame(master, width=MAP_SIZE + SIDEBAR_WIDTH, height=MAP_SIZE)
        self.frame.grid(row=0, column=0, columnspan=2)

        self.sidebar = Frame(self.frame, width=SIDEBAR_WIDTH, height=MAP_SIZE)
        self.sidebar.grid(row=0, column=1, rowspan=4, columnspan=1)

        self.map = map
        self.colormap = Map(self.map.size)
        self.canvas = Canvas(self.frame, width=MAP_SIZE, height=MAP_SIZE, bg="#FFFFFF")
        self.canvas.grid(row=0, column=0)

        self.nextturn = Button(self.sidebar, text="Turn", command=self.turn)
        self.nextturn.grid(row=0, column=0)

        self.textboxes = {"Location": Label(self.sidebar, text="Location: N/A"),
                          "Population": Label(self.sidebar, text="Population: N/A"),
                          "Mountainous": Label(self.sidebar, text="Mountainous: N/A"),
                          "Land Area": Label(self.sidebar, text="Land Area: N/A"),
                          "Land Fertility": Label(self.sidebar, text="Land Fertility: N/A"),
                          "Livestock": Label(self.sidebar, text="Livestock: N/A"),
                          "Forest": Label(self.sidebar, text="Forest: N/A"),
                          "Climate": Label(self.sidebar, text="Climate: N/A"),
                          "Ore": Label(self.sidebar, text="Ore: N/A"),
                          "Desirability": Label(self.sidebar, text="Desirability: N/A"),
                          "Travel": Label(self.sidebar, text="Travel: N/A"),
                          "Empire": Label(self.sidebar, text="Empire: N/A")}

        for i, things in enumerate(self.textboxes.items()):
            key, label = things

            label.grid(row=i + 1, column=0)

        self.cellpx = float(MAP_SIZE) / map.size
        print(self.cellpx)

        g = 3

        x = 0

        self.canvas.create_line(g, g, g, MAP_SIZE)  # leftmost grid line

        while x <= MAP_SIZE:
            self.canvas.create_line(x, MAP_SIZE, x, 0)  # vertical lines
            x += self.cellpx

        y = 0

        self.canvas.create_line(g, g, MAP_SIZE, g)  # Topmost grid line

        while y <= MAP_SIZE:
            self.canvas.create_line(0, y, MAP_SIZE, y)  # horizontal lines
            y += self.cellpx

        self.img = PhotoImage(width=MAP_SIZE, height=MAP_SIZE)
        self.canvas.create_image((MAP_SIZE / 2, MAP_SIZE / 2), image=self.img, state="normal")

        self.canvas.bind("<Button-1>", self._click_callback)

        self.last_clicked = None

    def _click_callback(self, event):
        print("clicked at", event.x, event.y)

        location = (int(math.floor(event.x / self.cellpx)), int(math.floor(event.y / self.cellpx)))

        if self.last_clicked is not None:
            self[self.last_clicked] = "#FFFFFF"
            self.color_empires()

        self[location] = "#0000FF"

        self.last_clicked = location

        # self.textboxes["Location"].config(text="Location: " + str(self.map[location].location))
        # self.textboxes["Population"].config(text="Population: " + str(self.map[location].population))

        for name, val in self.map[location].properties.items():
            self.textboxes[name].config(text=name + ": " + str(val))

    def _get_cell_coords(self, location):
        top_left = (location[0] * self.cellpx, location[1] * self.cellpx)
        bottom_right = (top_left[0] + self.cellpx, top_left[1] + self.cellpx)
        return top_left, bottom_right

    # def __getitem__(self, item):
    #     if len(item) != 2:
    #         raise IndexError("The index must be [x, y] coordinates")
    #     return self.img.get(item[0], [1])

    # def __setitem__(self, key, value):
    #     if len(key) != 2:
    #         raise IndexError("The index must be [x, y] coordinates")
    #     self.img.put(value, key)

    def __setitem__(self, location, color):
        if len(location) != 2:
            raise ValueError("The location must be [x, y] coordinates")

        self.map[location].color = color

        top_left = ((location[0] * self.cellpx), (location[1] * self.cellpx))
        bottom_right = ((top_left[0] + self.cellpx), (top_left[1] + self.cellpx))
        self.canvas.create_rectangle(top_left, bottom_right, fill=color)
        self.canvas.addtag_closest(location, top_left[0], top_left[1])

    def turn(self):
        self.map.turn()
        if self.last_clicked is not None:
            for name, val in self.map[self.last_clicked].properties.items():
                self.textboxes[name].config(text=name + ": " + str(val))

        for row in self.map.grid:
            for cell in row:
                top_left = (cell.properties["Location"][0] * self.cellpx, cell.properties["Location"][1] * self.cellpx)
                bottom_right = (top_left[0] + self.cellpx, top_left[1] + self.cellpx)
                self.canvas.create_rectangle(top_left, bottom_right, fill=cell.color)
                self.canvas.addtag_closest(cell.properties["Location"], top_left[0], top_left[1])

        for name, empire in self.empires.items():
            empire.turn()

    def add_empire(self, empire):
        self.empires[empire.name] = empire
        self.color_empires()

    def color_empires(self):
        for name, empire in self.empires.items():
            empire.color_cells()
