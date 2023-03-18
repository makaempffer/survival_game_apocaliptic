from settings import *
from functions import *

class HealthManager:
    def __init__(self, screen, combat_system_ref, player_ref):
        self.screen = screen
        self.combat_ref = combat_system_ref
        self.player_ref = player_ref
        self.player_a = None
        self.player_b = None
        
    def is_combat_active(self) -> bool:
        """Return True if there is a battle happening."""
        active_combat = self.combat_ref.player_active_battle
        if active_combat != None:
            return True
        else:
            return False
        
    def set_players(self):
        active_combat = self.combat_ref.player_active_battle
        
        if self.is_combat_active():
            self.player_a, self.player_b = active_combat

    def update_health_counters(self, event):
        if self.is_combat_active():
            self.player_a.health.timer_event(event)
            self.player_b.health.timer_event(event)

    def update(self):
        self.render_player_body(self.player_ref)
        if self.player_a == None or self.player_b == None:
            self.set_players()
        if self.player_b:
            self.render_player_body(self.player_b, "Npc")
        
            if self.player_b.health.is_alive == False:
                self.player_b = None


    def render_player_body(self, player, type: str = "Player"):
        self.render_player_head(player, type)
        self.render_player_chest(player, type)
        self.render_player_arms(player, type)
        self.render_player_legs(player, type)
        
    def get_hp_color(self, hp: float, hp_max: int = 100):
        
        if hp > 70:
            return GREEN
        if hp <= 70 and hp > 30:
            return YELLOW
        if hp <= 30:
            return RED

    def render_player_head(self, player, type: str = "Player"):
        offset = 0
        if type == "Npc":
            offset = 100
        head_hp = player.health.head
        #pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(25, 25, 10, 10))
        pg.draw.circle(self.screen, self.get_hp_color(head_hp), (30 + offset, 25), 1)
        eye_r = player.health.eye_r
        pg.draw.circle(self.screen, self.get_hp_color(eye_r), (32 + offset, 29), 1)
        eye_l = player.health.eye_l
        pg.draw.circle(self.screen, self.get_hp_color(eye_l), (28 + offset, 29), 1)
        mouth = player.health.mouth
        pg.draw.circle(self.screen, self.get_hp_color(mouth), (30 + offset, 34), 1)


    def render_player_chest(self, player, type: str = "Player"):
        #pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(25, 40, 10, 25))
        offset = 0
        if type == "Npc":
            offset = 100
        chest_hp = player.health.chest
        pg.draw.circle(self.screen, self.get_hp_color(chest_hp), (30 + offset, 45), 1)
        stomach_hp = player.health.stomach
        pg.draw.circle(self.screen, self.get_hp_color(stomach_hp), (30 + offset, 55), 1)

    def render_player_arms(self, player, type: str = "Player"):
        #pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(40, 40, 5, 20))
        offset = 0
        if type == "Npc":
            offset = 100
        arm_r = player.health.arm_r
        bone_arm_r = player.health.bone_arm_r
        hand_r = player.health.hand_r
        fingers_r = player.health.fingers_r
        pg.draw.circle(self.screen, self.get_hp_color(arm_r), (40 + offset, 45), 1)
        pg.draw.circle(self.screen, self.get_hp_color(bone_arm_r), (40 + offset, 50), 1)
        pg.draw.circle(self.screen, self.get_hp_color(hand_r), (40 + offset, 55), 1)
        pg.draw.circle(self.screen, self.get_hp_color(fingers_r), (40 + offset, 60), 1)
        

       #pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(15, 40, 5, 20))
        arm_l = player.health.arm_l
        bone_arm_l = player.health.bone_arm_l
        hand_l = player.health.hand_l
        fingers_l = player.health.fingers_l
        pg.draw.circle(self.screen, self.get_hp_color(arm_l), (20 + offset, 45), 1)
        pg.draw.circle(self.screen, self.get_hp_color(bone_arm_l), (20 + offset, 50), 1)
        pg.draw.circle(self.screen, self.get_hp_color(hand_l), (20 + offset, 55), 1)
        pg.draw.circle(self.screen, self.get_hp_color(fingers_l), (20 + offset, 60), 1)
    
    def render_player_legs(self, player, type: str = "Player"):
        offset = 0
        if type == "Npc":
            offset = 100
        leg_r = player.health.leg_r
        knee_r = player.health.knee_r
        foot_r = player.health.foot_r
        pg.draw.circle(self.screen, self.get_hp_color(leg_r), (35 + offset, 65), 1)
        pg.draw.circle(self.screen, self.get_hp_color(knee_r), (35 + offset, 72.5), 1)
        pg.draw.circle(self.screen, self.get_hp_color(foot_r), (35 + offset, 80), 1)
        
        
        
        leg_l = player.health.leg_l
        knee_l = player.health.knee_l
        foot_l = player.health.foot_l
        pg.draw.circle(self.screen, self.get_hp_color(leg_l), (25 + offset, 65), 1)
        pg.draw.circle(self.screen, self.get_hp_color(knee_l), (25 + offset, 72.5), 1)
        pg.draw.circle(self.screen, self.get_hp_color(foot_l), (25 + offset, 80), 1)