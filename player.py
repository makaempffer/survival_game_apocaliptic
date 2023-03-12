
import pygame as pg
class Player(pg.sprite.Sprite):
    def __init__(self, menu):
        super().__init__()
        self.posX = 400
        self.posY = 400
        self.menu = menu
        self.rect = pg.Rect(self.posX, self.posY, 10, 10)
        self.image = pg.image.load("./assets/character_player.png")
        self.lastCommand = ""
        self.counter = 0
        self.cooldown = 200
        self.doAction = True
        self.isWalking = False
        self.walkSound = pg.mixer.Sound('./sounds/walk.mp3')
        self.triggered = False
        
    
    def walk(self, target):
        
        if self.isWalking == True and self.triggered == False:
            self.walkSound.set_volume(0.2)
            self.walkSound.play(5, 0, 4000)
            
            self.triggered = True
        
        if target == None:
            self.walkSound.fadeout(2000)
            self.triggered = False

    def update(self):
        self.counter += 1
        self.movement()
    
    def movement(self):
        
        
        if self.counter == self.cooldown:
            self.doAction = True
            self.counter = 0
        
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
                            #self.setPosition(self.rect.x - 10, self.rect.y)
                        elif distX < 0:
                            self.rect.x, self.rect.y = self.rect.x + 10, self.rect.y
                            #self.setPosition(self.rect.x + 10, self.rect.y)
            
                        if distY > 0: 
                            self.rect.x, self.rect.y = self.rect.x, self.rect.y - 10
                            #self.setPosition(self.rect.x, self.rect.y - 10)
                        elif distY < 0: 
                            self.rect.x, self.rect.y = self.rect.x, self.rect.y + 10
                            #self.setPosition(self.rect.x, self.rect.y + 10)
                        self.doAction = False   
