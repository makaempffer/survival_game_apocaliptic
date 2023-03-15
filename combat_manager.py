from combat_system import CombatSystem
from settings import *
from pop_menu import PopMenu
from math import sqrt
class CombatManager:
    def __init__(self, screen, npc_group: pg.sprite.Group, 
                player_group: pg.sprite.Group, 
                menu: PopMenu,
                combatSystem: CombatSystem = CombatSystem):
        self.menu = menu
        self.screen = screen
        self.combat_system = CombatSystem()
        self.npc_group = npc_group
        self.player_group = player_group
        self.closest_ref = None
        self.closest_possible = 10000
        self.player_ref = None
        

    def get_player_ref(self, player = None):
        if self.player_ref == None:
            for player in self.player_group:
                self.player_ref = player
                return player



    def create_battle(self, a, b):
        self.combat_system.create_battle_instance(a, b)

    def run_battle(self):
        current_combat = self.combat_system.player_active_battle
        if current_combat != None:
            current_combat[0].health.give_damage(current_combat[1].health)
            self.combat_system.end_combat()
            current_combat[1].health.give_damage(current_combat[0].health)
            print(current_combat[0].health.body_avg)
            print("Player damage:",current_combat[0].health.calculate_damage())
            print("Npc damage:",current_combat[1].health.calculate_damage())
            self.combat_system.end_combat()
        
            

        
### FIX SAVING THE CLOSEST TARGET TO THE PLAYER AS TARGET, NOT THE SELECTED
    def player_create_instance(self):
        npc_objective = self.menu.selected_target
        if npc_objective != None:
            action = self.menu.previous_action
            player_to_npc_dist_x = (npc_objective.rect.x - self.player_ref.rect.x)**2
            player_to_npc_dist_y = (npc_objective.rect.y - self.player_ref.rect.y)**2
            dist = sqrt(player_to_npc_dist_x + player_to_npc_dist_y)

            if action == "Attack" and self.combat_system.player_active_battle == None and dist < self.player_ref.vision_distance and self.player_ref.health.is_alive:
                self.create_battle(self.player_ref, npc_objective)
                self.player_ref.combat_triggered = True
                npc_objective.combat_triggered = True
                print("[COMBAT-M] - COMBAT CREATED")
            else:
                self.menu.previous_action = None

    def update(self):
        self.get_player_ref()
        self.player_create_instance()
        self.run_battle()