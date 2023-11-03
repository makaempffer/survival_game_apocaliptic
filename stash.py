import pygame as pg
from inventory import Inventory
class Stash(pg.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.inventory = Inventory(screen, None)
        self.inventory.is_stash = True
        self.inventory.transfer_mode = True
        self.inventory.setup_stash()
    
    def open_stash(self):
        self.inventory.is_open = not self.inventory.is_open
        print("Stash open", self.inventory.is_open)
        
    def render_update_stash(self):
        self.inventory.render()
        self.inventory.update()