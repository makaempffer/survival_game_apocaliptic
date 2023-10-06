from settings import *
from functions import calculate_damage, apply_resistance
from random import randint



# TODO ADD MODIFIERS ON LIMB HEALTH: EX -> arm_r 
# How do I get the gun? 
# The equiped gun is stored in: HealthEffects - equiped_list
# IDEA: Make a function that returns the first gun in the list
class Combat:
    def __init__(self, user):
        self.user = user
        self.attacker = None
        
    def get_attacked_entity(self):
        target = self.user.menu.npc_target
        if not target:
            return
        
        command = self.user.lastCommand
        print("COMMAND", command)
        if command:
            command = command.lower()
            
            if command == "range atk":
                self.attack_distance(target_user=target)
            
            elif command == "melee atk":
                self.attack_melee(target_user=target)
                            
    def player_combat_logic(self):
        self.get_attacked_entity()

    def set_attacker_to_target(self, user_target):
        user_target.attacker = self
        
    def attack_distance(self, target_user):
        gun = self.user.health_effects.get_gun()
        if not gun:
            print("User has no gun")
            return

        if target_user:
            gun_range = gun.range * BLOCK_SIZE # Multiplied to match pixel units
            distance = self.user.position.distance_to(target_user.position)
            if distance > gun_range:
                print("Target too far, gun range too short")
                return
            attack_success = self.hit_chance()
            if attack_success:
                damage = self.calculate_damage_distance(gun.damage)
                target_user.combat.receive_distance_damage(damage)
    
    def attack_melee(self, target_user):
        if target_user:
            distance = self.user.position.distance_to(target_user.position)
            if distance <= self.user.interaction_reach:
                print("can melee hit")
                attack_success = self.hit_chance()
                if attack_success:
                    damage = self.calculate_damage_melee()
                    target_user.combat.receive_melee_damage(damage)
                
    def receive_distance_damage(self, damage):
        """Calculates the damage acording to the user armor"""
        armor_rating = self.user.health_effects.get_armor_rating()
        damage_after_res = apply_resistance(damage, armor_rating, RESISTANCE_FACTOR)
        self.user.health.receive_damage(damage_after_res)
        
    def receive_melee_damage(self, damage):
        armor_rating = self.user.health_effects.get_armor_rating() + self.user.skills.strength
        damage_after_res = apply_resistance(damage, armor_rating, RESISTANCE_FACTOR)
        self.user.health.receive_damage(damage_after_res)
        print("Received melee damage.")
        
    def calculate_damage_distance(self, weapon_damage) -> float:
        accuracy = self.user.skills.accuracy
        damage = calculate_damage(weapon_damage, accuracy, WEAPON_DAMAGE_FACTOR)
        return damage
        
    def calculate_damage_melee(self) -> float:
        strength_level = self.user.skills.strength
        damage = calculate_damage(5, strength_level, SKILLS_FACTOR)
        return damage
    
    def hit_chance(self):
        accuracy_level = self.user.skills.accuracy
        random_roll = randint(0, 10)
        if random_roll <= accuracy_level:
            print("[COMBAT-NEW] - HIT CHANCE SUCCESS.")
            return True
        else:
            print("[COMBAT-NEW] - ATTACK MISSED.")
            return False
    
        
        
    
    