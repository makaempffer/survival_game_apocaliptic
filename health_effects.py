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
    def __init__(self, user_health_ref, inventory_ref, sound_system=None):
        self.sound_system = sound_system
        self.health = user_health_ref
        self.inventory = inventory_ref
        self.stomach_size = 50
        self.bladder_size = 50
        self.bleed_resistance = 10
        self.equiped_index = 0
        self.environment_radiation = 0
        self.current_radiation = 0
        self.radiation_shield = 0
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
            slot = Item(self.inventory.x_start - (ITEM_SIZE * slots_amount) + (x * ITEM_SIZE), self.inventory.y_start, "ITEM_FRAME")
            self.equiped_items.add(slot)
            self.equiped_list.append(slot)
            
    def set_environment_radiation(self, block):
        if not block:
            return
        if block:
            #print(f"[*] - BLOCK {block.type}")
            #print(f"RADIATION_LEVEL: {block.radiation_level}")
            self.environment_radiation = block.radiation_level
            
            
    def render_slots(self):
        self.equiped_items.draw(self.inventory.screen)
        
    def radiation_effect(self):
        taken_radiation = apply_resistance(self.environment_radiation, self.radiation_resistance, RADIATION_RES_FACTOR)
        if self.environment_radiation > self.radiation_resistance and self.radiation_shield <= 0:
            self.current_radiation += taken_radiation * RADIATION_EFFECT_FACTOR
        elif self.environment_radiation > self.radiation_resistance and self.radiation_shield > 0:
            self.radiation_shield -= taken_radiation
            
        if self.current_radiation >= 1:
            self.health.take_true_damage(self.current_radiation*RADIATION_DMG_MULTIPLIER)
            
        elif self.current_radiation < 0:
            self.radiation_shield += abs(self.current_radiation)
            self.current_radiation = 0
            
            
        if self.current_radiation > 0 and self.environment_radiation <= self.radiation_resistance:
            self.current_radiation -= 0.02
                
    
    def overcumbered_effect(self):
        if self.inventory.get_inventory_weight() > self.max_weight:
            print("[HEALTH-EFFECTS] - OVER ENCUMBERED.")
            difference = self.inventory.get_inventory_weight() - self.max_weight
            # Example: self.state_icons.show("encumbered")
            self.health.take_true_damage(0.1 * difference)
        
    def affections(self):
        pass
    
    def withdrawal_effect(self):
        pass

    def needs_effect(self):
        hunger, thirst = self.health.get_hunger(), self.health.get_thirst()
        if hunger <= 0 or thirst <= 0:
            # Example: self.state_icons.show("bleed")
            # Following code is what ever happens as consecuence.
            self.health.take_true_damage(0.1)
            
        liver, stomach = self.health.get_organ("liver"), self.health.get_organ("stomach")
        if hunger >= stomach.MAX_CAPACITY // 2 and thirst >= liver.MAX_CAPACITY // 2 and self.health.true_hp < MAX_TRUE_HP:
            self.health.true_hp += HP_RECOVERY_AMOUNT
        
        if self.health.true_hp >= MAX_TRUE_HP and self.health.get_health() < self.health.get_max_hp_limbs():
            self.health.heal_random_limb(HP_RECOVERY_AMOUNT)
            
    def basic_update(self):
        ### DISPLAY STATUS ICONS HERE!! encumbered, bleeding, etc.
        self.needs_effect()
        self.overcumbered_effect()
        self.radiation_effect()
        
    def organs_update(self):
        if not self.health.organs:
            return
        liver = self.health.get_organ('liver')
        stomach = self.health.get_organ('stomach')
        liver.drain_capacity(ORGAN_DRAIN_AMOUNT)
        stomach.drain_capacity(ORGAN_DRAIN_AMOUNT)
               
    def physical_updates(self):
        self.organs_update()
        self.basic_update()
    
    def reset_equiped_list(self):
        self.equiped_list.clear() 
        for item in self.equiped_items:
            self.equiped_list.append(item)
            print("[HEALTH-EFFECTS] - EQUIPABLE LIST RESET")
            
    def equip_item(self, item):
        for _item in self.equiped_list:
            if item.item_id == _item.item_id:
                return
        self.reset_equiped_list()
        if self.equiped_index >= len(self.equiped_items):
            self.equiped_index = 0
        slot = self.equiped_list[self.equiped_index]
        if item.equipable:
            slot.set_item_to(item.item_id)
            self.equiped_index += 1
            
    def get_gun(self) -> Item:
        """Returns equiped ranged weapon if exist else return False"""
        for item in self.equiped_list:
            if item.item_type == "gun":
                return item
        return False

    def get_melee(self) -> Item:
        """Returns equiped melee weapon if exist else return False"""
        for item in self.equiped_list:
            if item.item_type == "melee":
                return item
            
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
                bleeding_limb = self.health.get_bleeding_limb()
                if bleeding_limb:
                    bleeding_limb.stop_bleed()
                    self.sound_system.play_sound("bandage")
                    print("[HEALTH-EFFECTS] - HEMOSTAT APPLIED.")
                    return
                
            elif item.item_type == "food":
                stomach = self.health.get_organ('stomach')
                print(f"[HEALTH-EFFECTS] - FOOD CONSUMED {item.item_id}")
                satisfy_amount = float(item.amount)
                stomach.fill_capacity(satisfy_amount)
                    
            elif item.item_type == "drink":
                liver = self.health.get_organ('liver')
                print(f"[HEALTH-EFFECTS] - DRINK CONSUMED {item.item_id}")
                satisfy_amount = float(item.amount)
                liver.fill_capacity(satisfy_amount)
                    
            elif item.item_type == "analgesic":
                # Do something
                print(f"[HEALTH-EFFECTS] - CONSUMED ANALGESIC. {item.item_id} {item.amount}")
                
            elif item.item_type == "drug":
                print(f"[HEALTH-EFFECTS] - CONSUMED DRUG {item.item_id}")
                # PLACEHOLDER EFFECT
                
                if item.sub_type == "cigarette" and self.inventory.has_item_type('fire_starter'):
                    self.current_radiation -= item.amount
                    self.sound_system.play_sound("smoke")
                    
                elif item.sub_type == "cigarette" and not self.inventory.has_item_type('fire_starter'):
                    self.inventory.add_to_logger("Wish I a had a lighter...", PURPLE)
                    return False
        return True   
        