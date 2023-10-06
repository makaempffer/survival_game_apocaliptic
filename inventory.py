from settings import *
import pygame as pg
import json

with open('./data/items/items.json', 'r') as file:
    item_data = json.load(file)
item_dict = {item['item_id']: item for item in item_data['items']}

class Item(pg.sprite.Sprite):
    def __init__(self, x=0, y=0, item_id: str = "ITEM_FRAME"):
        super().__init__()
        self.item_id = item_id
        self.ITEM_SIZE = 12
        self.size = ITEM_SIZE
        self.rect = pg.Rect(x, y, ITEM_SIZE, ITEM_SIZE)
        self.image = None
        self.item_quantity: int = 1
        self.stackable = False
        self.consumable = False
        self.placeable = False
        self.equipable = False
        self.item_type = ""
        self.create_from_dict(item_dict)
        # self.get_item_sprite()
  
    def update(self, screen):
        self.font_set_quantity(screen)

    def font_set_quantity(self, screen):
        # Only show stackables quantity
        if not self.stackable:
            return
        rect = pg.Rect(self.rect.x, self.rect.y, ITEM_SIZE, ITEM_SIZE)
        text = FONT.render(str(self.item_quantity), True, (255, 255, 255))
        screen.blit(text, rect)

    def consume(self):
        self.item_quantity -= 1
        
    def set_item_to(self, item_id):
        self.item_id = item_id
        self.create_from_dict(item_dict)
    
    def create_from_dict(self, _dict):
        if pg.get_init(): 
            id = self.item_id            
            if id == "ITEM_FRAME":
                self.image = pg.image.load("./assets/icons/item_frame_icon.png").convert_alpha()
                return
            if self.item_id in _dict:
                for key, value in _dict[id].items():
                    setattr(self, key, value)
            self.load_image()
        
    def load_image(self):
        if self.file_path:
            self.image = pg.image.load(self.file_path).convert_alpha()
            print("[ITEM] - IMAGE LOADED.")

    

class Inventory:
    def __init__(self, screen=None) -> None:
        self.rows = 10
        self.columns = 6
        self.ITEM_SIZE = 12
        self.x_start = WIDTH - self.ITEM_SIZE * self.rows
        self.y_start = 0 + 12
        self.item_frame_group = pg.sprite.Group()
        self.item_group = pg.sprite.Group()
        self.screen = screen
        self.inventory = None
        self.is_open = False
        self.consumable_stack = []
        self.last_consumed = None
        self.selected_item = None
        self.last_equiped = None
        self.create_item_frame_group()
        self.create_inventory()
        
        # self.update_item_group()
            
            
    def get_inventory_weight(self):
        weight = 0
        for item in self.item_group:
            item_weight = item.weight * item.item_quantity
            weight += item_weight
        print(f"[INV] - INVENTORY WEIGHT {weight}")
        return weight
        
    def decrease_item_count(self, item, amount=1):
        item = self.get_item_slot(item)
        item.item_quantity -= amount

    def setup_starting_items(self):
        self.add_item("BANDAGE", 3)
        self.add_item("IRON_BAR", 5)
        self.add_item("WOOD_TABLE", 1)
        self.add_item("BREAD", 5)
        self.add_item("PILL", 3)
        self.add_item("AMMO_9MM", 16)
        self.add_item("BOTTLE")
        self.add_item("PICKAXE")
        self.add_item("PISTOL")
        self.add_item("PICKAXE")
        self.add_item("CIGARRETE_UNLUCKY", 5)

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
                self.inventory[slot_x][slot_y] = item

    def create_item_frame_inventory(self):
        return [[Item(self.x_start + j * self.ITEM_SIZE, self.y_start + i * self.ITEM_SIZE) for j in range(self.rows)] for i in range(self.columns)]

    # NOT WORKING RIGHT
    # def create_item_frame_inventory(self):
        # return [[Item(self.x_start + j*ITEM_SIZE, self.y_start + i*ITEM_SIZE) for j in range(self.rows)] for i in range(self.columns)]

    def use_consumable(self, item):
        if item.is_consumable:
            item.consume()

    def update_item_player_effects(self):
        """All item-player related update-calls here."""
        self.consume_stack()

    def create_item_frame_group(self):
        frames = self.create_item_frame_inventory()
        if len(self.item_frame_group) == 0:
            for row in frames:
                for item in row:
                    self.item_frame_group.add(item)

    def get_sprites(self):
        print("[INV] - GETTING ITEMS.")
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
                    item.rect.x = self.x_start + y * ITEM_SIZE 
                    item.rect.y = self.y_start + x * ITEM_SIZE

    def create_inventory(self):
        self.inventory = [[None for j in range(
            self.rows)] for i in range(self.columns)]

    def get_inventory(self):
        return self.inventory

    def add_item(self, item_name, quantity=1):
    
        for row in self.inventory:
            for slot in row:
                if slot != None:
                    if slot.item_id == item_name and slot.stackable:
                        slot.item_quantity += quantity
                        print(f"[INV] - ADDED QUANTITY {quantity} TO {slot.item_id}")
                        return
                    
        for x, row in enumerate(self.inventory):
            for y, slot in enumerate(row):
                if slot == None:
                    item = Item(0, 0, item_name)
                    item.item_quantity = quantity
                    print("[INV] - FILLED CLOSEST EMPTY SLOT.")
                    item.rect.x = self.x_start + x * ITEM_SIZE
                    item.rect.y = self.y_start + y * ITEM_SIZE 
                    #slot = item
                    self.inventory[x][y] = item
                    return

        print("[INV] - NO SLOTS AVAILABLE OR ITEM DOESN'T EXIST")

    def add_to_consumable_stack(self, item):
        if item.consumable and item not in self.consumable_stack:
            print(f"[INV] - APPENDED CONSUMABLE {item} TO STACK.")
            self.consumable_stack.append(item)

    def consume_stack(self):
        if len(self.consumable_stack) < 1:
            return
        item = self.consumable_stack.pop()
        self.last_consumed = item
        item.consume()
        
    def select_item(self, item):
        if item.placeable:
            self.selected_item = item
        else:
            self.selected_item = None
            
    def get_item_slot(self, _item) -> Item:
        for row in self.inventory:
            for item in row:
                if item == _item:
                    return item
                    

    def get_item(self) -> Item:
        if not pg.mouse.get_pressed()[0]:
            return
        mouse_x, mouse_y = pg.mouse.get_pos()
        for row in self.inventory:
            for item in row:
                if item != None:
                    if mouse_x >= item.rect.x and mouse_x <= item.rect.x + ITEM_SIZE:
                        if mouse_y >= item.rect.y and mouse_y <= item.rect.y + ITEM_SIZE:
                            self.add_to_consumable_stack(item)
                            self.select_item(item)
                            if item.equipable:
                                self.last_equiped = item
                            return item

    def kill_consumed(self):
        self.last_consumed = None

    def check_empty(self):
        for x, row in enumerate(self.inventory):
            for y, item in enumerate(row):
                if item == None or item.item_id == "EMPTY":
                    continue
                if item.item_quantity <= 0:
                    print(f"[INV] - DELETING ITEM -> {item.item_id}")
                    self.item_group.remove(item)
                    self.inventory[x][y] = None

    def update(self):
        self.update_item_group()
        self.update_sprites_positions()
        self.get_item()
        self.check_empty()

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

    def render_item_text(self):
        self.item_group.update(self.screen)

    def render(self):
        if self.screen != None and self.is_open:
            self.item_frame_group.draw(self.screen)
            self.item_group.draw(self.screen)
            self.render_item_text()
