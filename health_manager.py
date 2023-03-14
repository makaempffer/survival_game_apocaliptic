from settings import *
from functions import *

class HealthManager:
    def __init__(self, screen, combat_system_ref, player_ref):
        self.screen = screen
        self.combat_ref = combat_system_ref
        self.player_ref = player_ref
        self.player_a = None
        self.player_b = None

    def set_players(self):
        active_combat = self.combat_ref.player_active_battle
        if active_combat != None:
            self.player_a, self.player_b = active_combat

    def update(self):
        self.render_player_body(self.player_ref)
        if self.player_a == None or self.player_b == None:
            self.set_players()

    def render_player_body(self, player):
        self.render_player_head(player)
        self.render_player_chest(player)
        self.render_player_arms(player)
        self.render_player_legs(player)
        

    def render_player_head(self, player):
        head_hp = player.health.head
        #pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(25, 25, 10, 10))
        pg.draw.circle(self.screen, (0, mapFromTo(head_hp, 0, 100, 0, 255), 0), (30, 25), 1)
        eye_r = player.health.eye_r
        pg.draw.circle(self.screen, (0, mapFromTo(eye_r, 0, 100, 0, 255), 0), (32, 29), 1)
        eye_l = player.health.eye_l
        pg.draw.circle(self.screen, (0, mapFromTo(eye_l, 0, 100, 0, 255), 0), (28, 29), 1)
        mouth = player.health.mouth
        pg.draw.circle(self.screen, (0, mapFromTo(mouth, 0, 100, 0, 255), 0), (30, 34), 1)

    def render_player_chest(self, player):
        #pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(25, 40, 10, 25))
        chest_hp = player.health.chest
        pg.draw.circle(self.screen, (0, mapFromTo(chest_hp, 0, 100, 0, 255), 0), (30, 45), 1)
        stomach_hp = player.health.stomach
        pg.draw.circle(self.screen, (0, mapFromTo(stomach_hp, 0, 100, 0, 255), 0), (30, 55), 1)

    def render_player_arms(self, player):
        #pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(40, 40, 5, 20))
        arm_r = player.health.arm_r
        bone_arm_r = player.health.bone_arm_r
        hand_r = player.health.hand_r
        fingers_r = player.health.fingers_r
        pg.draw.circle(self.screen, (0, mapFromTo(arm_r, 0, 100, 0, 255), 0), (40, 45), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(bone_arm_r, 0, 100, 0, 255), 0), (40, 50), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(hand_r, 0, 100, 0, 255), 0), (40, 55), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(fingers_r, 0, 100, 0, 255), 0), (40, 60), 1)
        

       #pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(15, 40, 5, 20))
        arm_l = player.health.arm_l
        bone_arm_l = player.health.bone_arm_l
        hand_l = player.health.hand_l
        fingers_l = player.health.fingers_l
        pg.draw.circle(self.screen, (0, mapFromTo(arm_l, 0, 100, 0, 255), 0), (20, 45), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(bone_arm_l, 0, 100, 0, 255), 0), (20, 50), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(hand_l, 0, 100, 0, 255), 0), (20, 55), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(fingers_l, 0, 100, 0, 255), 0), (20, 60), 1)
    
    def render_player_legs(self, player):
        leg_r = player.health.leg_r
        knee_r = player.health.knee_r
        foot_r = player.health.foot_r
        pg.draw.circle(self.screen, (0, mapFromTo(leg_r, 0, 100, 0, 255), 0), (35, 65), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(knee_r, 0, 100, 0, 255), 0), (35, 72.5), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(foot_r, 0, 100, 0, 255), 0), (35, 80), 1)
        
        
        
        leg_l = player.health.leg_l
        knee_l = player.health.knee_l
        foot_l = player.health.foot_l
        pg.draw.circle(self.screen, (0, mapFromTo(leg_l, 0, 100, 0, 255), 0), (25, 65), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(knee_l, 0, 100, 0, 255), 0), (25, 72.5), 1)
        pg.draw.circle(self.screen, (0, mapFromTo(foot_l, 0, 100, 0, 255), 0), (25, 80), 1)