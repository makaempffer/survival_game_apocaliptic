import pygame as pg
from health import Health
from inventory import Inventory
class Player(pg.sprite.Sprite):
    def __init__(self, menu):
        super().__init__()
        self.health = Health("Player")
        self.inventory = Inventory()
        self.posX = 400
        self.posY = 400
        self.menu = menu
        self.rect = pg.Rect(self.posX, self.posY, 10, 10)
        self.image = pg.image.load("./assets/character_player.png")
        self.lastCommand = ""
        self.counter = 0
        self.cooldown = 3
        self.doAction = True
        self.isWalking = False
        self.walkSound = pg.mixer.Sound('./sounds/walk.mp3')
        self.triggered = False
        self.combat_triggered = False
        self.vision_distance = 30
        self.timer = pg.USEREVENT + 1
        self.time_delay = 1000
        pg.time.set_timer(self.timer, self.time_delay)

    def behavior_controller(self):
        #prevent player from moving when in battle
        if self.combat_triggered == False and self.health.is_alive:
            self.movement()
        if self.combat_triggered == True:
            self.walkSound.stop()

    def walk(self, target):
        
        if self.health.is_alive and self.isWalking == True and self.triggered == False and self.combat_triggered == False:
            self.walkSound.set_volume(0.2)
            self.walkSound.play(1, 0, 2000)
            
            self.triggered = True
        if self.combat_triggered == True or self.health.is_alive == False:
            self.walkSound.fadeout(2000)
        if target == None:
            self.walkSound.fadeout(2000)
            self.triggered = False

    def update(self):
        self.behavior_controller()
        self.health.update(self)
    
    def timer_event(self, event):
        if event.type == self.timer:
            self.counter += 1
        

    def counter_timer(self) -> bool:
        if self.counter >= self.cooldown:
            self.counter = 0
            return True
        else:
            return False
    
    def movement(self):
        if self.counter_timer():
            self.doAction = True
        
        if self.doAction:
        
            action = self.menu.getAction()
            if action != None:
                
                self.lastCommand = action
                self.isWalking = True
            if self.lastCommand:
                #print("Action:", action, "Last Command:", self.lastCommand)
                if self.lastCommand == "Walk" and self.menu.savedLocation:
                    targetLocation = self.menu.savedLocation
                    targetLocation[0] = (targetLocation[0] // 10) * 10
                    targetLocation[1] = (targetLocation[1] // 10) * 10
                    #print("Starting point:", self.menu.startingPoint)
                    #print(self.rect.x, targetLocation[0], self.rect.y, targetLocation[1])

                    if self.rect.x == targetLocation[0] and self.rect.y == targetLocation[1]:
                        targetLocation = None
                        self.lastCommand = None
                        self.isWalking = False
                        self.walk(targetLocation)
                        return
                        
                    self.walk(targetLocation)
                    if targetLocation:
                        
                        distX = (self.rect.x - targetLocation[0])
                        distY = (self.rect.y - targetLocation[1])

                        
                        if distX > 0:
                            self.rect.x, self.rect.y = self.rect.x - 10, self.rect.y
                        elif distX < 0:
                            self.rect.x, self.rect.y = self.rect.x + 10, self.rect.y
            
                        if distY > 0: 
                            self.rect.x, self.rect.y = self.rect.x, self.rect.y - 10
                        elif distY < 0: 
                            self.rect.x, self.rect.y = self.rect.x, self.rect.y + 10
                    self.doAction = False   

        
