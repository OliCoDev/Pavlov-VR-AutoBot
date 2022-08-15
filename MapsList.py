import random

maps = []


def getMap():
    global maps
    if len(maps) == 0:
        return None
    return maps.pop(0)


def addMap(newMap):
    global maps
    maps.append(newMap)
    print("New length:", len(maps))


def shuffle():
    global maps
    for i in range(len(maps)):
        randomPos = random.randint(0, len(maps) - 1)
        tempMap = maps[randomPos]
        maps[randomPos] = maps[i]
        maps[i] = tempMap
