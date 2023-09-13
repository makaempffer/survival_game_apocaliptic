from settings import *
from block import Block
class BlockManager:
    def __init__(self, screen, mapData):
        self.group = pg.sprite.Group()
        self.blocks = []
        self.screen = screen
        self.mapData = mapData
        self.coordinatesGroup = []
        self.resource_blocks = []
        self.fill_groups()
        
    def render(self):
        self.group.draw(self.screen)

    def update_resource_blocks(self):
        for block in self.resource_blocks:
            block.update()

    def fill_groups(self):
        print("[BLOCK-MNG] - FILLING MAP...")
        for x, row in enumerate(self.mapData):
            block = Block(self.mapData[x][0], self.mapData[x][1], self.mapData[x][2])
            self.group.add(block)
            self.blocks.append(block)
            self.mapData[x].append(block.type)
            if block.is_resource:
                self.resource_blocks.append(block)

        print("[BLOCK-MNG] - BLOCK GROUP FILLED.")

