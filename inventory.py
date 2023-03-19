from settings import *

class Item(pg.sprite.Sprite):
    def __init__(self, x, y, item_id: str = "EMPTY"):
        super().__init__()
        self.item_id = item_id
        self.size = 32
        self.rect = pg.Rect(x, y, 32, 32)
        self.image = None
        self.item_quantity: int = 0
        self.is_stackable = False
        self.get_item_sprite()
    
    def get_item_sprite(self):
        if self.item_id == "EMPTY":
            self.image = pg.image.load("./assets/item_frame.png").convert_alpha()
        if self.item_id == "MONEY":
            self.is_stackable = True
            self.image = pg.image.load("./assets/money.png").convert_alpha()
        if self.item_id == "BANDAGE":
            self.is_stackable = True
            self.image = pg.image.load("./assets/bandage.png").convert_alpha()

class Inventory:
    def __init__(self, screen=None) -> None:
        self.x_start = WIDTH // 3
        self.y_start = HEIGHT // 2
        self.item_frame_group = pg.sprite.Group()
        self.item_group = pg.sprite.Group()
        self.screen = screen
        self.rows = 5
        self.columns = 5
        self.inventory = None
        self.is_open = False

        self.create_item_frame_group()
        self.create_inventory()
        self.insert_item(3, 3, Item(self.x_start + 3*32, self.y_start + 3*32, "MONEY"))
        self.update_item_group()

    def create_item_frame_inventory(self):
        return [[Item(self.x_start + j*32, self.y_start + i*32) for j in range(self.rows)] for i in range(self.columns)]
    
    def create_item_frame_group(self):
        frames = self.create_item_frame_inventory()
        if len(self.item_frame_group) == 0:
            for row in frames:
                for item in row:
                    self.item_frame_group.add(item)

    def create_inventory(self):
        self.inventory = [[None for j in range(self.rows)] for i in range(self.columns)]
    
    def get_inv(self):
        return self.inventory

    def insert_item(self, pos_x, pos_y, item="X"):
            if self.inventory[pos_x][pos_y] == None:
                self.inventory[pos_x][pos_y] = item
                print("[INV] - ITEM INSERTED")
            else:
                for slot in self.inventory:
                    if slot == None:
                        slot = item
                        print("[INV] - ITEM AUTO PLACED")
                print("[INV] - NO SLOTS AVAILABLE")

    def update_item_group(self):
        if len(self.inventory) > 0:
            for row in self.inventory:
                for item in row:
                    if item != None and item not in self.item_group:
                        self.item_group.add(item)
    
    def render(self):
        if self.screen != None:
            self.item_frame_group.draw(self.screen)
            self.item_group.draw(self.screen)


