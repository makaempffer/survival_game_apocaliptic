from settings import *
from functions import *
    
class Director:
    def __init__(self, npc_manager, block_manager) -> None:
        self.counter = 0
        self.cycle = 1
        self.clock = Clock()
        self.run_clock = True
        self.npc_manager = npc_manager
        self.block_manager = block_manager
        self.screen = block_manager.screen
        self.cycle_changed = False
        self.last_cycle = None
        self.difficulty = 1
        self.start()
        
    def update(self):
        #print(self.cycle)
        self.tick()
        self.counter_logic()
        self.clock.update()
        if self.cycle_changed:
            self.spawn_enemies()
            self.difficulty_logic()
            self.world_day_time(False)
            self.game_clock()
    
    def render_clock(self):
        self.clock.render_clock(self.screen)
    
    def tick(self):
        if self.run_clock:
            self.counter += 1
            if self.cycle != self.last_cycle:
                print("[DIR] CYCLE CHANGED.")
                self.cycle_changed = True
            if self.cycle == self.last_cycle:
                self.cycle_changed = False     
            
            self.last_cycle = self.cycle           
        
    def counter_logic(self):
        if self.counter >= CYCLE_DURATION:
            self.counter = 1
            self.cycle += 1
            
    def world_day_time(self, bypass: bool):
        if self.cycle % DAYTIME_INTERVAL == 0 or bypass:
            print("[DIR] - DAYTIME CHANGED.")
            alpha_level = mapFromTo(self.cycle, 1, 1000, 100, 255)
            self.block_manager.set_world_alpha(alpha_level)
        
    def difficulty_logic(self):
        if self.cycle % SPAWN_INTERVAL_CYCLES == 0:
            self.increase_difficulty()
    
    def game_clock(self):
        self.clock.cycle(self.cycle)
        
    def increase_difficulty(self):
        self.difficulty += 1            
            
    def spawn_enemies(self):
        if self.cycle % SPAWN_INTERVAL_CYCLES == 0:
            self.npc_manager.spawn_enemies(self.difficulty)
            
    def start(self):
        """Setup the environment world start."""
        self.world_day_time(True)
        

class Clock:
    def __init__(self):
        self.minute:int = 0
        self.hour:int = 0
        self.day:int = 0
        
    def increase_minute(self):
        self.minute += 1
    
    def increase_hour(self):
        self.hour += 1
        self.minute = 0
        
    def increase_day(self):
        self.day += 1
        self.hour = 0
    
    def update(self):
        self.logic()
        
    def logic(self):
        if self.minute >= 60:
            self.increase_hour()
        elif self.hour >= 24:
            self.increase_day()
            
    def cycle(self, cycle):
        if cycle % GAME_TIME_MINUTE_CYCLE == 0:
            self.increase_minute()
            #print(f"{self.minute}:{self.hour}:{self.day}")
    
    def render_clock(self, screen):
        rect = pg.Rect(CLOCK_X, CLOCK_Y, 92, 92)
        text = FONT.render(f"{self.minute}:{self.hour}:{self.day}", True, (255, 255, 255))
        screen.blit(text, rect)