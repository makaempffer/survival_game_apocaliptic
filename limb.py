from random import random
from settings import BLEEDING_DAMAGE
class Limb:
    def __init__(self, limb_name, max_hp = 100):
        self.limb_name = limb_name
        self.MAX_HP = max_hp
        self.current_hp = self.MAX_HP
        self.bleeding = False
        self.broken = False
        
    def heal(self, amount):
        if self.current_hp <= 0:
            print("[LIMB] Cant heal dead limbs")
            return
        self.current_hp += amount
        
    def take_damage(self, amount):
        self.current_hp -= amount
        
    def stop_bleed(self):
        if self.bleeding:
            self.bleeding = False
    
    def start_bleed(self):
        if self.bleeding == False:
            self.bleeding = True
            
    def roll_bleed_chance(self, probabilty: float = 25):
        if self.bleeding: return
        probabilty = probabilty / 100
        roll = random()
        if roll < probabilty:
            self.start_bleed()
            return True
        else:
            return False
        
            
    def break_bone(self):
        self.broken = True
        
    def heal_bone(self):
        self.broken = False
        
    def get_hp(self):
        return self.current_hp
    
    def bleeding_status(self):
        if self.bleeding:
            #print(self.limb_name, self.bleeding)
            self.take_damage(BLEEDING_DAMAGE)
    
    def update(self):
        self.bleeding_status()
