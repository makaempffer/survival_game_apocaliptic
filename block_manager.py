from settings import *
from block import Block
class BlockManager:
    def __init__(self, screen, mapData):
        self.group = pg.sprite.Group()
        self.screen = screen
        self.mapData = mapData
        self.coordinatesGroup = []
        self.fillGroup()
        
    def render(self):
        self.group.draw(self.screen)

    def fillGroup(self):
        print("[BLOCK-MNG] - FILLING MAP...")
        for x, row in enumerate(self.mapData):
            block = Block(self.mapData[x][0], self.mapData[x][1], self.mapData[x][2])
            self.group.add(block)
            self.mapData[x].append(block.type)
        print("[BLOCK-MNG] - BLOCK GROUP FILLED.")

