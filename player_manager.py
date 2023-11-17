from settings import *
from player import Player
import pygame as pg
class PlayerManager:
    def __init__(self, screen, menu):
        self.group = pg.sprite.Group()
        self.screen = screen
        self.menu = menu
        self.createPlayer()
        self.player = self.get_player()
    
    def createPlayer(self):
        player = Player(self.menu, self.screen)
        self.group.add(player)
    
    def update(self, delta_time):
        self.group.update(delta_time)

    def get_player(self) -> Player:
        for player in self.group : return player
    
    def update_player_events(self, event):
        if self.player:
            self.player.timer_event(event)

    def render(self):
        self.group.draw(self.screen)