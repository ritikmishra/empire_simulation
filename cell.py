import random

import math


class Cell:
    def __init__(self):
        self.properties = {}

        self.color = "#FFFFFF"

        self.invade_multiplier = None
        self.exvade_multiplier = None

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

        result.properties["Forest"] = random.random()  # Percent of land with forest

        result.properties["Climate"] = random.gauss(0, 20)  # deviation from 23 degrees centigrade

        result.properties["Ore"] = max(random.gauss(10, 20), 0)  # amount of ore in the land

        result.properties["Population"] = random.gauss(50, 15)
        result.base_death_rate = random.gauss(0.5, 0.25)  # gaussian
        result.base_birth_rate = result.base_death_rate + random.uniform(0.1,
                                                                         0.5)  # death_rate + uniform \in [-0.2, 0.2]

        result.properties["Desirability"] = result.properties["Land Area"] \
                                            * (result.properties["Ore"] + result.properties["Forest"]
                                               + result.properties["Livestock"]
                                               + result.properties["Land Fertility"]) \
                                            + Cell._tempAdjustFunc(result.properties["Climate"])
        result.properties["Travel"] = math.sqrt(result.properties["Mountainous"] \
                                                * result.properties["Land Area"])  # lower = better

        return result

    def growPop(self):
        # print("I grew a pop!")
        self.properties["Population"] = ((1 - self.base_death_rate) * self.properties["Population"]) + (
            (1 + self.base_birth_rate) * self.properties["Population"])

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

        extract = Cell._oreFunc(self.properties["Ore"])
        self.properties["Ore"] -= extract

        return labor * extract

    """
    Takes in the number of people that are chopping the trees
    Outputs the number of wood extracted from the trees 
    """
    def chopTrees(self, labor):
        return self._oreFunc(self.properties["Forest"] * self.properties["Land Area"] * 100) * labor


    """
    When mining ore, this func defines the amount of ore extracted
    """
    @staticmethod
    def _oreFunc(x):
        return 1.021865 ** x
