from settings import *

class CombatSystem:
    def __init__(self):
        self.player_active_battle = None

    def create_battle_instance(self, player_a, player_b):
        if player_a.health.is_alive and player_b.health.is_alive:
            self.player_active_battle = [player_a, player_b]
            print("[COMBAT-S] - CURRENT BATTLE :", self.player_active_battle)
        else:
            return False
        
    def end_combat(self):
        if self.player_active_battle != None:
            player_a, player_b = self.player_active_battle
            if player_a.health.get_total_hp() <= 0:
                player_b.combat_triggered = False
                self.player_active_battle = None
                print("[COMBAT-S] - COMBAT ENDED")

            if player_b.health.get_total_hp() <= 0:
                player_a.combat_triggered = False
                self.player_active_battle = None
                print("[COMBAT-S] - COMBAT ENDED")

                
           

    def stop_movement(self):
        if self.player_active_battle != None:
            player_a = self.player_active_battle[0]
            player_b = self.player_active_battle[1]
            player_a.doAction = False
            player_b.doAction = False
            
    def getPosibleInstances(self):
        pass

    






