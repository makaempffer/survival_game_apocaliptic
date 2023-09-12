import pygame as pg
from health import Health
from inventory import Inventory
class Player(pg.sprite.Sprite):
    def __init__(self, menu, narrator = None):
        super().__init__()
        self.health = Health("Player")
        self.hunger = 0
        self.thirst = 0
        self.inventory = Inventory()
        self.posX = 400
        self.posY = 400
        self.menu = menu
        self.narrator = narrator
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
        self.last_action = ""
        pg.time.set_timer(self.timer, self.time_delay)

    def update_time_effects(self):
        print(f"[PLAYER] - HUNGER {self.hunger} THIRST {self.thirst}")
        self.hunger += 0.03
        self.thirst += 0.05

    def check_effects(self):
        """Check if the player should start losing health according to health/hunger"""
        MAX_STARVATION = 10
        if self.hunger >= MAX_STARVATION:
            self.health.receive_damage(0.1)
            print("[PLAYER] - STARVING.")
        if self.thirst >= MAX_STARVATION:
            self.health.receive_damage(0.1)
            print("[PLAYER] - DEHYDRATED.")

    def get_stats_text(self):
        """Returns player stats on presentable format"""
        message = "HUNGER: " + str(round(self.hunger, 2)) + " THIRST: " + str(round(self.thirst, 2))
        self.narrator.set_constant_text(("HP: " + str(self.health.get_total_hp())), " ACTION: " + self.last_action)
        self.narrator.append_message(message)
        
    def set_narrator(self, narrator):
        self.narrator = narrator

    def behavior_controller(self):
        #prevent player from moving when in battle
        if self.combat_triggered == False and self.health.is_alive:
            self.movement()
        if self.combat_triggered == True:
            self.walkSound.stop()

    def set_current_action(self, action):
        if self.last_action != action:
            self.last_action = action

    def walk(self, target):
        if self.health.is_alive and self.isWalking == True and self.triggered == False and self.combat_triggered == False:
            self.walkSound.set_volume(0.2)
            self.walkSound.play(1, 0, 2000)
            self.last_action = "Walking..."
            
            self.triggered = True
        if self.combat_triggered == True or self.health.is_alive == False:
            self.walkSound.fadeout(2000)

        if target == None:
            self.walkSound.fadeout(2000)
            self.triggered = False

    def update(self):
        self.behavior_controller()
        self.health.update(self)
        self.check_effects()
    
    def timer_event(self, event):
        if event.type == self.timer:
            self.counter += 1

    def counter_timer(self) -> bool:
        if self.counter >= self.cooldown:
            self.counter = 0
            self.update_time_effects()
            self.get_stats_text()
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

        
