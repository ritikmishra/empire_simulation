import random


class Empire:
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
        self.military_strength = 1
        self.new_territories = set()

    def turn(self):
        for cell in self.territory:
            cell.properties["Empire"] = self.name
            available_labor = Empire.ADULT_PERCENT * cell.properties["Population"]
            self.metals += cell.mineOre(self.mine_alloc * available_labor)
            self.wood += cell.chopTrees(self.chop_alloc * available_labor)
            # recruit troops

        self.expand_to_nearby()
        self.color_cells()

        self.military_strength = self.metals + self.wood
        if self.military_strength < 0:
            print("WARN:", self.name, "neg mil strength", "Metals:", self.metals, "Wood:", self.wood)


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
                print(self.name, "got inspired!")
            else:
                cells_in_radius = Empire.APP.map.getCellsInRadius(1, (a, b))
            for cell in cells_in_radius:
                self.new_territories.add(cell)

        new_territories = list(set(self.new_territories))

        for x, y in new_territories:
            if self.military_strength > 0:
                if 0 <= x < Empire.APP.map.size and 0 <= y < Empire.APP.map.size:
                    self.territory.add(Empire.APP.map[x, y])
                    self.military_strength -= random.gauss(50, 10) + Empire.APP.map[x, y].properties["Desirability"]

    def invade(self, other_empires):

        for other_empire in other_empires:
            if other_empire.name != self.name:

                invaded_territory = set()

                invadable_territory = other_empire.territory & Empire.APP.map.getAdjacentLocs(self.new_territories)

                for cell in invadable_territory:
                    target_military_strength = 2 * (cell.properties["Desirability"] + self.military_strength) / self.military_strength
                    if self.military_strength > target_military_strength > 0:
                        invaded_territory.add(cell)
                        self.military_strength -= target_military_strength
                other_empire.territory = other_empire.territory - invaded_territory
                self.territory = self.territory | invaded_territory



