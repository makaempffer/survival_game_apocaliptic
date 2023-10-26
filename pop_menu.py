from settings import *


class PopMenu:
    def __init__(self, mapdata, block_manager, npcGroup, screen):
        self.screen = screen
        self.mapData = mapdata
        self.group = block_manager.group
        self.block_manager = block_manager
        self.npcGroup = npcGroup
        self.attacked_entity = None
        self.selected = None
        self.selected_block = None
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
        self.npc_target = None
        self.savedLocation = []
        self.previous_action = None
        self.selected_target = None
        self.open_menu_sound = pg.mixer.Sound('./sounds/Open_menu.wav')
        self.select_sound = pg.mixer.Sound('./sounds/Select.wav')
        self.stepped_block = None
        self.hovered_index = None

    def get_selected_block(self):
        return self.selected_block

    def get_npc_options(self):
        mouse_pos = pg.mouse.get_pos()
        options = []
        detected = False

        for npc in self.npcGroup:
            if npc.rect.collidepoint(mouse_pos):
                self.npc_target = npc
                self.selected_target = npc
                detected = True
                break

        if detected == False:
            self.npc_target = None

        if self.npc_target:
            if self.npc_target.type == "zombie":
                options = ["Melee Atk", "Range Atk"]
            
            if self.npc_target.type == "trader":
                options = ["Quest?", "Sell Trinkets."]

        return options

    def getMenuOptions(self):
        self.open_menu_sound.set_volume(0.02)
        self.open_menu_sound.play()
        mouseX, mouseY = pg.mouse.get_pos()
        self.startingPoint = [mouseX, mouseY]
        options = []
        # print(mouseX//10, mouseY//10)
        for index, block in enumerate(self.mapData):
            if mouseX//BLOCK_SIZE == block[0] and mouseY//BLOCK_SIZE == block[1]:
                self.selected = block[3]
                # TODO Make get_block_index()
                self.selected_block = self.block_manager.blocks[index]
                self.posX, self.posY = mouseX, mouseY
                self.blockIndex = index

        if self.selected == "DIRT":
            options = ["Walk", "Place"]
            self.options = options

        elif self.selected == "TREE":
            options = ["Walk", "Cut Tree", "Inspect"]
            self.options = options

        elif self.selected == "WATER":
            options = ["Drink", "Fill container", "Inspect"]
            self.options = options

        elif self.selected == "SAND":
            options = ["Walk", "Inspect", "Dig"]
            self.options = options
        
        elif self.selected.upper() == "WOOD_TABLE":
            options = ["Craft"]
            self.options = options

        options += self.get_npc_options()

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
            print("[DBG]" + selectedAction)
            return selectedAction
    
    def get_option_by_index(self, index: int):
        return self

    def showMenu(self, options):
        print("SHOWMENU")
        menuWidth = 100
        menuOptHeight = 20
        surfaceMenu = pg.Surface((menuWidth, len(options)*menuOptHeight))
        surfaceMenu.fill((50, 50, 50))
        mouse_pos = pg.mouse.get_pos()

        if abs(self.posX - WIDTH) < menuWidth and self.xCorrection == False:
            self.posX = self.posX - menuWidth
            self.xCorrection = True

        if (HEIGHT - self.posY) < menuOptHeight*len(options) and self.yCorrection == False:
            self.posY -= menuOptHeight*len(options)
            if abs(HEIGHT - self.posY) >= menuOptHeight*len(options):
                self.yCorrection = True

        self.screen.blit(surfaceMenu, (self.posX, self.posY))
        for index, item in enumerate(options):
            
           # print(item)
            rect = pg.Rect(self.posX + 5, self.posY + 2 +
                           (index*menuOptHeight), menuWidth, menuOptHeight)
            self.optionRects.append(rect)
            
            font_color = (255, 255, 255)
            if isinstance(self.hovered_index, int):
                
                if rect.collidepoint(mouse_pos):   
                    if self.hovered_index == index: 
                        print("hovered -> " + str(self.hovered_index))
                        font_color = (255, 0, 0)
            
            
            
        
            text = FONT.render(item, True, font_color)
            
            self.screen.blit(text, rect)
            rect.y -= 6
            rect.width = 48
            pg.draw.line(self.screen, (233, 43, 18), rect.bottomleft, rect.bottomright)
            
    def get_hovered_index(self):
        print("RUNNING HOVER")
        print("RUNNGIN IDNEX", self.hovered_index)
        mouse_pos = pg.mouse.get_pos()
        for index, rect in enumerate(self.optionRects):
            if rect.collidepoint(mouse_pos): 
                    self.hovered_index = index
                    print(index)
                    return index
                
        return None
    
    
            
    def getSelectedOption(self, event):
        mouseX, mouseY = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.opened:
            for index, rect in enumerate(self.optionRects):
                if mouseX >= rect.x and mouseX <= rect.x + 100:  # 100 is menuwidth
                    if mouseY >= rect.y and mouseY <= rect.y + 20:  # 20 is option height
                        self.selectedAction = index
                        self.select_sound.set_volume(0.02)
                        self.select_sound.play()
                        return index
        
    def get_block(self, x, y):
        """Make this faster"""
        for block in self.block_manager.blocks:
            if block.rect.collidepoint((x, y)):
                self.stepped_block = block
                print(f"BLOCK from get block -> {block.type}")
                return block
        
                
    def update(self):
        self.interactionUpdate()
        self.getAction()
        self.get_hovered_index()
