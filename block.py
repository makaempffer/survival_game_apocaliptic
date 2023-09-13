from settings import *
from random import randint

class Block(pg.sprite.Sprite):
    def __init__(self, posX, posY, value):
        super().__init__()
        self.posX = posX    
        self.posY = posY
        self.size = 10
        self.rect = pg.Rect(posX * self.size, posY * self.size, 10, 10)
        self.is_resource = False
        self.resource_amount = 0
        self.value = value
        self.path = "./assets/tree.png"
        self.image = pg.image.load("./assets/water.png")
        self.type = None
        self.data = []
        self.getImage()
        self.setup_resources()

    def reload_image(self, block_name: str):
        path = "./assets/" + block_name + ".png"
        self.image = pg.image.load(path)

    def update(self):
        self.consumable_logic()

    def get_resource_amount(self):
        return self.resource_amount

    def consumable_logic(self):
        if self.resource_amount <= 0:
            self.type == "DIRT"
            self.is_resource = False
            self.reload_image("dirt")

    def harvest_resource(self, amount):
        if self.resource_amount <= 0:
            return 0
        self.resource_amount -= amount
        print(f"[BLOCK] - HARVESTED {amount} LEFT {self.resource_amount}")
        if self.resource_amount < amount:
            amount_left = self.resource_amount
            self.resource_amount = 0
            return amount_left 
        return amount

    def getImage(self):
        #getting and setting the image for the block according to the perlin value
        if self.value >= 0.4 and self.value <= 1:
            self.path = "./assets/water.png"
            self.type = "WATER"
        if self.value >= 0.3 and self.value <= 0.4: 
            self.path = "./assets/sand.png"
            self.type = "SAND"
        if self.value >= -0.2 and self.value <= 0.3: 
            self.path = "./assets/dirt.png"
            self.type = "DIRT"
        if self.value >= -1 and self.value <= -0.2:
            self.path = "./assets/tree.png"
            self.type = "TREE"
            self.is_resource = True

    def setup_resources(self):
        if self.is_resource:
            if self.type == "TREE":
                self.resource_amount = randint(5, 10)
            elif self.type == "WATER":
                self.resource_amount = randint(20, 50)


        self.image = pg.image.load(str(self.path)).convert_alpha()

