import pygame as pg
from settings import *

class UIComponent(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = None
        
    def create_component(self, image_path, x, y, scale=None, rotated=False):
        self.image = pg.image.load(image_path)
        if scale: self.image = pg.transform.scale(self.image, (scale, scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

class UI(pg.sprite.Sprite):
    def __init__(self, screen, player):
        super().__init__()
        self.show = True
        self.screen = screen
        self.player = player
        self.logger = Logger(self.screen)
        self.components = pg.sprite.Group()
        self.icon_data: dict = {}
        self.setup()
        self.process_component_data()
    
    def log(self, text):
        '''Logs a message to the logger to display.'''
        self.logger.add_log(text)
        
    def create_ui_component_data(self, id: str, path: str, x: int, y: int, scale: int=None):
        self.icon_data[id] = [path, x, y, scale]
    
    def process_component_data(self):
        for key, value in self.icon_data.items():
            component = UIComponent()
            component.create_component(value[0], value[1], value[2], value[3])
            self.add_component(component)
            
    def setup(self):
        self.create_ui_component_data("Main UI", "./assets/UI/UI_Display/UI_Bloody_1.png", WIDTH - UI_SIZE_X, HEIGHT - 192)
        self.create_ui_component_data("HP Icon", "./assets/UI_ICONS/heart.png", (WIDTH - UI_SIZE_X + ICON_SIZE * 1 + ICON_SPACING) - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y)
        self.create_ui_component_data("Weight Icon", "./assets/UI_ICONS/weight.png", (WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 2) - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y)
        self.create_ui_component_data("Armor Icon", "./assets/UI_ICONS/armor.png", (WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 3) - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y)
        self.create_ui_component_data("Radioactive", "./assets/UI_ICONS/radioactive.png", WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 4 - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y)
        self.create_ui_component_data("Chicken", "./assets/UI_ICONS/chicken.png", WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 5 - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y)
        self.create_ui_component_data("Water", "./assets/UI_ICONS/water.png", WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 6 - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y)
    
    
    def add_component(self, component):
        self.components.add(component)
        
    def draw_components(self):
        if not self.show:
            return
        self.components.draw(self.screen)
        
    def render_text(self):
        if not self.show:
            return
        self.setup_text()
        self.logger.render_log()
        
    def setup_text(self):
        self.render_text_at(self.player.health.get_health(), (WIDTH - UI_SIZE_X + ICON_SIZE * 1 + ICON_SPACING) - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y, UI_FONT_COLOR)
        self.render_text_at(self.player.inventory.get_inventory_weight(), (WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 2) - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y, UI_FONT_COLOR)
        self.render_text_at(self.player.health_effects.get_armor_rating(),(WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 3) - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y, UI_FONT_COLOR)
        self.render_text_at(self.player.health_effects.current_radiation, WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 4 - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y, UI_FONT_COLOR)
        self.render_text_at(self.player.health.get_hunger(), WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 5 - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y, UI_FONT_COLOR)
        self.render_text_at(self.player.health.get_thirst(), WIDTH - UI_SIZE_X + (ICON_SIZE + ICON_SPACING) * 6 - ICON_X_MARGIN, HEIGHT - UI_SIZE_Y, UI_FONT_COLOR)
    
    def render_text_at(self, text: str, x: int, y: int, color: tuple=(255, 255, 255), offset_start: bool = True):
        if isinstance(text, float):
            text = format_two_decimals(text)
        text = FONT.render(str(text), True, color)
        if offset_start:
            x += ICON_SIZE
        self.screen.blit(text, (x, y))
        
class Logger:
    def __init__(self, screen) -> None:
        '''Shows messages, every new message makes all the 
        messages go up, scrolling'''
        self.stack = []
        self.screen = screen
        self.max_messages = MAX_LOGS
        self.add_log("HELLO WORL THIS A FUCKIN TEST")
        self.add_log("Hello brothesrs this a testing shit")
        
    def add_log(self, log: str, font_color: tuple = LOG_FONT_COLOR):
        if len(self.stack) > MAX_LOGS:
            self.stack.pop()
        self.stack.insert(0, [log, font_color])
    
    def render_log(self):
        for index, log in enumerate(self.stack):
            text = FONT.render(str(log[0]), True, log[1])
            x = LOG_START_X + LOG_SPACING
            y = LOG_START_Y - LOG_SPACING - index * FONT_SIZE
            self.screen.blit(text, (x, y))