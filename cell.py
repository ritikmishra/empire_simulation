import random

import math


class Cell:
    EPSILON = 1e-10

    def __init__(self):
        self.properties = {}

        self.color = "#FFFFFF"

        self.invade_multiplier = None
        self.exvade_multiplier = None

        self.carrying_capacity = None

        self.troops = []
        self.sovereign = 0

        self.base_birth_rate = None  # death_rate + uniform \in [-0.2, 0.2]
        self.base_death_rate = None  # gaussian

    @classmethod
    def randomGen(cls, location):
        result = cls()

        result.properties["Location"] = location  # (x, y) coords of cell on map

        result.properties["Mountainous"] = random.random()  # How mountainous the cell is, on a scale from 0 to 1

        result.properties["Land Area"] = random.random()  # How much of the cell's area isn't water, from 0 to 1

        result.properties["Land Fertility"] = random.random()  # How fertile the land is, from 0 to 1
        result.properties["Livestock"] = random.random()  # Percent of land suitable for livestock ranching

        result.properties["Forest"] = random.betavariate(2, 2)  # Percent of land with forest

        result.properties["Climate"] = random.gauss(0, 20)  # deviation from 23 degrees centigrade

        result.properties["Ore"] = random.betavariate(2, 2)  # Percent of land with forest

        result.properties["Population"] = random.gauss(50, 15)
        result.base_death_rate = random.gauss(0.5, 0.25)  # gaussian
        result.base_birth_rate = result.base_death_rate + random.uniform(0.1,
                                                                         0.5)  # death_rate + uniform \in [-0.2, 0.2]

        result.carrying_capacity = max(result.properties["Population"] * random.betavariate(3.9, 1.3) * 10, result.properties["Population"] *  2)

        result.properties["Desirability"] = result.properties["Land Area"] \
                                            * (result.properties["Ore"] + result.properties["Forest"]
                                               + result.properties["Livestock"]
                                               + result.properties["Land Fertility"]) \
                                            + Cell._tempAdjustFunc(result.properties["Climate"])
        result.properties["Travel"] = math.sqrt(result.properties["Mountainous"] \
                                                * result.properties["Land Area"])  # lower = better

        result.properties["Empire"] = "Unconquered"

        return result

    def growPop(self):
        # print("I grew a pop!")

        dy = self.properties["Population"] * (self.base_birth_rate - self.base_death_rate) * (
        1 - self.properties["Population"] / self.carrying_capacity)

        self.properties["Population"] = self.properties["Population"] + dy

        if self.properties["Population"] == float("-inf") or self.properties["Population"] == float("-inf"):
            raise Exception("what the frickin heck dude")

    """
    When calculating desirability, this function adjusts the temp constant so that pos temp impacts less than neg temp
    """

    @staticmethod
    def _tempAdjustFunc(x):
        n = 0.1
        return - math.e ** (-x * n)

    """
    Takes in the number of people that are mining the ore
    Outputs the number of metals extracted from the ore 
    """

    def mineOre(self, labor):
        if self.properties["Ore"] > 0:
            extract = self._oreFunc(self.properties["Ore"])
            self.properties["Ore"] -= extract

            if math.isnan(extract):
                pass


            return labor * self.properties["Land Area"] * extract
        return 0.0

    """
    Takes in the number of people that are chopping the trees
    Outputs the number of wood extracted from the trees 
    """

    def chopTrees(self, labor):
        dy = (self.properties["Land Fertility"] - self._treeFunc(self.properties["Forest"])) * self.properties[
            "Forest"] * (1 - self.properties["Forest"])
        self.properties["Forest"] -= dy
        if math.isnan(dy):
            print("     ")

        return dy * self.properties["Land Area"] * labor

    """
    When mining ore, this func defines the amount of ore extracted
    """

    @staticmethod
    def _oreFunc(x):
        return math.log(abs(x) + 1)

    @staticmethod
    def _treeFunc(x):
        return -2*x+1
