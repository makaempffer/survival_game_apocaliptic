import sys
import pygame as pg
from settings import *
from functions import *
from world import World
from menu import PopMenu
from npc_manager import NPCManager
from block_manager import BlockManager
from player_manager import PlayerManager
from narrator_system import Narrator
from director import Director

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # SIZE CAN BE CORRECTED BY SUBSTRACTING 16 TO WIDTH, UI HAS TO BE MOVED.
        self.world = World(WIDTH, HEIGHT)
        self.popMenu = None
        self.block_manager = BlockManager(self.screen, self.world.mapData)
        self.npcManager = NPCManager(self.screen)
        self.isRunning = True
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.counter = 0
        self.max_ticks = 100
        self.playerManager = None
        self.newGame()
    
    def timed_updates(self):
        self.counter += 1
        if self.counter >= self.max_ticks:
            """Functions to call on tick cooldown."""
            self.block_manager.update_click_for_stash()
            self.counter = 0

    def newGame(self):
        self.popMenu = PopMenu(self.block_manager.mapData, self.block_manager, self.npcManager.npc_group, self.screen)
        self.playerManager = PlayerManager(self.screen, self.popMenu)
        self.narrator = Narrator(self.screen)
        self.player =  self.playerManager.get_player()
        self.player.set_narrator(self.narrator)
        self.inventory = self.player.inventory
        self.player.inventory.screen = self.screen
        self.director = Director(npc_manager=self.npcManager, block_manager=self.block_manager)
        print("[ENGINE] - VARIABLES CREATED")

    def update(self):
        self.director.update()
        self.playerManager.update(self.delta_time)
        self.popMenu.update()
        self.npcManager.update(self.delta_time, self.player)
        self.block_manager.update_resource_blocks()
        self.timed_updates()
        self.narrator.update()
        self.player.inventory.update()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.block_manager.render()
        self.playerManager.render()
        self.npcManager.render()
        self.player.render_player_related()
        self.player.inventory.render()
        self.director.render_clock()

     
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.mixer.quit()
                pg.quit()
                sys.exit()

            self.playerManager.update_player_events(event)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:#right button mousse
                self.popMenu.setupMenu()

            if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
                self.inventory.open()
            
            if event.type == pg.KEYDOWN and event.key == pg.K_l:
                self.player.user_interface.show = not self.player.user_interface.show

            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.world.regenerate_map()
                self.block_manager.generate_map()
                
            # MENU STUFF
            self.popMenu.getSelectedOption(event)
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:#left mouse button
                self.popMenu.interacting = False
        
        
    def run(self):
        while self.isRunning:
            self.check_events()
            self.update()
            self.draw()

    
game = Game()
game.run()

