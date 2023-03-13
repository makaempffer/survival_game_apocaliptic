from settings import *

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
        self.render_player_body()
        if self.player_a == None or self.player_b == None:
            self.set_players()

    def render_player_body(self):
        self.render_player_head()
        

    def render_player_head(self):
        head_hp = self.player_ref.health.head
        pg.draw.rect(self.screen, (head_hp, head_hp, head_hp), pg.Rect(25, 25, 30, 30))
        