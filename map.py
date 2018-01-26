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
            raise IndexError("Index must be tuple of size 2, but was actually " + str(key))
        if len(key) != 2:
            raise IndexError("Index must be tuple of size 2, but was actually " + str(key))
        return self.grid[key[1]][key[0]]

    def rand_select(self):
        loc =  random.randrange(0, self.size), random.randrange(0, self.size)
        return self[loc]

    def getCellsInRadius(self, r, loc):
        if r > 0:
            new_territories = set()
            a = loc[0]
            b = loc[1]

            for dx in range(-r, r+1):
                for dy in range(-r, r+1):
                    new_territories.add((a + dx, b + dy))

            return new_territories

    def getAdjacentLocs(self, locs):
        adj_locs = set()
        for loc in locs:
            radius_locs = self.getCellsInRadius(1, loc)
            for loc in radius_locs:
                adj_locs.add(loc)
        return adj_locs
