from cell import Cell
from map import Map
if __name__ == '__main__':
    size = 30
    map = Map(size)

    for x in range(5):
        map[0,4].growPop()
        print(map[0,4].properties["Population"])
    print("b")
