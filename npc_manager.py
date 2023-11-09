from settings import *
from random import randrange,randint, choice
from npc import NPC
class NPCManager():
    def __init__(self, screen, width=WIDTH, height=HEIGHT):
        self.npc_group = pg.sprite.Group()
        self.screen = screen
        self.map = []
        self.sizeX, self.sizeY = width, height
        self.setupNpc()

    def get_npcs(self):
        for npc in self.npc_group: return npc
    
    def npcEvent(self):
        self.npc_group.move()
        
    def remove_dead_npc(self):
        for npc in self.npc_group:
            if not npc.health.check_alive():
                self.npc_group.remove(npc)
                npc.kill()

    def setupNpc(self):
        self.create_spawns()
        #self.spawn()
    
    def update(self, delta_time, player):
        for npc in self.npc_group:
            npc.update(delta_time)
            npc.check_entity_in_range(player)
        self.remove_dead_npc()

    def spawn_npc(self,x, y,type="zombie", difficulty=1):
        if len(self.npc_group) < ENTITY_SPAWN_LIMIT:
            self.npc_group.add(NPC(x, y, type, difficulty))

    def render(self):
        self.npc_group.draw(self.screen)

    def create_spawns(self):
        noise = PerlinNoise(octaves=7, seed=1)
        xpix, ypix = HEIGHT//BLOCK_SIZE, WIDTH//BLOCK_SIZE
        self.rows, self.cols = (self.sizeX//BLOCK_SIZE, self.sizeY//BLOCK_SIZE)
        arr = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
        self.map = arr
        print("[NPC-M] - NPC MAP CREATED")
    
    def spawn(self):
        if len(self.map) > 1:
            for x, row in enumerate(self.map):
                for y, col in enumerate(row):
                    if x == 0 and y == 0:
                        print("SPAWNING TRADER")
                        self.spawn_npc(20, 10, "trader")
                        continue
                    if self.map[x][y] >= -0.4 and self.map[x][y] <= -0.3:
                        choice = randrange(0, 10)
                        if choice > 8:
                            self.spawn_npc(x, y, "zombie") 
            print("[NPC-M] - NPC SPAWN DONE")
            
    def random_point_near_edges(self, screen_width, screen_height, min_distance_to_center=50):
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Calculate the allowable range for enemy spawn near the edges
        x_range = screen_width - 2 * min_distance_to_center
        y_range = screen_height - 2 * min_distance_to_center

        if x_range <= 0 or y_range <= 0:
            raise ValueError("Screen dimensions are too small for the specified minimum distance to the center.")

        # Randomly choose to spawn near the horizontal or vertical edge
        spawn_near_horizontal_edge = randint(0, 1)

        if spawn_near_horizontal_edge:
            x = randint(0, screen_width)
            if x < center_x:
                x -= min_distance_to_center
            else:
                x += min_distance_to_center
            y = randint(min_distance_to_center, screen_height - min_distance_to_center)
        else:
            y = randint(0, screen_height)
            if y < center_y:
                y -= min_distance_to_center
            else:
                y += min_distance_to_center
            x = randint(min_distance_to_center, screen_width - min_distance_to_center)
            
        position = pg.Vector2(x, y)
        choices = [(0,0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]
        if position.distance_to((WIDTH//2, HEIGHT//2)) < WIDTH//3:
            pos_x, pos_y = choice(choices)
            pos_x += EDGE_SPAWN_OFFSET
            if y < HEIGHT//2:
                pos_y += EDGE_SPAWN_OFFSET
            else:
                pos_x += EDGE_SPAWN_OFFSET
            
            return pos_x, pos_y

        return x, y

            
    def spawn_enemies(self, difficulty):
        amount = randrange(MIN_SPAWN_AMOUNT, MAX_SPAWN_AMOUNT)
        for i in range(amount):
            x, y = self.random_point_near_edges(WIDTH, HEIGHT, EDGE_SPAWN_MARGIN)
            self.spawn_npc(x, y, "zombie", difficulty)