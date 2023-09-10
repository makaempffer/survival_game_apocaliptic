import pygame as pg
from settings import *

class Narrator:
    def __init__(self, screen):
        self.screen = screen
        self.position = pg.Vector2(5, HEIGHT-NARRATOR_HEIGHT-5)
        self.message = ""
        self.message_stack = []
        self.color = (255, 255, 255)
        self.show = True
        self.append_message("Hello the world.")
        
    def append_message(self, message):
        self.message_stack.append(message)
        self.set_message()

    def pop_message(self) -> str:
        return self.message_stack.pop()
    
    def set_message(self):
        self.message = self.pop_message()

    def show_narrator(self):
        if not self.show:
            return
        surface = pg.Surface((NARRATOR_WIDTH, NARRATOR_HEIGHT))
        surface.fill((50, 80, 40))
        
        self.screen.blit(surface, self.position)
        text = FONT.render(self.message, True, self.color)
        self.screen.blit(text, self.position)

    def update(self):
        pass
        
