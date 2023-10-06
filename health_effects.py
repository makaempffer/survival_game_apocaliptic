from settings import *
from inventory import Item
from pygame.sprite import Group
# Add hunger and thirst to the health object

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
        ## EQUIPABLE SLOTS
        self.equiped_items = Group()
        # Creating item frames
        self.equipable_slots_frame(3)
        
    def equipable_slots_frame(self, slots_amount=3):
        """Creates item slots for equipables"""
        for x in range(slots_amount):
            slot = Item(self.inventory.x_start - 64 + (x * 12), self.inventory.y_start, "ITEM_FRAME")
            self.equiped_items.add(slot)
            
    def render_slots(self):
        self.equiped_items.draw(self.inventory.screen)
        
    def affections(self):
        pass
    
    def bleeding_effect(self):
        # Get the last hit part when the bleeding started and save it
        pass
        
    def basic_update(self):
        if self.health.hunger <= 0 or self.health.thirst <= 0:
            self.health.receive_damage(0.2)
                
    def physical_updates(self):
        self.basic_update()
        amount = 0.1
        self.health.hunger -= amount
        self.health.thirst -= amount
        
    def equip_item(self, item):
        if item.equipable:
            print("is equipable")
            for _item in self.equiped_items:
                if _item.item_id == "ITEM_FRAME":
                    _item.set_item_to(item.item_id)
                    return
            
            
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
                