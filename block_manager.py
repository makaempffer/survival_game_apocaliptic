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
        self.generate_map()
        
    def render(self):
        self.group.draw(self.screen)

    def update_resource_blocks(self):
        for block in self.resource_blocks:
            block.update()

    def insert_item_block(self, x, y, item):
        block = Block(x//BLOCK_SIZE, y//BLOCK_SIZE, None, item.item_id)
        print(f"[BLOCK] - TYPE {block.type}")
        self.group.add(block)

    def generate_map(self):
        self.group.empty()
        self.coordinatesGroup.clear()
        self.resource_blocks.clear()
        self.blocks.clear()
        print("[BLOCK-MNG] - FILLING MAP...")
        for x, row in enumerate(self.mapData):
            block = Block(self.mapData[x][0], self.mapData[x][1], self.mapData[x][2])
            self.group.add(block)
            self.blocks.append(block)
            self.mapData[x].append(block.type)
            if block.is_resource:
                self.resource_blocks.append(block)

        print("[BLOCK-MNG] - BLOCK GROUP FILLED.")

