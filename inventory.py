from settings import *
import pygame as pg

class Item(pg.sprite.Sprite):
    def __init__(self, x=0, y=0, item_id: str = "EMPTY"):
        super().__init__()
        self.item_id = item_id
        self.size = 32
        self.rect = pg.Rect(x, y, 32, 32)
        self.image = None
        self.item_quantity: int = 1
        self.is_stackable = False
        self.get_item_sprite()

    def update(self, screen):
        self.font_set_quantity(screen)

    def font_set_quantity(self, screen):
        rect = pg.Rect(self.rect.x, self.rect.y, 32, 32)
        text = FONT.render(str(self.item_quantity), True, (255, 255, 255))
        screen.blit(text, rect)

    def get_item_sprite(self):
        if pg.get_init():
            if self.item_id == "EMPTY":
                self.image = pg.image.load(
                    "./assets/item_frame.png").convert_alpha()
            if self.item_id == "MONEY":
                self.is_stackable = True
                self.image = pg.image.load("./assets/money.png").convert_alpha()
            if self.item_id == "BANDAGE":
                self.is_stackable = True
                self.image = pg.image.load("./assets/bandage.png").convert_alpha()


class Inventory:
    def __init__(self, screen=None) -> None:
        self.rows = 5
        self.columns = 5
        self.item_size = 32
        self.x_start = WIDTH - self.item_size * self.rows
        self.y_start = HEIGHT - self.item_size * self.columns
        self.item_frame_group = pg.sprite.Group()
        self.item_group = pg.sprite.Group()
        self.screen = screen
        self.inventory = None
        self.is_open = False
        self.create_item_frame_group()
        self.create_inventory()
        
        self.insert_item(0, 0, Item(self.x_start + 2*32,
                         self.y_start + 2*32, "BANDAGE"))
        self.insert_item(0, 0, Item(self.x_start + 3*32,
                         self.y_start + 3*32, "MONEY"))
        """
        self.insert_item(3, 3, Item(self.x_start + 3*32,
                         self.y_start + 3*32, "MONEY"))
        """
        # self.update_item_group()

    def add_item_list(self, inventory_list):
        slot_x, slot_y = None, None
        for x, row in enumerate(inventory_list):
            for y, item in enumerate(row):
                if item == None and slot_x == None and slot_y == None:
                    slot_x, slot_y = x, y
                if item != None and item.item_id == self.inventory[x][y].item_id:
                    self.inventory[x][y].item_quantity += item.item_quantity
                    continue
                if item != None and self.inventory[x][y] == None:
                    print("[INV] - ITEM ADDED ->", item.item_id)
                    #self.insert_item(0, 0, item)
                self.inventory[slot_x][slot_y] = item

    def create_item_frame_inventory(self):
        return [[Item(self.x_start + j*32, self.y_start + i*32) for j in range(self.rows)] for i in range(self.columns)]

    def create_item_frame_group(self):
        frames = self.create_item_frame_inventory()
        if len(self.item_frame_group) == 0:
            for row in frames:
                for item in row:
                    self.item_frame_group.add(item)

    def get_sprites(self):
        print("Getting sprites")
        item_list = []
        for x, row in enumerate(self.inventory):
            for y, item in enumerate(row): 
                if item != None:
                    item_list.append(item)
        return item_list

    def update_sprites_positions(self):
        for x, row in enumerate(self.inventory):
            for y, item in enumerate(row):
                if isinstance(item, Item):
                    item.rect.x = self.x_start + x * 32
                    item.rect.y = self.y_start + y * 32

    def create_inventory(self):
        self.inventory = [[None for j in range(
            self.rows)] for i in range(self.columns)]

    def get_inv(self):
        return self.inventory

    def insert_item(self, pos_x=0, pos_y=0, item: Item=Item()):
        if self.inventory[pos_x][pos_y] == None:
            self.inventory[pos_x][pos_y] = item
            print("[INV] - ITEM INSERTED")
        else:
            for row in self.inventory:
                for slot in row:
                    if slot != None:
                        if slot.item_id == item.item_id:
                            print(slot.item_id,"=",item.item_id)
                            slot.item_quantity += item.item_quantity
                            print("[INV] - ITEM FOUND -> {", slot.item_id, "} -> QUANTITY:", slot.item_quantity)
                            return
                        
            for x, row in enumerate(self.inventory):
                for y, slot in enumerate(row):
                    if slot == None:
                        print("[INV] - FILLED CLOSEST EMPTY SLOT")
                        item.rect.x = self.x_start + x * 32
                        item.rect.y = self.y_start + y * 32
                        #slot = item
                        self.inventory[x][y] = item
                        return

            print("[INV] - NO SLOTS AVAILABLE")

    def get_item(self) -> Item:
        mouse_x, mouse_y = pg.mouse.get_pos()
        for row in self.inventory:
            for item in row:
                if item != None:
                    if mouse_x >= item.rect.x and mouse_x <= item.rect.x + 32:
                        if mouse_y >= item.rect.y and mouse_y <= item.rect.y + 32:
                            return item

    def update(self):
        self.update_item_group()
        self.update_sprites_positions()
        #print(self.get_item())

    def open(self):
        if self.is_open:
            self.is_open = False
        else:
            self.is_open = True

    def update_item_group(self):
        for row in self.inventory:
                for item in row:
                    if item != None and not self.item_group.has(item):
                        self.item_group.add(item)
                        print("[INV] - ITEM: {", item.item_id, "} APPENDED")
        """    
        if len(self.inventory) > 0:
            for row in self.inventory:
                for item in row:
                    if item != None and item not in self.item_group:
                        self.item_group.add(item)
                        print("[INV] - ITEM: {", item.item_id, "} APPENDED")
        """         
    def render_item_text(self):
        self.item_group.update(self.screen)

    def render(self):
        if self.screen != None and self.is_open:
            self.item_frame_group.draw(self.screen)
            self.item_group.draw(self.screen)
            self.render_item_text()
