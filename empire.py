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
        self.territory = [capital]
        self.mine_alloc = random.uniform(0, 1)
        self.chop_alloc = 1 - self.mine_alloc

        self.metals = 0
        self.wood = 0

    def turn(self):
        for cell in self.territory:
            cell.properties["Empire"] = self.name
            available_labor = Empire.ADULT_PERCENT * cell.properties["Population"]
            self.metals += cell.mineOre(self.mine_alloc * available_labor)
            self.wood += cell.chopTrees(self.chop_alloc * available_labor)
            # recruit troops
        self.expand_to_nearby()
        self.color_cells()

    def color_cells(self):
        bois = 0
        print(len(self.territory))
        for cell in self.territory:
            # print("doing a color wit color", self.color)
            if Empire.APP.canvas.itemcget(cell.properties["Location"], "fill") != self.color:
                print(Empire.APP.canvas.itemcget(Empire.APP.colormap[cell.properties["Location"]], "fill"))
                bois += 1
                Empire.APP.canvas.delete(Empire.APP.colormap[cell.properties["Location"]])
                Empire.APP[cell.properties["Location"]] = self.color
        print("recolor bois x", bois)

    def expand_to_nearby(self):
        new_territories = []
        for cell in self.territory:
            a, b = cell.properties["Location"]
            new_territories.append((a, b + 1))
            new_territories.append((a, b - 1))

            new_territories.append((a + 1, b))
            new_territories.append((a - 1, b))

            new_territories.append((a + 1, b + 1))
            new_territories.append((a - 1, b + 1))

            new_territories.append((a + 1, b - 1))
            new_territories.append((a - 1, b - 1))

        new_territories = list(set(new_territories))

        for x, y in new_territories:
            if 0 <= x < Empire.APP.map.size and 0 <= y < Empire.APP.map.size:
                self.territory.append(Empire.APP.map[x, y])
        self.territory = list(set(self.territory))
