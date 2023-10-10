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
        self.show_hp = False
        self.target = None
        
    
    def loot_body(self, target):
        self.user.inventory.add_item_list(target.inventory.inventory)
        
    def return_attack(self):
        if self.attacker:
            if self.attack_distance(self.attacker):
                return
            else:
                self.attack_melee(self.attacker)
            
        
    def attack_objective(self):
        target = self.user.menu.npc_target
        self.target = target
        
        if not target:
            return
        
        if not target.health.check_alive():
            self.loot_body(target)
            self.target = None
            self.user.menu.npc_target = None
            
        command = self.user.lastCommand
        if command:
            command = command.lower()
            if command == "range atk":
                self.attack_distance(target_user=target)
                self.show_hp = True
                self.target = target
                target.combat.return_attack()
            
            elif command == "melee atk":
                self.attack_melee(target_user=target)
                self.show_hp = True
                self.target = target
                target.combat.return_attack()
            
    def render_enemy_hp(self):
        if self.target and self.show_hp:
            self.target.show_health_bar(self.user.inventory.screen)
                            
    def player_combat_logic(self):
        self.attack_objective()    

    def attack_distance(self, target_user):
        gun = self.user.health_effects.get_gun()
        if not gun:
            print("User has no gun")
            return False
        
        
        if not self.user.inventory.get_ammo_by_caliber(gun.caliber):
            if self.user.sound_system:
                self.user.sound_system.play_sound("pistol_pack")
                print("NO AMMO")
                return
        if self.user.sound_system:   
            self.user.sound_system.play_sound(gun.item_id)
        self.user.inventory.consume_ammo(gun.caliber)
            
        if target_user:
            gun_range = gun.range * BLOCK_SIZE # Multiplied to match pixel units
            distance = self.user.position.distance_to(target_user.position)
            print(f"[COMBAT - TARGET DISTANCE {distance} {self.user.position} / {target_user.position}")
            if distance > gun_range:
                print("Target too far, gun range too short")
                return False
            attack_success = self.hit_chance()
            if attack_success:
                damage = self.calculate_damage_distance(gun.damage)
                target_user.combat.receive_distance_damage(damage)
                # Giving a reference to the attacker
                target_user.combat.attacker = self.user
                return True
    
    def attack_melee(self, target_user):
        if target_user:
            distance = self.user.position.distance_to(target_user.position)
            if distance <= self.user.interaction_reach:
                print("can melee hit")
                attack_success = self.hit_chance()
                if attack_success:
                    damage = self.calculate_damage_melee()
                    target_user.combat.receive_melee_damage(damage)
                    # Giving a reference to the attacker
                    target_user.combat.attacker = self.user
                    
            else:
                print("Target is too far to melee hit.")
                
    def receive_distance_damage(self, damage):
        """Calculates the damage acording to the user armor"""
        armor_rating = self.user.health_effects.get_armor_rating()
        damage_after_res = apply_resistance(damage, armor_rating, RESISTANCE_FACTOR)
        print(f"[COMBAT] - DAMAGE RECEIVED {damage_after_res} HP: {self.user.health.get_health()}")
        self.user.health.take_damage_on_calculated_limb(damage_after_res)
        
    def receive_melee_damage(self, damage):
        armor_rating = self.user.health_effects.get_armor_rating() + self.user.skills.strength * 2
        damage_after_res = apply_resistance(damage, armor_rating, RESISTANCE_FACTOR)
        self.user.health.take_damage_on_calculated_limb(damage_after_res)
        print(f"[COMBAT] - DAMAGE RECEIVED {damage_after_res} HP: {self.user.health.get_health()}.")
        
    def calculate_damage_distance(self, weapon_damage) -> float:
        random_number = randint(0, 3)
        accuracy = self.user.skills.accuracy
        damage = calculate_damage(weapon_damage + random_number, accuracy, WEAPON_DAMAGE_FACTOR)
        return damage
        
    def calculate_damage_melee(self) -> float:
        random_number = randint(0, 3)
        strength_level = self.user.skills.strength
        damage = calculate_damage(5 + random_number, strength_level, SKILLS_FACTOR)
        return damage
    
    def hit_chance(self):
        accuracy_level = self.user.skills.accuracy + self.user.skills.perception
        random_roll = randint(0, 10)
        if random_roll <= accuracy_level:
            print("[COMBAT-NEW] - HIT SUCCEED.")
            return True
        else:
            print("[COMBAT-NEW] - ATTACK MISSED.")
            return False
    
        
        
    
    