from settings import *
from random import randrange
from npc import NPC
class NPCManager():
    def __init__(self, screen, width=WIDTH, height=HEIGHT):
        self.npcGroup = pg.sprite.Group()
        self.screen = screen
        self.map = []
        self.sizeX, self.sizeY = width, height

    def get_npcs(self):
        for npc in self.npcGroup: return npc
    
    def npcEvent(self):
        self.npcGroup.move()

    def setupNpc(self):
        self.createSpawns()
        self.spawn()

    def spawnNpc(self,x, y,type="zombie"):
        self.npcGroup.add(NPC(x, y, type))

    def render(self):
        self.npcGroup.draw(self.screen)

    def createSpawns(self):
        noise = PerlinNoise(octaves=7, seed=1)
        xpix, ypix = HEIGHT//10, WIDTH//10
        self.rows, self.cols = (self.sizeX//10, self.sizeY//10)
        arr = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
        self.map = arr
        print("[NPC-M] - NPC MAP CREATED")
    
    def spawn(self):
        if len(self.map) > 1:
            for x, row in enumerate(self.map):
                for y, col in enumerate(row):
                    if self.map[x][y] >= -0.4 and self.map[x][y] <= -0.3:
                        choice = randrange(0, 10)
                        if choice > 8:
                            self.spawnNpc(x, y, "zombie") 
            print("[NPC-M] - NPC SPAWN DONE")

