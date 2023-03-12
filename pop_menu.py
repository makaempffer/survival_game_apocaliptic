from settings import *


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
        self.savedLocation = []
        self.previous_action = None
        
    
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
            self.previous_action = selectedAction
            self.selectedAction = None
            if selectedAction == "Walk":
                self.savedLocation = self.startingPoint
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
            text = FONT.render(item, True, (255, 255, 255))
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