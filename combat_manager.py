from combat_system import CombatSystem
from settings import *
class CombatManager:
    def __init__(self, screen, npc_group: pg.sprite.Group, 
                player_group: pg.sprite.Group, 
                combatSystem: CombatSystem = CombatSystem):
        self.screen = screen
        self.combat_system = combatSystem
        self.npc_group = npc_group
        self.player_group = player_group

    def get_player_vs_npc(self, player= None):
        player_ref = player
        for player in self.player_group:
            player_ref = player
            player_x = player.rect.x
            player_y = player.rect.y
        for npc in self.npc_group:
            npc_x, npc_y = npc.rect.x, npc.rect.y
            dist_x = abs(player_x - npc_x)
            dist_y = abs(player_y - npc_y)
            avg_dist = (dist_x + dist_y) / 2

            if avg_dist < player_ref.vision_distance:
                pg.draw.rect(self.screen, (20, 230, 20), npc.rect)
                print(avg_dist)
                print(dist_x)
                print(dist_y)
    
    def update(self):
        self.get_player_vs_npc()