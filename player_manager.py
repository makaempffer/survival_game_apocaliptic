from settings import *
from player import Player
class PlayerManager:
    def __init__(self, screen, menu):
        self.group = pg.sprite.Group()
        self.screen = screen
        self.menu = menu
        self.createPlayer()
    
    def createPlayer(self):
        player = Player(self.menu)
        self.group.add(player)
    
    def update(self):
        self.group.update()

    def render(self):
        self.group.draw(self.screen)