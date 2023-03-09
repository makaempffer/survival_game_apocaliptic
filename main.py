import random
import time
import os
import sys
import pygame as pg
from perlin_noise import PerlinNoise
FPS = 60
WIDTH, HEIGHT = 1000, 600

pg.font.init()
font = pg.font.Font('freesansbold.ttf', 12)



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
            block = Block(self.mapData[x][0], self.mapData[x][1], self.mapData[x][2])
            self.group.add(block)
            self.mapData[x].append(block.type)
        print("[BLOCK-M] - BLOCK GROUP FILLED")

class PopMenu:
    def __init__(self, mapdata, group, screen):
        self.screen = screen
        self.mapData = mapdata
        self.group = group
        self.selected = None
        self.opened = False
        self.interacting = False
        self.options = []
        self.posX = 0
        self.posY = 0
        self.xCorrection, self.yCorrection = False, False
        self.optionRects = []
        self.selectedAction = None
        
        

    def getCurrentBlock(self):
        mouseX, mouseY = pg.mouse.get_pos()
        #print(mouseX//10, mouseY//10)
        for block in self.mapData:
            if mouseX//10 == block[0] and mouseY//10 == block[1]:
                self.selected = block[3]
                self.posX, self.posY = mouseX, mouseY
        if self.selected == "DIRT":
            options = ["Walk", "Inspect", "Dig"]
            self.options = options
            return options
        if self.selected == "TREE":
            options = ["Cut Tree", "Inspect"]
            self.options = options
            return options
        if self.selected == "WATER":
            options = ["Drink", "Pour to Container", "Inspect"]
            self.options = options
            return options
        if self.selected == "SAND":
            options = ["Walk", "Inspect", "Dig"]
            self.options = options
            return options
        
        else:
            return ["None"]

    def setupMenu(self):
        if self.opened == False:
            options = self.getCurrentBlock()
            self.opened = True
            self.interacting = True
        else:
            self.showMenu(options=[])
        
    def interactionUpdate(self):
        if self.interacting == False:
            self.opened = False
        if self.interacting == True:
            self.opened = True
        if self.opened and len(self.options) > 0:
            self.showMenu(self.options)
        if self.opened == False:
            self.xCorrection = False
            self.yCorrection = False
            self.optionRects = []
            
    def getAction(self):
        if self.selectedAction != None:
            selectedAction = self.options[self.selectedAction]
            print(selectedAction)
            self.selectedAction = None
            return selectedAction



    def showMenu(self, options):
        menuWidth = 100
        menuOptHeight = 20
        surfaceMenu = pg.Surface((menuWidth, len(options)*menuOptHeight))
        surfaceMenu.fill((50, 50, 50))

        if abs(self.posX - WIDTH) < menuWidth and self.xCorrection == False:
            self.posX = self.posX - menuWidth
            print(self.posX)
            self.xCorrection = True
            #if abs(WIDTH - self.posX) >= menuWidth:

        if (HEIGHT - self.posY) < menuOptHeight*len(options) and self.yCorrection == False:
            self.posY -= menuOptHeight*len(options)
            if abs(HEIGHT - self.posY) >= menuOptHeight*len(options):
                self.yCorrection = True
        
        self.screen.blit(surfaceMenu, (self.posX, self.posY))
        for index, item in enumerate(options):
            rect = pg.Rect(self.posX, self.posY + (index*menuOptHeight), menuWidth, menuOptHeight)
            self.optionRects.append(rect)
            text = font.render(item, True, (255, 255, 255))
            x, y = self.posX, self.posY + (index*menuOptHeight)
            #surfaceMenu.blit(text, rect)
            self.screen.blit(text, rect)
        
            
    def getSelectedOption(self, event):
        mouseX, mouseY = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.opened:
            for index, rect in enumerate(self.optionRects):
                if mouseX >= rect.x and mouseX <= rect.x + 100: #100 is menuwidth
                    if mouseY >= rect.y and mouseY <= rect.y + 20: #20 is option height
                        self.selectedAction = index
                        return index
                        

    def update(self):
        self.interactionUpdate()
        self.getAction()



class Block(pg.sprite.Sprite):
    def __init__(self, posX, posY, value):
        super().__init__()
        self.posX = posX    
        self.posY = posY
        self.size = 10
        self.rect = pg.Rect(posX * self.size, posY * self.size, 10, 10)
        self.value = value
        self.path = "./assets/tree.png"
        self.image = pg.image.load("./assets/water.png")
        self.type = None
        self.getImage()

    def getImage(self):
        #getting and setting the image for the block according to the perlin value
        if self.value >= 0.4 and self.value <= 1:
            self.path = "./assets/water.png"
            self.type = "WATER"
        if self.value >= 0.3 and self.value <= 0.4: 
            self.path = "./assets/sand.png"
            self.type = "SAND"
        if self.value >= -0.2 and self.value <= 0.3: 
            self.path = "./assets/dirt.png"
            self.type = "DIRT"
        if self.value >= -1 and self.value <= -0.2:
            self.path = "./assets/tree.png"
            self.type = "TREE"

        """
        if self.value <= 0:
            self.type = "./assets/sand.png"
        if self.value <= 0.3 and self.value >= 0:
            self.type = "./assets/dirt.png"
        if self.value <= 0.4 and self.value >= 0.3:
            self.type = "./assets/water.png"
        if self.value >= 0.6 and self.value <= 1:
            self.type = "./assets/tree.png"
        """    

        self.image = pg.image.load(str(self.path))

            


class World:
    def __init__(self, sizeX, sizeY):
        self.map = []
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.createMap()
        self.mapData = []
        self.view()
        self.cols = 0
        self.rows = 0

    def createMap(self):
        noise = PerlinNoise(octaves=7, seed=1)
        xpix, ypix = HEIGHT//10, WIDTH//10
        self.rows, self.cols = (self.sizeX//10, self.sizeY//10)
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
        self.popMenu = None
        self.blockManager = BlockManager(self.screen, self.world.mapData)
        self.isRunning = True
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.newGame()

    def newGame(self):
        self.player = Player()
        self.popMenu = PopMenu(self.blockManager.mapData, self.blockManager.group, self.screen)
        



    def updatePlayerPos(self):
        return
        self.world.map[self.player.posX][self.player.posY] = self.player

    def update(self):
        self.updatePlayerPos()
        self.popMenu.update()
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
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:#right button mousse
                self.popMenu.setupMenu()
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

