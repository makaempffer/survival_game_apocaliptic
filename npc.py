from settings import *
from random import randint, choice
from new_health import Health
from inventory import Inventory
from new_combat import Combat
from skills import Skills
from health_effects import HealthEffects
from functions import mapFromTo

class NPC(pg.sprite.Sprite):
    def __init__(self, x, y, npc_type):
        super().__init__()
        self.inventory = Inventory()
        self.skills = Skills()
        self.combat = Combat(self)
        self.health = Health(self.skills)
        self.health_effects = HealthEffects(self.health, self.inventory)
        self.size = BLOCK_SIZE
        self.rect = pg.Rect(x * self.size, y * self.size, BLOCK_SIZE, BLOCK_SIZE)
        self.position = pg.Vector2(self.rect.x, self.rect.y)
        self.path = "./assets/blocks/zombie.png"
        self.image = pg.image.load(self.path)
        self.type = npc_type
        self.interaction_reach = 12
        self.speed = 0.01
        self.counter = 0
        self.target_reached = False
        self.target_pos = None
        self.can_move = True
        self.friendly = False
        self.vision_distance = 30
        self.cooldown = randint(100, 500)
        self.start_timer = False
        self.get_type()
        self.inventory.add_item("BANDAGE", 1)
        self.max_hp = self.health.get_health()
        
    def show_health_bar(self, screen):
        hp = self.health.get_health()
        pg.draw.line(screen, (255, 0, 0), (self.rect.x, self.rect.y), (self.rect.x + mapFromTo(hp, 0, self.max_hp, 0, BLOCK_SIZE), self.rect.y))

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

    def update(self, delta_time):
        if not self.friendly:
            self.health.update()
        self.move(delta_time)
        self.cooldown_timer()
        self.check_boundaries()
    
    def check_boundaries(self):
        over_shoot = False
        if self.position.x > WIDTH:
            self.position.x = 0
            over_shoot = True
        elif self.position.x < 0:
            self.position.x = WIDTH
            over_shoot = True
            
        if self.position.y > HEIGHT:
            over_shoot = True
            self.position.y = 0
        elif self.position.y < 0:
            over_shoot = True
            self.position.y = HEIGHT
            
        if over_shoot:
            target_pos = self.getMoveLocation()
            target_pos = pg.Vector2(target_pos[0], target_pos[1])
            self.target_pos = target_pos
            
        
    def move(self, delta_time):
        attacker = self.combat.attacker
        if attacker:
            self.position = self.position.move_towards(attacker.position, self.speed * delta_time)
            self.rect.x, self.rect.y = self.position.x, self.position.y
        else:
            if not self.can_move:
                return
            if self.position == self.target_pos:
                self.target_reached = True
                self.can_move = False
                self.start_timer = True
                
            elif self.position != self.target_pos:
                self.target_reached = False
                
            if self.target_reached or not self.target_pos:       
                target_pos = self.getMoveLocation()
                target_pos = pg.Vector2(target_pos[0], target_pos[1])
                self.target_pos = target_pos
                
            if self.target_pos:
                self.position = self.position.move_towards(self.target_pos, self.speed * delta_time)
                self.rect.x, self.rect.y = self.position.x, self.position.y
                
    def cooldown_timer(self):
        if self.start_timer:
            self.counter += 1
            
        if self.counter >= self.cooldown:
            self.can_move = True
            self.counter = 0
            self.start_timer = False
            

    def getMoveLocation(self):            
        gridX, gridY = self.rect.x, self.rect.y
        left = [gridX - 0, gridX - BLOCK_SIZE, gridX - BLOCK_SIZE * 2, gridX - BLOCK_SIZE * 3, gridX - BLOCK_SIZE * 4]
        right = [gridX + 0, gridX + BLOCK_SIZE, gridX + BLOCK_SIZE * 2, gridX + BLOCK_SIZE * 3, gridX + BLOCK_SIZE * 4]
        up = [gridY - 0, gridY - BLOCK_SIZE, gridY - BLOCK_SIZE * 2, gridY - BLOCK_SIZE * 3, gridY - BLOCK_SIZE * 4]
        bottom = [gridY + 0, gridY + BLOCK_SIZE, gridY + BLOCK_SIZE * 2, gridY + BLOCK_SIZE * 3, gridY + BLOCK_SIZE * 4]
        xMoves = [left, right]
        yMoves = [up, bottom]
        xMovement = choice(xMoves)
        yMovement = choice(yMoves)
        moveChoiceX = choice(xMovement)
        moveChoiceY = choice(yMovement)
        self.isMoving = True
        self.target = [moveChoiceX, moveChoiceY]
        return [moveChoiceX, moveChoiceY]