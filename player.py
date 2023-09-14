import pygame as pg
from health import Health
from inventory import Inventory
from sound_system import SoundSystem

class Player(pg.sprite.Sprite):
    def __init__(self, menu, narrator = None):
        super().__init__()
        self.health = Health("Player")
        self.hunger = 0
        self.thirst = 0
        self.inventory = Inventory()
        self.inventory.setup_starting_items()
        self.sound_system = SoundSystem()
        self.sound_system.setup_sounds()
        self.position = pg.Vector2(400, 400)
        self.menu = menu
        self.narrator = narrator
        self.rect = pg.Rect(self.position.x, self.position.y, 10, 10)
        self.image = pg.image.load("./assets/character_player.png")
        self.lastCommand = ""
        self.counter = 0
        self.interaction_reach = 15
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
        """Player loses health when MAX_STARVATION is reached."""
        MAX_STARVATION = self.health.stomach
        if self.hunger >= MAX_STARVATION:
            self.health.receive_damage(0.1)
            print("[PLAYER] - STARVING.")
            self.set_current_action("Starving...")
        if self.thirst >= MAX_STARVATION:
            self.health.receive_damage(0.1)
            self.set_current_action("Dehydrated...")
            print("[PLAYER] - DEHYDRATED.")

    def get_stats_text(self):
        """Returns player stats on presentable format"""
        message = "HUNGER: " + str(round(self.hunger, 2)) + " THIRST: " + str(round(self.thirst, 2))
        self.narrator.set_constant_text(("HP: " + str(round(self.health.get_total_hp(), 2))), " ACTION: " + self.last_action)
        self.narrator.append_message(message)
        
    def set_narrator(self, narrator):
        self.narrator = narrator

    def behavior_controller(self):
        #prevent player from moving when in battle
        if self.combat_triggered == False and self.health.is_alive:
            self.movement()
        if self.combat_triggered == True:
            self.set_current_action("Fighting.")
            self.walkSound.stop()


    def distance_to(self, position: pg.Vector2):
        distance = self.position.distance_to(position)
        return distance
    
    def gather_action(self, gathered_material: str = "WOOD", amount: int = 1):
        gathered_material = gathered_material.upper()
        block = self.menu.get_selected_block()
        if not self.distance_to(block.position) <= self.interaction_reach:
            print("[PLAYER] - BLOCK TOO FAR.")
            return
        
        self.set_current_action("Gathering...")
        block.gather_resource(amount)
        self.block_resource_update(block)
        self.inventory.add_item(gathered_material, amount)

    def perform_action(self):
        # TODO CALCULATE AMOUNT SOMEHOW
        total = 1
        print("PERFORMING ACTION...")
        action = self.lastCommand
        print(f"ACTION TO PERFORM - {action}")
        if not action:
            return
        action = action.lower()
        if action == "cut tree":
            self.gather_action("wood", 1)
            print("[PLAYER] - GETTING WOOD.")

    def block_resource_update(self, block):
        if block.get_resource_amount() <= 0:
            self.lastCommand = None
            self.set_current_action("Idle.")

    def set_current_action(self, action):
        if self.last_action != action:
            self.last_action = action

    def walk(self, target):
        if self.health.is_alive and self.isWalking == True and self.triggered == False and self.combat_triggered == False:
            self.sound_system.play_sound("walk")
            self.set_current_action("Walking...")
            
            self.triggered = True
        if self.combat_triggered == True or self.health.is_alive == False:
            self.sound_system.fadeout_sound("walk")

        if target == None:
            self.sound_system.fadeout_sound("walk")
            self.triggered = False

    def update(self):
        self.behavior_controller()
        self.health.update(self)
        self.check_effects()
    
    def timer_event(self, event):
        if event.type == self.timer:
            self.counter += 1

    def get_consumed_item(self):
        """Get the consumed item effects, all items to add here."""
        consumed_item = self.inventory.last_consumed
        if not consumed_item:
            return
        if consumed_item.item_id == "BANDAGE":
            print("[PLAYER] - USED BANDAGE")
            most_damaged = self.health.get_most_damaged_part()
            self.health.add_body_part_hp(most_damaged, 10)
            print(self.health.get_total_hp())
            self.set_current_action("Bandaging...")
            self.inventory.kill_consumed()
            # Get the most damaged part and heal it some amount.

    def update_on_timer(self):
        """Function calls to run every time the timer is met."""
        self.update_time_effects()
        self.get_stats_text()
        self.inventory.update_item_player_effects()
        self.get_consumed_item()
        self.perform_action()

    def counter_timer(self) -> bool:
        if self.counter >= self.cooldown:
            self.counter = 0
            self.update_on_timer()
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
                        self.position.x, self.position.y = self.rect.x, self.rect.y
                    self.doAction = False   

        
