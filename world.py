from settings import *
from random import randint

class World:
    def __init__(self, sizeX, sizeY):
        self.map = []
        self.sizeX = sizeX 
        self.sizeY = sizeY
        self.mapData = []
        self.cols = 0
        self.rows = 0
        self.createMap()
        self.view()
        
    def regenerate_map(self):
        seed = randint(1, 500)
        self.createMap(seed)
        self.view()

    def createMap(self, seed=1):
        noise = PerlinNoise(octaves=7, seed=seed)
        xpix, ypix = HEIGHT//BLOCK_SIZE, WIDTH//BLOCK_SIZE
        self.rows, self.cols = (self.sizeX//BLOCK_SIZE, self.sizeY//BLOCK_SIZE)
        arr = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
        self.map = arr
    
    def view(self):
        print("[WORLD] - CREATING WORLD...")
        if len(self.map) > 1:
            for x, row in enumerate(self.map):
                for y, col in enumerate(row):
                    #color = mapFromTo(self.map[x][y], -1, 1, 0, 255)
                    self.mapData.append([x, y, self.map[x][y]])
            print("[WORLD] - WORLD MAP DATA DONE")
