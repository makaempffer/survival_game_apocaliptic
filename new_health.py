from settings import *
from organ import Organ
from limb import Limb
import random

class Health:
    '''Npcs don't have organs!, #only call setup organs on player.
    (Might lead to code erros.)'''
    def __init__(self, skills):
        self.true_hp = 100
        self.alive = True
        self.organs = None
        self.skills = skills
        self.limbs = {
            'head': Limb('head', 50),
            'torso': Limb('torso'),
            'arm_right': Limb('arm_right'),
            'arm_left': Limb('arm_left'),
            'leg_right': Limb('leg_right'),
            'leg_left': Limb('leg_left')
        }
        self.limb_probabilities = {
            'head': 10 - self.skills.agility,  # Head is harder to hit with higher agility
            'torso': 20,
            'arm_right': 15,
            'arm_left': 15,
            'leg_right': 20,
            'leg_left': 20,
        }
        
    def take_true_damage(self, damage):
        '''Taking direct damage as radiation, etc.'''
        print("DIRECT DAMAGE TAKEN")
        self.true_hp -= damage
        
    def update_probabilities_by_level(self):
        self.limb_probabilities = {
            'head': 10 - self.skills.agility,  # Head is harder to hit with higher agility
            'torso': 20,
            'arm_right': 15,
            'arm_left': 15,
            'leg_right': 20,
            'leg_left': 20,
            }
        
    def get_bleeding_limb(self):
        for limb in self.limbs.values():
            if limb.bleeding:
                return limb
        print("No bleeding limbs!")
        return False
        
    def setup_organs(self):
        self.organs = {
            'liver': Organ('liver', 60),
            'stomach': Organ('stomach', 60),
            'lungs': Organ('lungs', 80)
            }
    
    def get_organ(self, organ_name):
        if organ_name in self.organs:
            return self.organs[organ_name]
             
    def get_limb(self, limb_name: str):
        if limb_name in self.limbs:
            return self.limbs[limb_name]
        
    def take_damage(self, limb_name: str, damage: float):
        limb = self.get_limb(limb_name)
        limb.take_damage(damage)
        
    def take_damage_on_calculated_limb(self, amount):
        limb = self.calculate_vulnerable_limb()
        limb.take_damage(amount)
        
    def heal_limb(self, limb_name: str, amount: float):
        limb = self.get_limb(limb_name)
        limb.heal(amount)
        
    def update(self):
        for limb in self.limbs.values():
            limb.update()
            
    def check_alive(self) -> bool:
        hp = self.get_health()
        if hp <= 0:
            self.alive = False
            return False
        elif self.get_limb('head').get_hp() <= 0:
            self.alive = False
            return False
        elif self.get_limb('torso').get_hp() <= 0:
            self.alive = False
            return False
        return True 
            
    def get_health(self) -> float:
        '''Returns the sum of all limbs'''
        total_hp = 0
        for limb in self.limbs.values():
            total_hp += limb.current_hp
        return total_hp
    
            
    def calculate_vulnerable_limb(self) -> Limb:
        '''Limb selection gets calculated by the agility
        skill level, the higher agility less likely to be hit in 
        fatal limbs'''
         # Normalize probabilities to add up to 100
        total_probability = sum(self.limb_probabilities.values())
        normalized_probabilities = {limb: prob / total_probability * 100 for limb, prob in self.limb_probabilities.items()}

        # Choose a random limb based on probabilities
        random_value = random.randint(1, 100)
        cumulative_probability = 0

        for limb, probability in normalized_probabilities.items():
            cumulative_probability += probability
            if random_value <= cumulative_probability:
                print(f"LIMB -> {limb}")
                return self.get_limb(limb)

        # Fallback: Return the last limb in case of an issue
        return self.get_limb('leg_left')  # You can choose any limb as a fallback
        
    def get_hunger(self, organ_name='stomach'):
        if not self.organs:
            return
        if organ_name in self.organs:
            return self.organs[organ_name].get_capacity()
        
    def get_thirst(self, organ_name='liver'):
        if not self.organs:
            return
        if organ_name in self.organs:
            return self.organs[organ_name].get_capacity()
        
    def update_organs(self):
        if not self.organs:
            return
        for organ in self.organs.values():
            organ.update()