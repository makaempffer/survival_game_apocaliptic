import pygame as pg
from perlin_noise import PerlinNoise
FPS = 60
WIDTH, HEIGHT = 1280, 720
pg.font.init()
FONT = pg.font.Font('./fonts/TerminusTTFWindows-4.49.3.ttf', 12)
#FONT = pg.font.Font('freesansbold.ttf', 12) #default use font
RED = 255, 0, 0
GREEN = 0, 255, 0
YELLOW = 255, 255, 0
NARRATOR_WIDTH = 150
NARRATOR_HEIGHT = 40
ITEM_SIZE = 12
BLOCK_SIZE = 12 # PIXELS
RESISTANCE_FACTOR = 0.7 # 20% damage reduction from all resistances
SKILLS_FACTOR = 0.5
WEAPON_DAMAGE_FACTOR = 1
ORGAN_DRAIN_AMOUNT = 0.1
