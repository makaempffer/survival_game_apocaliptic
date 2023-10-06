from settings import *
from functions import apply_resistance
from inventory import Item
from pygame.sprite import Group
# Add hunger and thirst to the health object
# TODO FINISH RADIATION SYSTEM
# TODO GET PASSIVE BONUSES FROM THE EQUIPED ITEMS SUCH AS ARMOR, RADIATION RES, ETC.

class HealthEffects:
    """Class that applies all the corresponding effects to the user,
    bleeding, broken bones, etc.
    ## Requires a health object reference."""
    def __init__(self, user_health_ref, inventory_ref):
        self.health = user_health_ref
        self.inventory = inventory_ref
        self.bleeding: bool = False
        self.stomach_size = 50
        self.bladder_size = 50
        self.bleed_resistance = 10
        self.equiped_index = 0
        self.environment_radiation = 0
        self.current_radiation = 0
        self.radiation_resistance = 10 # SHOULD BE INCREASED BY SKILLS AND EQUIPABLE ITEMS.
        ## EQUIPABLE SLOTS
        self.equiped_items = Group()
        self.equiped_list = []
        self.max_weight = 50
        self.slot_amount = 3
        # calculate somehow this value
        # Creating item frames
        self.equipable_slots_frame(self.slot_amount)
        
    def equipable_slots_frame(self, slots_amount=3):
        """Creates item slots for equipables"""
        self.inventory.get_inventory_weight()
        ###
        for x in range(slots_amount):
            slot = Item(self.inventory.x_start - 64 + (x * 12), self.inventory.y_start, "ITEM_FRAME")
            self.equiped_items.add(slot)
            self.equiped_list.append(slot)
            
    def set_environment_radiation(self, block):
        if not block:
            return
        if block:
            print(f"[*] - BLOCK {block.type}")
            print(f"RADIATION_LEVEL: {block.radiation_level}")
            self.environment_radiation = block.radiation_level
            
    def render_slots(self):
        self.equiped_items.draw(self.inventory.screen)
        
    def radiation_effect(self):
        print(self.environment_radiation)
        taken_radiation = apply_resistance(self.environment_radiation, self.radiation_resistance, RESISTANCE_FACTOR)
        if self.environment_radiation > self.radiation_resistance:
            self.current_radiation += taken_radiation
        if self.current_radiation >= 1:
            self.health.receive_damage(taken_radiation)
        elif self.current_radiation < 0:
            self.current_radiation = 0
    
    def overcumbered_effect(self):
        if self.inventory.get_inventory_weight() > self.max_weight:
            print("[HEALTH-EFFECTS] - OVER ENCUMBERED.")
            difference = self.inventory.get_inventory_weight() - self.max_weight
            # Example: self.state_icons.show("encumbered")
            self.health.receive_damage(0.1 * difference)
        
    def affections(self):
        pass
    
    def bleeding_effect(self):
        # Get the last hit part when the bleeding started and save it
        pass
    
    def withdrawal_effect(self):
        pass
    
    def needs_effect(self):
        if self.health.hunger <= 0 or self.health.thirst <= 0:
            # Example: self.state_icons.show("bleed")
            # Following code is what ever happens as consecuence.
            self.health.receive_damage(0.2)
            
    def basic_update(self):
        ### DISPLAY STATUS ICONS HERE!! encumbered, bleeding, etc.
        self.needs_effect()
        self.overcumbered_effect()
        self.radiation_effect()
        
    def physical_updates(self):
        
        self.basic_update()
        amount = 0.1
        self.health.hunger -= amount
        self.health.thirst -= amount    
    
    def reset_equiped_list(self):
        self.equiped_list.clear() 
        for item in self.equiped_items:
            self.equiped_list.append(item)
            print("[HEALTH-EFFECTS] - EQUIPABLE LIST RESET")
            
    def equip_item(self, item):
        self.reset_equiped_list()
        if self.equiped_index >= len(self.equiped_items):
            self.equiped_index = 0
        slot = self.equiped_list[self.equiped_index]
        if item.equipable:
            slot.set_item_to(item.item_id)
            self.equiped_index += 1
            
    def get_gun(self) -> Item:
        for item in self.equiped_list:
            if item.item_type == "gun":
                print("User has Gun!")
                return item
        print("No gun.")
        return False

    def get_armor_rating(self) -> float:
        armor = 0
        for item in self.equiped_list:
            if item.item_type == "clothing":
                armor += item.armor
        return armor
            
    def consume_item_effect(self, item):
        
        if item.item_type:
            print(f"[HEALTH-EFFECTS] -> ITEM: {item}")
            if item.item_type == "hemostat":
                print("[HEALTH-EFFECTS] - HEMOSTAT APPLIED.")
                self.bleeding = False
                
            elif item.item_type == "food":
                print(f"[HEALTH-EFFECTS] - FOOD CONSUMED {item.item_id}")
                satisfy_amount = float(item.amount)
                self.health.hunger += satisfy_amount
                if self.stomach_size < self.health.hunger:
                    self.receive_damage(satisfy_amount//2)
                    
            elif item.item_type == "drink":
                print(f"[HEALTH-EFFECTS] - DRINK CONSUMED {item.item_id}")
                satisfy_amount = float(item.amount)
                self.health.thirst += satisfy_amount
                if self.bladder_size < self.health.thirst:
                    self.receive_damage(satisfy_amount//2)
                    
            elif item.item_type == "analgesic":
                # Do something
                print(f"[HEALTH-EFFECTS] - CONSUMED ANALGESIC. {item.item_id} {item.amount}")
                
            elif item.item_type == "drug":
                print(f"[HEALTH-EFFECTS] - CONSUMED {item.item_id}")
                self.current_radiation -= item.amount
                
