from settings import *

class CombatSystem:
    def __init__(self):
        
        self.player_active_battle = None

    def create_battle_instance(self, player_a, player_b):
        self.player_active_battle = [player_a, player_b]
        
    
    def stop_movement(self):
        if self.player_active_battle != None:
            player_a = self.player_active_battle[0]
            player_b = self.player_active_battle[1]
            player_a.doAction = False
            player_b.doAction = False
            
    def getPosibleInstances(self):
        pass

    






