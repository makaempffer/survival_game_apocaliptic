import pygame as pg
from perlin_noise import PerlinNoise
FPS = 60
WIDTH, HEIGHT = 1280 + 16, 720 # ADDING 16 PIXELS TO X FIXES RENDERING OFFSET
pg.font.init()
FONT_SIZE = 12
FONT = pg.font.Font('./fonts/TerminusTTFWindows-4.49.3.ttf', FONT_SIZE)
#FONT = pg.font.Font('freesansbold.ttf', 12) #default use font
RED = 255, 0, 0
GREEN = 0, 255, 0
YELLOW = 255, 255, 0

# ASSET DATA
NARRATOR_WIDTH = 150
NARRATOR_HEIGHT = 40
ITEM_SIZE = 24
BLOCK_SIZE = 24 # PIXELS

# HEALTH/COMBAT GAMEPLAY
RESISTANCE_FACTOR = 0.7 # 20% damage reduction from all resistances
SKILLS_FACTOR = 0.5
WEAPON_DAMAGE_FACTOR = 1
ORGAN_DRAIN_AMOUNT = 0.1

# UI
ICON_SIZE = 24
ICON_SPACING = 24
ICON_X_MARGIN = 24
UI_MARGIN = 16
UI_FONT_COLOR = (0, 255, 0)

UI_SIZE_X = 320
UI_SIZE_Y = 192

# LOG
LOG_SPACING = 8
LOG_MARGIN = 64
LOG_START_X = WIDTH - UI_SIZE_X
LOG_START_Y = HEIGHT - LOG_SPACING#UI SIZE
MAX_LOGS = 12
LOG_FONT_COLOR = (255, 255, 255)

def format_two_decimals(number: float):
    formatted_number = "{:.2f}".format(number)
    return formatted_number