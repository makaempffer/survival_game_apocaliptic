import random
import time
import os
import sys
import pygame as pg
from perlin_noise import PerlinNoise
from enum import Enum
FPS = 60
WIDTH, HEIGHT = 600, 600
def mapFromTo(x_input, in_range_start, in_range_start_end, out_range_start, out_range_end):
   y=(x_input - in_range_start) / (in_range_start_end-in_range_start) * (out_range_end-out_range_start) + out_range_start
   return y


class BlockManager:
    def __init__(self, screen, mapData):
        self.group = pg.sprite.Group()
        self.screen = screen
        self.mapData = mapData
        self.coordinatesGroup = []
        self.fillGroup()
        
    def render(self):
        self.group.draw(self.screen)

    def fillGroup(self):
        for x, row in enumerate(self.mapData):
            self.group.add(Block(self.mapData[x][0], self.mapData[x][1], self.mapData[x][2]))
        print("[BLOCK-M] - BLOCK GROUP FILLED")




class Block(pg.sprite.Sprite):
    def __init__(self, posX, posY, value):
        super().__init__()
        self.posX = posX    
        self.posY = posY
        self.rect = pg.Rect(posX * 10, posY * 10, 10, 10)
        self.value = value
        self.type = "./assets/dirt.png"
        self.image = pg.image.load("./assets/dirt.png")
        self.getImage()

    def getImage(self):
        if self.value <= 0.2:
            self.type = "./assets/sand.png"
        elif self.value <= 0.4:
            self.type = "./assets/water.png"
        elif self.value <= 0.6:
            self.type = "./assets/water.png"
        elif self.value <= 1:
            self.type = "./assets/tree.png"
        self.image = pg.image.load(str(self.type))

            


class World:
    def __init__(self, sizeX, sizeY):
        self.map = []
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.createMap()
        self.mapData = []
        self.view()

    def createMap(self):
        noise = PerlinNoise(octaves=10, seed=1)
        xpix, ypix = WIDTH//10, HEIGHT//10
        rows, cols = (self.sizeX//10, self.sizeY//10)
        arr = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
        self.map = arr
    
    def view(self):
        if len(self.map) > 1:
            for x, row in enumerate(self.map):
                for y, col in enumerate(row):
                    #color = mapFromTo(self.map[x][y], -1, 1, 0, 255)
                    self.mapData.append([x, y, self.map[x][y]])
            print("[WORLD] - WORLD MAP DATA DONE")

            

        

class Player:
    def __init__(self):
        self.hp = 10
        self.posX = random.randint(0, WIDTH//10)
        self.posY = random.randint(0, HEIGHT//10)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.world = World(WIDTH, HEIGHT)
        self.player = None
        self.blockManager = BlockManager(self.screen, self.world.mapData)
        self.isRunning = True
        self.clock = pg.time.Clock()
        self.delta_time = 1

    def newGame(self):
        self.player = Player()



    def updatePlayerPos(self):
        return
        self.world.map[self.player.posX][self.player.posY] = self.player

    def update(self):
        self.updatePlayerPos()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.blockManager.render()

        

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while self.isRunning:
            self.check_events()
            self.update()
            self.draw()

    
game = Game()
game.run()

