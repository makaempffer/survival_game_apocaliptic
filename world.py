from settings import *
class World:
    def __init__(self, sizeX, sizeY):
        self.map = []
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.createMap()
        self.mapData = []
        self.view()
        self.cols = 0
        self.rows = 0

    def createMap(self):
        noise = PerlinNoise(octaves=7, seed=1)
        xpix, ypix = HEIGHT//10, WIDTH//10
        self.rows, self.cols = (self.sizeX//10, self.sizeY//10)
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
