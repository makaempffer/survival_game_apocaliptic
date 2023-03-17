from settings import *
class Block(pg.sprite.Sprite):
    def __init__(self, posX, posY, value):
        super().__init__()
        self.posX = posX    
        self.posY = posY
        self.size = 10
        self.rect = pg.Rect(posX * self.size, posY * self.size, 10, 10)
        self.value = value
        self.path = "./assets/tree.png"
        self.image = pg.image.load("./assets/water.png")
        self.type = None
        self.data = []
        self.getImage()

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

        self.image = pg.image.load(str(self.path)).convert_alpha()