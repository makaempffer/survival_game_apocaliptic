from settings import *
from random import randrange
from npc import NPC
class NPCManager():
    def __init__(self, screen, width=WIDTH, height=HEIGHT):
        self.npc_group = pg.sprite.Group()
        self.screen = screen
        self.map = []
        self.sizeX, self.sizeY = width, height
        self.setupNpc()

    def get_npcs(self):
        for npc in self.npc_group: return npc
    
    def npcEvent(self):
        self.npc_group.move()

    def setupNpc(self):
        self.create_spawns()
        self.spawn()

    def spawn_npc(self,x, y,type="zombie"):
        self.npc_group.add(NPC(x, y, type))

    def render(self):
        self.npc_group.draw(self.screen)

    def create_spawns(self):
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
                    if x == 45 and y == 40:
                        self.spawn_npc(x, y, "trader")
                        continue
                    if self.map[x][y] >= -0.4 and self.map[x][y] <= -0.3:
                        choice = randrange(0, 10)
                        if choice > 8:
                            self.spawn_npc(x, y, "zombie") 
            print("[NPC-M] - NPC SPAWN DONE")

