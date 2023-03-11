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
    def __init__(self, mapdata, blockGroup, npcGroup, screen):
        self.screen = screen
        self.mapData = mapdata
        self.group = blockGroup
        self.npcGroup = npcGroup
        self.selected = None
        self.opened = False
        self.interacting = False
        self.options = []
        self.startingPoint = []
        self.posX = 0
        self.posY = 0
        self.xCorrection, self.yCorrection = False, False
        self.optionRects = []
        self.selectedAction = None
        self.blockIndex = None
        self.npcTarget = None
        
    
    def getTargetNpc(self):
        mouseX, mouseY = pg.mouse.get_pos()
        options = []
        detected = False
        
        for index, npc in enumerate(self.npcGroup):
            if mouseX//10 == npc.rect.x//10 and mouseY//10 == npc.rect.y//10:
                self.npcTarget = npc
                detected = True
                break
        if detected == False:
            self.npcTarget = None
        
        if self.npcTarget:
            if self.npcTarget.type == "zombie":
                options = ["Attack", "Identify"]

        return options
        

    def getMenuOptions(self):
        mouseX, mouseY = pg.mouse.get_pos()
        self.startingPoint = [mouseX, mouseY]
        options = []
        #print(mouseX//10, mouseY//10)
        for index, block in enumerate(self.mapData):
            if mouseX//10 == block[0] and mouseY//10 == block[1]:
                self.selected = block[3]
                self.posX, self.posY = mouseX, mouseY
                self.blockIndex = index
            
        for index, npc in enumerate(self.npcGroup):
            if mouseX//10 == npc.rect.x//10 and mouseY//10 == npc.rect.y//10:
                self.npcTarget = npc
                break

        if self.selected == "DIRT":
            options = ["Walk", "Inspect", "Dig"]
            self.options = options
            
        elif self.selected == "TREE":
            options = ["Cut Tree", "Inspect"]
            self.options = options
            
        elif self.selected == "WATER":
            options = ["Drink", "Pour to Container", "Inspect"]
            self.options = options
            
        elif self.selected == "SAND":
            options = ["Walk", "Inspect", "Dig"]
            self.options = options
        
        options += self.getTargetNpc()
        
        return options

    def setupMenu(self):
        if self.opened == False:
            options = self.getMenuOptions()
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
            self.xCorrection = True

        if (HEIGHT - self.posY) < menuOptHeight*len(options) and self.yCorrection == False:
            self.posY -= menuOptHeight*len(options)
            if abs(HEIGHT - self.posY) >= menuOptHeight*len(options):
                self.yCorrection = True
        
        self.screen.blit(surfaceMenu, (self.posX, self.posY))
        for index, item in enumerate(options):
            rect = pg.Rect(self.posX + 5, self.posY + (index*menuOptHeight), menuWidth, menuOptHeight)
            self.optionRects.append(rect)
            text = font.render(item, True, (255, 255, 255))
            x, y = self.posX, self.posY + (index*menuOptHeight)
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


class NPC(pg.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.size = 10
        self.rect = None
        self.path = "./assets/character_player.png"
        self.image = pg.image.load(self.path)
        self.rect = pg.Rect(x * self.size, y * self.size, 10, 10)
        self.type = type
        self.didMove = False
        self.isMoving = False
        self.stopAction = False
        self.recalculate = True
        self.target = []
        self.resetTime = random.randint(500, 3000)
        self.counter = 0
        self.actionCooldown = random.randint(100, 1000)
        self.doAction = True
        self.getType()

    def getType(self):
        if self.type == "zombie":
            self.path = "./assets/zombie.png"
            self.image = pg.image.load(self.path)

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def moveEventFunction(self):
        self.counter += 1
        if self.counter == self.resetTime:
            self.recalculate = True
            self.counter = 0
        
        if self.counter == self.actionCooldown:
            self.doAction = True
        if self.counter != self.actionCooldown:
            self.doAction = False

        

    def update(self):
        self.moveEventFunction()
        if self.doAction:
            self.move()
        
    
    def move(self):
        targetLocation = None
        if self.recalculate == True:
            targetLocation = self.getMoveLocation()
            self.recalculate = False
        else:
            targetLocation = self.target 
        if self.isMoving:
            if targetLocation and self.isMoving:
                distX = (self.rect.x - targetLocation[0])
                distY = (self.rect.y - targetLocation[1])

                if distX > 0:
                    self.setPosition(self.rect.x - 10, self.rect.y)
                if distX < 0:
                    self.setPosition(self.rect.x + 10, self.rect.y)
                if self.rect.x == targetLocation[0] and self.rect.y == targetLocation[1]:
                    targetLocation = None
                    self.isMoving = False

                
                if distY > 0: 
                    self.setPosition(self.rect.x, self.rect.y - 10)
                if distY < 0: 
                    self.setPosition(self.rect.x, self.rect.y + 10)
            
        #neighbors = self.getNeighbors()
        #self.rect.x = neighbors[0]
        #self.getMoveLocation()
        #self.rect.y = neighbors[2]

    def getMoveLocation(self):
        if self.recalculate:
            possibleMovements = []
            
            gridX, gridY = self.rect.x, self.rect.y
            left = [gridX - 0, gridX - 10, gridX - 20, gridX - 30, gridX - 40]
            right = [gridX + 0, gridX + 10, gridX + 20, gridX + 30, gridX + 40]
            up = [gridY - 0, gridY - 10, gridY - 20, gridY - 30, gridY - 40]
            bottom = [gridY + 0, gridY + 10, gridY + 20, gridY + 30, gridY + 40]
            xMoves = [left, right]
            yMoves = [up, bottom]
            xMovement = random.choice(xMoves)
            yMovement = random.choice(yMoves)
            moveChoiceX = random.choice(xMovement)
            moveChoiceY = random.choice(yMovement)
            self.isMoving = True
            self.target = [moveChoiceX, moveChoiceY]
            return [moveChoiceX, moveChoiceY]

    
    def getNeighbors(self):
        left = self.rect.x - 10
        right = self.rect.x + 10
        top = self.rect.y - 10
        bottom = self.rect.y + 10
        return [left, right, top, bottom]
    

    
class NPCManager():
    def __init__(self, screen, width=WIDTH, height=HEIGHT):
        self.npcGroup = pg.sprite.Group()
        self.screen = screen
        self.map = []
        self.sizeX, self.sizeY = width, height
    
    def npcEvent(self):
        self.npcGroup.move()

    def setupNpc(self):
        self.createSpawns()
        self.spawn()

    def spawnNpc(self,x, y,type="zombie"):
        self.npcGroup.add(NPC(x, y, type))

    def render(self):
        self.npcGroup.draw(self.screen)

    def createSpawns(self):
        noise = PerlinNoise(octaves=7, seed=1)
        xpix, ypix = HEIGHT//10, WIDTH//10
        self.rows, self.cols = (self.sizeX//10, self.sizeY//10)
        arr = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
        self.map = arr
        print("[NPC] - NPC MAP CREATED")
    
    def spawn(self):
        if len(self.map) > 1:
            for x, row in enumerate(self.map):
                for y, col in enumerate(row):
                    if self.map[x][y] >= -0.4 and self.map[x][y] <= -0.3:
                        choice = random.randrange(0, 10)
                        if choice > 8:
                            self.spawnNpc(x, y, "zombie") 
            print("[NPC] - NPC SPAWN DONE")



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
        self.data = []
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

class Player(pg.sprite.Sprite):
    def __init__(self, menu):
        super().__init__()
        self.posX = 400
        self.posY = 400
        self.menu = menu
        self.rect = pg.Rect(self.posX, self.posY, 10, 10)
        self.image = pg.image.load("./assets/character_player.png")
        self.lastCommand = ""

    
    def update(self):
        self.movement()
    
    def movement(self):
        
        action = self.menu.getAction()
        if action != None:
            
            self.lastCommand = action
            
        if self.lastCommand:
            print("Action:", action, "Last Command:", self.lastCommand)
            if self.lastCommand == "Walk":
                targetLocation = self.menu.startingPoint
                targetLocation[0] = (targetLocation[0] // 10) * 10
                targetLocation[1] = (targetLocation[1] // 10) * 10
                print("Starting point:", self.menu.startingPoint)
                print(self.rect.x, targetLocation[0], self.rect.y, targetLocation[1])

                

                if self.rect.x == targetLocation[0] and self.rect.y == targetLocation[1]:
                    targetLocation = None
                    self.lastCommand = None
                    return
                if targetLocation:
                    distX = (self.rect.x - targetLocation[0])
                    distY = (self.rect.y - targetLocation[1])

                    
                    if distX > 0:
                        self.rect.x, self.rect.y = self.rect.x - 10, self.rect.y
                        #self.setPosition(self.rect.x - 10, self.rect.y)
                    if distX < 0:
                        self.rect.x, self.rect.y = self.rect.x + 10, self.rect.y
                        #self.setPosition(self.rect.x + 10, self.rect.y)
        
                    if distY > 0: 
                        self.rect.x, self.rect.y = self.rect.x, self.rect.y - 10
                        #self.setPosition(self.rect.x, self.rect.y - 10)
                    if distY < 0: 
                        self.rect.x, self.rect.y = self.rect.x, self.rect.y + 10
                        #self.setPosition(self.rect.x, self.rect.y + 10)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.world = World(WIDTH, HEIGHT)
        self.popMenu = None
        self.blockManager = BlockManager(self.screen, self.world.mapData)
        self.npcManager = NPCManager(self.screen)
        self.isRunning = True
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.playerManager = None
        self.newGame()

    def newGame(self):
        self.popMenu = PopMenu(self.blockManager.mapData, self.blockManager.group, self.npcManager.npcGroup, self.screen)
        self.playerManager = PlayerManager(self.screen, self.popMenu)
        self.npcManager.setupNpc()
        

    def update(self):
        self.playerManager.update()
        self.popMenu.update()
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

