import pygame as pg
from health import Health
from inventory import Inventory
from sound_system import SoundSystem
from health_effects import HealthEffects
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, menu, narrator = None):
        super().__init__()
        self.health = Health("Player")
        self.inventory = Inventory()
        self.health_effects = HealthEffects(self.health, self.inventory)
        self.inventory.setup_starting_items()
        self.sound_system = SoundSystem()
        self.sound_system.setup_sounds()
        self.friendly = False
        self.position = pg.Vector2(360, 360)
        self.menu = menu
        self.narrator = narrator
        self.rect = pg.Rect(self.position.x, self.position.y, BLOCK_SIZE, BLOCK_SIZE)
        self.image = pg.image.load("./assets/blocks/character_player.png")
        self.lastCommand = ""
        self.counter = 0
        self.interaction_reach = 12
        self.cooldown = 3
        self.doAction = True
        self.isWalking = False
        self.triggered = False
        self.combat_triggered = False
        self.vision_distance = 30
        self.timer = pg.USEREVENT + 1
        self.time_delay = 1000
        self.last_action = ""
        pg.time.set_timer(self.timer, self.time_delay)

    def update_time_effects(self):
        self.menu.get_block(self.position.x, self.position.y)
        self.health_effects.physical_updates()
        self.health_effects.set_environment_radiation(self.menu.stepped_block)
        # Add updates on tick.
        pass


    def get_stats_text(self):
        """Returns player stats on presentable format"""
        message = "HUNGER: " + str(round(self.health.hunger, 2)) + " THIRST: " + str(round(self.health.thirst, 2)) + " RADS: " + str(round(self.health_effects.current_radiation, 2))
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
        

    def distance_to(self, position: pg.Vector2):
        distance = self.position.distance_to(position)
        return distance
    
    def gather_action(self, gathered_material: str = "WOOD", amount: int = 1):
        gathered_material = gathered_material.upper()
        block = self.menu.get_selected_block()
        if not self.distance_to(block.position) <= self.interaction_reach:
            print("[PLAYER] - BLOCK TOO FAR.")
            return False
        
        self.set_current_action("Gathering...")
        block.gather_resource(amount)
        self.block_resource_update(block)
        self.inventory.add_item(gathered_material, amount)
        return True
        
    def is_resource_empty(self) -> bool:
        block = self.menu.get_selected_block()
        if block.is_resource:
            if block.resource_amount <= 0:
                return True
            else:
                return False
        
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
            if self.gather_action("wood", 1):
                self.sound_system.play_sound("wood_chop")
                if self.is_resource_empty():
                    self.sound_system.play_sound("chop_over")
        
        elif action == "fill container":
            self.gather_action("water", 1)
        
        elif action == "place" and self.inventory.selected_item:
            # Place item in the map.
            self.menu.block_manager.insert_item_block(self.position.x, self.position.y, self.inventory.selected_item)
            self.inventory.decrease_item_count(self.inventory.selected_item)
            print(f"[PLYR] - ITEM {self.inventory.selected_item} PLACED.")
            self.inventory.selected_item = None

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
    
    def timer_event(self, event):
        if event.type == self.timer:
            self.counter += 1
        
    def get_equiped(self):
        item = self.inventory.last_equiped
        if item:
            print(f"[PLAYER] - EQUIPED {item.item_id}")
            self.health_effects.equip_item(item)
            self.inventory.last_equiped = None

    def get_consumed_item(self):
        self.get_equiped()
        """Get the consumed item effects, all items to add here."""
        item = self.inventory.last_consumed
        print(f"[PLAYER] - LAST ITEM {item}")
        if not item:
            return
        self.health_effects.consume_item_effect(item)
        print(self.health.get_total_hp())
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
        
    def render_player_related(self):
        self.health_effects.render_slots()


    
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
                    targetLocation[0] = (targetLocation[0] // BLOCK_SIZE) * BLOCK_SIZE
                    targetLocation[1] = (targetLocation[1] // BLOCK_SIZE) * BLOCK_SIZE
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
                            self.rect.x, self.rect.y = self.rect.x - BLOCK_SIZE, self.rect.y
                        elif distX < 0:
                            self.rect.x, self.rect.y = self.rect.x + BLOCK_SIZE, self.rect.y
            
                        if distY > 0: 
                            self.rect.x, self.rect.y = self.rect.x, self.rect.y - BLOCK_SIZE
                        elif distY < 0: 
                            self.rect.x, self.rect.y = self.rect.x, self.rect.y + BLOCK_SIZE
                        self.position.x, self.position.y = self.rect.x, self.rect.y
                    self.doAction = False   

        
