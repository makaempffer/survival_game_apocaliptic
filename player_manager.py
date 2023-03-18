from settings import *
from player import Player
class PlayerManager:
    def __init__(self, screen, menu):
        self.group = pg.sprite.Group()
        self.screen = screen
        self.menu = menu
        self.createPlayer()
        self.player = self.get_player()
    
    def createPlayer(self):
        player = Player(self.menu)
        self.group.add(player)
    
    def update(self):
        self.group.update()

    def get_player(self):
        for player in self.group : return player
    
    def update_player_events(self, event):
        if self.player:
            self.player.timer_event(event)

    def render(self):
        self.group.draw(self.screen)