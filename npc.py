from settings import *
from random import randint, choice
from health import Health
from inventory import Inventory
from new_combat import Combat
from skills import Skills
from health_effects import HealthEffects

class NPC(pg.sprite.Sprite):
    def __init__(self, x, y, npc_type):
        super().__init__()
        self.health = Health(npc_type)
        self.inventory = Inventory()
        self.skills = Skills()
        self.combat = Combat(self)
        self.health_effects = HealthEffects(self.health, self.inventory)
        self.size = BLOCK_SIZE
        self.position = pg.Vector2(x, y)
        self.rect = None
        self.path = "./assets/blocks/zombie.png"
        self.image = pg.image.load(self.path)
        self.rect = pg.Rect(self.position.x * self.size, self.position.y * self.size, 10, 10)
        self.type = npc_type
        self.didMove = False
        self.isMoving = False
        self.stopAction = False
        self.recalculate = True
        self.target = []
        self.resetTime = randint(500, 3000)
        self.counter = 0
        self.actionCooldown = randint(100, 1000)
        self.doAction = True
        self.friendly = False
        self.combat_triggered = False
        self.vision_distance = 30
        self.get_type()
        self.inventory.add_item("BANDAGE", 1)

    def load_texture(self, type="zombie"):
        path = "./assets/blocks/" + type + ".png"
        self.image = pg.image.load(path)

    def get_type(self):
        self.load_texture(self.type)
        self.setup_behavior()

    def setup_behavior(self):
        if self.type == "zombie":
            self.friendly = False
        elif self.type == "trader":
            self.friendly = True
            self.vision_distance = 0

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def moveEventFunction(self):
        self.counter += 1
        if self.counter == self.resetTime:
            self.recalculate = True
            self.counter = 0
        
        if self.counter == self.actionCooldown:
            self.doAction = True
        if self.counter != self.actionCooldown:
            self.doAction = False

        

    def update(self):
        if not self.friendly:
            self.health.update(self)
        self.moveEventFunction()
        if self.doAction and not self.combat_triggered:
            self.move()
        
    
    def move(self):
        self.position.x, self.position.y = self.rect.x, self.rect.y
        targetLocation = None
        if self.recalculate == True:
            targetLocation = self.getMoveLocation()
            self.recalculate = False
        else:
            targetLocation = self.target 
        if self.isMoving:
            if targetLocation and self.isMoving:
                distX = (self.rect.x - targetLocation[0])
                distY = (self.rect.y - targetLocation[1])

                if distX > 0:
                    self.setPosition(self.rect.x - BLOCK_SIZE, self.rect.y)
                if distX < 0:
                    self.setPosition(self.rect.x + BLOCK_SIZE, self.rect.y)
                if self.rect.x == targetLocation[0] and self.rect.y == targetLocation[1]:
                    targetLocation = None
                    self.isMoving = False

                
                if distY > 0: 
                    self.setPosition(self.rect.x, self.rect.y - BLOCK_SIZE)
                if distY < 0: 
                    self.setPosition(self.rect.x, self.rect.y + BLOCK_SIZE)
            
        #neighbors = self.getNeighbors()
        #self.rect.x = neighbors[0]
        #self.getMoveLocation()
        #self.rect.y = neighbors[2]

    def getMoveLocation(self):
        if self.recalculate:
            possibleMovements = []
            
            gridX, gridY = self.rect.x, self.rect.y
            left = [gridX - 0, gridX - 12, gridX - 24, gridX - 36, gridX - 48]
            right = [gridX + 0, gridX + 12, gridX + 24, gridX + 36, gridX + 48]
            up = [gridY - 0, gridY - 12, gridY - 24, gridY - 36, gridY - 48]
            bottom = [gridY + 0, gridY + 12, gridY + 24, gridY + 36, gridY + 48]
            xMoves = [left, right]
            yMoves = [up, bottom]
            xMovement = choice(xMoves)
            yMovement = choice(yMoves)
            moveChoiceX = choice(xMovement)
            moveChoiceY = choice(yMovement)
            self.isMoving = True
            self.target = [moveChoiceX, moveChoiceY]
            return [moveChoiceX, moveChoiceY]

    
    def getNeighbors(self):
        left = self.rect.x - BLOCK_SIZE
        right = self.rect.x + BLOCK_SIZE
        top = self.rect.y - BLOCK_SIZE
        bottom = self.rect.y + BLOCK_SIZE 
        return [left, right, top, bottom]