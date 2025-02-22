import pygame as pg
from functions import *
from health import Health
from inventory import Inventory
from sound_system import SoundSystem
from health_effects import HealthEffects
from skills import Skills
from combat import Combat
from settings import *
from UI import UI

class Player(pg.sprite.Sprite):
    def __init__(self, menu, screen, narrator = None,):
        super().__init__()
        self.screen = screen
        self.inventory = Inventory()
        self.skills = Skills()
        self.skills.set_skill_level("accuracy", 8)
        self.health = Health(self.skills)
        self.health.setup_organs()
        self.sound_system = SoundSystem()
        self.sound_system.setup_sounds()
        self.sound_system.load_item_sounds_from_dict()
        self.health_effects = HealthEffects(self.health, self.inventory, self.sound_system)
        self.user_interface = UI(self.screen, self)
        self.inventory.logger = self.user_interface.logger
        self.combat = Combat(self, self.user_interface.logger)
        self.inventory.setup_starting_items()
        self.friendly = False
        self.position = pg.Vector2(360, 360)
        self.menu = menu
        self.type = "player"
        self.narrator = narrator
        self.rect = pg.Rect(self.position.x, self.position.y, BLOCK_SIZE, BLOCK_SIZE)
        self.image = pg.image.load("./assets/blocks/character_player.png")
        self.lastCommand = ""
        self.counter = 0
        self.interaction_reach = BLOCK_SIZE + 5
        self.cooldown = 3
        self.doAction = True
        self.is_walking = False
        self.isWalking = False
        self.triggered = False
        self.combat_triggered = False
        self.vision_distance = 30
        self.speed = 0.01
        self.timer = pg.USEREVENT + 1
        self.time_delay = 1000
        self.last_action = ""
        self.MAX_HP = self.health.get_health()
        pg.time.set_timer(self.timer, self.time_delay)

    def update_time_effects(self):
        self.menu.get_block(self.position.x, self.position.y)
        self.health_effects.physical_updates()
        self.health_effects.set_environment_radiation(self.menu.stepped_block)
        
        # Walking effect
        if self.is_walking:
            self.sound_system.play_sound("footstep_gravel")
    
    def show_health_bar(self):
        hp = self.health.get_health()
        pg.draw.line(self.inventory.screen, (255, 0, 0), (self.rect.x, self.rect.y), (self.rect.x + mapFromTo(hp, 0, self.MAX_HP, 0, BLOCK_SIZE), self.rect.y))
        
    def set_narrator(self, narrator):
        self.narrator = narrator
        

    def distance_to(self, position: pg.Vector2):
        distance = self.position.distance_to(position)
        return distance
    
    def gather_action(self, gathered_material: str = "WOOD", amount: int = 1):
        gathered_material = gathered_material.upper()
        block = self.menu.get_selected_block()
        if not self.distance_to(block.position) <= self.interaction_reach:
            print("[PLAYER] - BLOCK TOO FAR.")
            return False
        
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
        action = self.lastCommand
        if action != "walk":
            self.is_walking = False
        #print(f"ACTION TO PERFORM - {action}")
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
            
        elif action == "open stash":
            self.lastCommand = None
            distance = self.position.distance_to(self.menu.startingPoint)
            if distance > self.interaction_reach: return
            
            self.menu.selected_stash.stash.open_stash()
            if self.menu.selected_stash.stash.inventory.is_open:
                #self.menu.selected_stash.stash.inventory.transfer_target = self.inventory
                self.menu.selected_stash.stash.inventory.set_transfer_target(self)
                self.inventory.transfer_target = self.menu.selected_stash.stash
                self.inventory.transfer_mode = True
            else:
                self.inventory.transfer_mode = False

    def stash_logic(self):
        pass
    """if self.menu.selected_stash:
                if not self.menu.selected_stash: return
                if self.position.distance_to(self.menu.selected_stash.position) > self.interaction_reach:
                    if self.menu.selected_stash.stash.inventory:           
                        if self.menu.selected_stash.stash.inventory.is_open:
                            self.menu.selected_stash.stash.open_stash()"""

    def block_resource_update(self, block):
        if block.get_resource_amount() <= 0:
            self.lastCommand = None

    def set_current_action(self, action):
        if self.last_action != action:
            self.last_action = action

    def walk(self, target):
        if self.health.alive and self.isWalking == True and self.triggered == False and self.combat_triggered == False:
            self.sound_system.play_sound("walk")
            self.triggered = True

        if self.combat_triggered == True or self.health.alive == False:
            self.sound_system.fadeout_sound("walk")

        if target == None:
            self.sound_system.fadeout_sound("walk")
            self.triggered = False
            
    def check_alive(self):
        if self.health.check_alive == False:
            self.kill()
            
    def update(self, delta_time):
        self.movement(delta_time)
        self.health.update()
        self.check_alive()
        self.stash_logic()
    
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
        if not item:
            return
        
        if item.consumable and self.health_effects.consume_item_effect(item):
            self.user_interface.logger.add_log(f"You consumed {item.item_id.lower()}.", PURPLE)
        self.inventory.kill_consumed()
            
        # Get the most damaged part and heal it some amount.

    def update_on_timer(self):
        """Function calls to run every time the timer is met."""
        self.update_time_effects()
        self.combat.player_combat_logic()
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
        self.user_interface.draw_components()
        self.health_effects.render_slots()
        self.combat.render_enemy_hp()
        self.user_interface.render_text()

    def movement(self, delta_time):
        self.counter_timer()
        if self.lastCommand and self.menu.opened:
            self.lastCommand = None
        if not self.lastCommand:
            self.lastCommand = self.menu.getAction()
        action = self.menu.getAction()
        if action != None and action != self.lastCommand:
            self.lastCommand = action
            
        if self.lastCommand == "Walk" and self.menu.savedLocation:
            target_pos = pg.Vector2(self.menu.savedLocation[0], self.menu.savedLocation[1])
            if self.position == target_pos:
                self.is_walking = False
                self.lastCommand = None
                return
            else:
                self.is_walking = True
                
            if target_pos:
                self.position = self.position.move_towards(target_pos, self.speed * delta_time)
                self.rect.center = self.position
                #self.rect.x, self.rect.y = self.position.x, self.position.y
            self.doAction = False   

        
