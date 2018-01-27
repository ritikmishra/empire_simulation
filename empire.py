import random

import functools

import math

from map import Map


class Empire:
    kP = 0
    ADULT_PERCENT = 0.65
    APP = None

    @staticmethod
    def _randColor():
        r = lambda: random.randint(0, 255)
        color = '#%02X%02X%02X' % (r(), r(), r())
        return color

    def __init__(self, name, capital):
        self.name = name
        self.color = Empire._randColor()
        self.territory = {capital}
        self.mine_alloc = random.uniform(0, 1)
        self.chop_alloc = 1 - self.mine_alloc

        self.metals = 0
        self.wood = 0
        self.travel = 0
        self.land_area = 0
        self.pop = 0


        self.military_strength = 1
        self.new_territories = set()

    def turn(self):
        self.metals = 0
        self.wood = 0
        self.pop = 0
        for cell in self.territory:
            cell.properties["Empire"] = self.name
            available_labor = Empire.ADULT_PERCENT * cell.properties["Population"]
            self.metals += cell.mineOre(self.mine_alloc * available_labor)
            self.wood += cell.chopTrees(self.chop_alloc * available_labor)
            self.pop += cell.properties["Population"]
            if self.metals == float("inf"):
                raise Exception("what the frickin heck")
            self.land_area += cell.properties["Land Area"] - 0.5
            self.travel += cell.properties["Travel"]

            # recruit troops


        self.military_strength = (self.pop * Empire.kP + self.metals + self.wood)
        # self.mine_alloc = self.metals / self.military_strength
        # self.chop_alloc = 1 - self.mine_alloc
        if self.military_strength < 0:
            print("WARN:", self.name, "neg mil strength", "Metals:", self.metals, "Wood:", self.wood)


        self.expand_to_nearby()
        self.color_cells()


    def color_cells(self):
        for cell in self.territory:
            cell.color = self.color
            cell.properties["Empire"] = self.name

    def expand_to_nearby(self):
        self.new_territories = set()
        for cell in self.territory:
            a, b = cell.properties["Location"]
            if random.random() < 0.01:
                cells_in_radius = Empire.APP.map.getCellsInRadius(2, (a, b))
                reduction = 2
                print(self.name, "got inspired!")
            else:
                cells_in_radius = Empire.APP.map.getCellsInRadius(1, (a, b))
                reduction = 1
            for cell in cells_in_radius:
                self.new_territories.add(cell)

        self.new_territories = list(set(self.new_territories))

        new_territories_cell = [x for x in sorted([Empire.APP.map[x, y] for x, y in self.new_territories if 0 <= x < Empire.APP.map.size and 0 <= y < Empire.APP.map.size], key=lambda cell: cell.properties["Desirability"]) if x.properties["Empire"] == "Unconquered"]


        for cell in new_territories_cell:
            if self.military_strength > 0:
                    self.territory.add(cell)
                    self.military_strength -= (random.gauss(50, 10) + cell.properties["Desirability"]) / reduction

    """Very power-hungry, slow method."""
    def invade(self, other_empires):

        for other_empire in other_empires:
            if other_empire.name != self.name:

                invaded_territory = set()

                invadable_territory = other_empire.territory & self.getBeyondBorders()

                for cell in invadable_territory:
                    target_military_strength = (cell.properties["Desirability"] + (other_empire.military_strength/len(other_empire.territory))) / self.military_strength
                    if self.military_strength > target_military_strength > 0:
                        invaded_territory.add(cell)
                        self.military_strength -= target_military_strength

                other_empire.territory = other_empire.territory - invaded_territory
                self.territory = self.territory | invaded_territory

    """Also a very power hungry slow method"""
    def getBeyondBorders(self):
        borders = set()
        for cell in self.territory:
            x, y = cell.properties["Location"]
            radius = Empire.APP.map.getCellsInRadius(1, (x, y))
            borders = borders.union(radius)

        border_cells = set(Empire.APP.map[x, y] for x, y in borders)

        return border_cells - self.territory

    def getBoundary(self):
        N = len(self.territory)
        points = [x.properties["Location"] for x in self.territory]
        if N == 1:
            return points
        # let points[N+1] = the array of points

        min_point = points[0]
        for point in points:
            if point is not None:
                if point[1] < min_point[1]:
                    min_point = point
        a = points.index(min_point)
        points[0], points[a] = points[a], points[0]

        def find_polar_angle(p):
            dy = (p[1]-min_point[1])
            dx = (p[0]-min_point[0])

            if dx == 0:
                if dy > 0: return math.pi / 2
                elif dy < 0: return - math.pi / 2
                else: return 0
            return math.atan(dy/dx)

        sorted_points = sorted(points[1:], key=find_polar_angle)
        points = [None, min_point] + sorted_points

        # We want points[0] to be a sentinel point that will stop the loop.
        points[0] = points[N]

        # M will denote the number of points on the convex hull.
        M = 1
        for i in range(2, N):
            # Find next valid point on convex hull.
            while Map.ccw(points[M-1], points[M], points[i]) <= 0:
                if M > 1:
                    M -= 1
                    continue
                # All points are collinear
                elif i == N:
                    break
                else:
                    i += 1

            # Update M and swap points[i] to the correct place.
            M += 1
            points[M], points[i] = points[i], points[M]
        return points[:M+1]



