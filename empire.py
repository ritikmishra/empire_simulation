import random
class Empire:
    def __init__(self):
        self.territory = []
        self.mine_alloc = random.uniform()
        self.chop_alloc = 1 - self.mine_alloc

        self.metals = 0
        self.wood = 0
    def turn(self):
        for cell in self.territory:
            self.metals += cell.mineOre(self.mine_alloc * cell.properties["Population"])
            # chop trees
            # recruit troops
            pass
        # expand