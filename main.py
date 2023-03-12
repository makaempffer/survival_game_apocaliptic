import sys
import pygame as pg

from settings import *
from functions import *
from world import World
from pop_menu import PopMenu
from npc_manager import NPCManager
from block_manager import BlockManager
from player_manager import PlayerManager
from combat_manager import CombatManager
         

class Game:
    def __init__(self):
        pg.init()
        self.programIcon = pg.image.load('./assets/character_player.png') 
        pg.display.set_icon(self.programIcon)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.world = World(WIDTH, HEIGHT)
        self.popMenu = None
        self.blockManager = BlockManager(self.screen, self.world.mapData)
        self.npcManager = NPCManager(self.screen)
        self.combat_manager: CombatManager
        self.isRunning = True
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.playerManager = None
        self.newGame()


    def newGame(self):
        self.popMenu = PopMenu(self.blockManager.mapData, self.blockManager.group, self.npcManager.npcGroup, self.screen)
        self.playerManager = PlayerManager(self.screen, self.popMenu)
        self.npcManager.setupNpc()
        self.combat_manager = CombatManager(self.screen, self.npcManager.npcGroup, self.playerManager.group, self.popMenu)
        
    def update(self):
        self.playerManager.update()
        self.popMenu.update()
        self.combat_manager.update()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()      


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.blockManager.render()
        self.playerManager.render()
        self.npcManager.render()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:#right button mousse
                self.popMenu.setupMenu()
            self.popMenu.getSelectedOption(event)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:#left mouse button
                self.popMenu.interacting = False
        self.npcManager.npcGroup.update()
            

    def run(self):
        while self.isRunning:
            self.check_events()
            self.update()
            self.draw()

    
game = Game()
game.run()

