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
from health_manager import HealthManager
from narrator_system import Narrator
         

class Game:
    def __init__(self):
        pg.init()
        self.programIcon = pg.image.load('./assets/character_player.png') 
        pg.display.set_icon(self.programIcon)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.world = World(WIDTH, HEIGHT)
        self.popMenu = None
        self.block_manager = BlockManager(self.screen, self.world.mapData)
        self.npcManager = NPCManager(self.screen)
        self.combat_manager: CombatManager
        self.isRunning = True
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.playerManager = None
        self.newGame()


    def newGame(self):
        self.popMenu = PopMenu(self.block_manager.mapData, self.block_manager, self.npcManager.npcGroup, self.screen)
        self.playerManager = PlayerManager(self.screen, self.popMenu)
        self.combat_manager = CombatManager(self.screen, self.npcManager.npcGroup, self.playerManager.group, self.popMenu)
        self.health_manager = HealthManager(self.screen, self.combat_manager.combat_system, self.playerManager.get_player())
        #self.inventory = Inventory(self.screen)
        self.narrator = Narrator(self.screen)
        self.player =  self.playerManager.get_player()
        self.player.set_narrator(self.narrator)
        self.inventory = self.player.inventory
        self.player.inventory.screen = self.screen
        print("[ENGINE] - VARIABLES CREATED")

    def update(self):
        self.playerManager.update()
        self.popMenu.update()
        self.combat_manager.update()
        self.health_manager.update()
        self.npcManager.npcGroup.update()
        self.block_manager.update_resource_blocks()
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
        self.player.inventory.render()
        self.narrator.show_narrator()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.mixer.quit()
                pg.quit()
                sys.exit()
            self.health_manager.update_health_counters(event)
            self.playerManager.update_player_events(event)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and not self.player.inventory.is_open:#right button mousse
                self.popMenu.setupMenu()
            if event.type == pg.KEYDOWN and event.key ==pg.K_i:
                self.inventory.open()
                print(self.inventory.get_sprites())
                #print(self.inventory.inventory)
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.world.regenerate_map()
                self.block_manager.fill_groups()

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

