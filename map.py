from cell import Cell
import random

class Map:
    def __init__(self, size):
        self.grid = [[None for y in range(size)] for x in range(size)]
        self.size = size

        for y, row in enumerate(self.grid):
            for x, point in enumerate(row):
                self.grid[y][x] = Cell.randomGen((x, y))

    def turn(self):
        print("Watering the map . . .")
        for row in self.grid:
            for cell in row:
                cell.growPop()

    def __getitem__(self, key):
        if type(key) is not tuple:
            raise IndexError("Index must be tuple of size 2")
        if len(key) != 2:
            raise IndexError("Index must be tuple of size 2")
        return self.grid[key[1]][key[0]]