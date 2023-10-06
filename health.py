from settings import *
import random
"""Continue and add methods for:
    # Do damage [N]
    # Receive damage [N]
    # Do damage [N]
    # Die [N]
    #[N]
    #[N]
    #[N]
    #[N]
    #[N]
    #[N]
    #[N]
    #[N]
"""
class Health:
    """Shared Health System for entities."""
    def __init__(self, type: str):
        #super().__init__()   
        self.attack_extremity: str = "arm_r"
        self.is_alive: bool = True 

        self.head: int
        self.eye_r: int
        self.eye_l: int
        self.mouth: int
        self.chest: int
        self.stomach: int
        self.arm_r: int
        self.bone_arm_r: int
        self.hand_r: int
        self.arm_l: int
        self.bone_arm_l: int
        self.hand_l: int    
        self.fingers_l: int
        self.fingers_r: int
        self.leg_l:int
        self.knee_l: int
        self.foot_l: int
        self.leg_r: int
        self.knee_r: int  
        self.foot_r: int
        self.body_avg: int = 0
        self.attack_cooldown: bool = False
        self.counter: int = 0
        self.create_instance(type)
        self.attack_sound = pg.mixer.Sound('./sounds/Hit_hurt.wav')
        self.death_sound = pg.mixer.Sound('./sounds/Death.wav')
        self.attack_sound.set_volume(0.1)
        self.death_sound.set_volume(0.1)
        self.timer = pg.USEREVENT + 1
        self.time_delay = 500
        pg.time.set_timer(self.timer, self.time_delay)

    def __del__(self):
        del self

    def timer_event(self, event):
        if event.type == self.timer:
            self.counter += 1
        
        if self.counter == 1:
            self.attack_cooldown = True
            self.counter = 0
        else:
            self.attack_cooldown = False
    
    def die(self, owner):
        self.is_alive = False
        owner.kill()
        self.death_sound.play()
        return False
    
    def damage_limb_group(self, limbs="arms"):
        pass
        
    def check_alive(self, owner):
        if self.body_avg <= 0:
            owner.kill()
        elif self.head <= 0:
            owner.kill()
    
    def get_total_hp(self) -> float:
        """Returns total hp"""
        hp_summed = (
            self.head + self.eye_r + self.eye_l 
            + self.mouth + self.chest + self.stomach 
            + self.arm_r + self.bone_arm_r + self.hand_r 
            + self.fingers_r + self.arm_l + self.bone_arm_l
            + self.hand_l + self.fingers_l + self.leg_l
            + self.knee_l + self.foot_l + self.leg_r
            + self.knee_r + self.foot_r )
        return hp_summed
    
    def apply_modifier(self, modifier: int):
        """Takes a modifier from 1-10"""
        self.head = 100 * (modifier * 0.1)
        self.eye_r = 100 * (modifier * 0.1)
        self.eye_l = 100 * (modifier * 0.1)
        self.mouth = 100 * (modifier * 0.1)
        self.chest = 100 * (modifier * 0.1)
        self.stomach = 100 * (modifier * 0.1)
        self.arm_r = 100 * (modifier * 0.1)
        self.bone_arm_r = 100 * (modifier * 0.1)
        self.hand_r = 100 * (modifier * 0.1)
        self.arm_l = 100 * (modifier * 0.1)
        self.bone_arm_l = 100 * (modifier * 0.1)
        self.hand_l = 100 * (modifier * 0.1)
        self.fingers_l = 100 * (modifier * 0.1)
        self.fingers_r = 100 * (modifier * 0.1)
        self.leg_l = 100 * (modifier * 0.1)
        self.knee_l = 100 * (modifier * 0.1)
        self.foot_l = 100 * (modifier * 0.1)
        self.leg_r = 100 * (modifier * 0.1)
        self.knee_r = 100 * (modifier * 0.1)
        self.foot_r = 100 * (modifier * 0.1)
        self.body_avg = self.get_total_hp()

    
    def create_instance(self, type: str):
        """Create a Health object for instance from type"""
        if type == "Player":
            self.apply_modifier(10) 
            self.hunger = 15
            self.thirst = 15
        if type == "zombie":
            self.apply_modifier(5)

    def update_current_hp(self):
        self.body_avg = self.get_total_hp()

    def get_most_damaged_part(self):
        part_list = list(self.__dict__.items())
        skip_list = ["hunger", "thirst", "body_avg", "attack_extremity", "is_alive", "attack_sound", "death_sound", "timer", "time_delay", "counter", "attack_cooldown"]
        most_damaged = None
        part = None
        # Fix using wrong body parts.
        for body_part, hp in part_list:
            if body_part in skip_list:
                continue
            if most_damaged == None:
                most_damaged = hp
                part = body_part 
            if hp < most_damaged:
                most_damaged = hp
                part = body_part
        print(f"[HEALTH] - MOST DAMAGED - {part}")
        return part

    def choose_random_body_part(self):
        body_list = list(self.__dict__.items())
        skip_list = ["hunger", "thirst", "attack_extremity", "is_alive", "attack_sound", "death_sound", "timer", "time_delay", "counter", "attack_cooldown"]
        cleaned_list = [(key, value) for key, value in body_list if key not in skip_list]
        shuffled_list = random.sample(body_list, k=len(body_list))
        for body_part, hp in shuffled_list:
            if body_part in skip_list:
                continue
            if hp > 0 and body_part != "body_avg":
                print(f"[HEALTH] -> BODY PART {body_part} - {hp}")
                return body_part

    def add_body_part_hp(self, body_part: str, amount):
        hp = self.__getattribute__(body_part)
        self.__setattr__(body_part, (hp + amount))

    def get_body_part_hp(self, body_part: str):
        hp = self.__getattribute__(body_part)
        return hp

    def receive_damage(self, damageAmount: int):
        if self.body_avg >= 1:
            body_part_hit = self.choose_random_body_part()
            if self.__getattribute__(body_part_hit) > 0:
                self.__setattr__(body_part_hit, self.get_body_part_hp(body_part_hit) - damageAmount)
                self.update_current_hp()


    def give_damage(self, target):
        if target:
            if target.body_avg >= 1:
                if self.attack_cooldown:
                    target.receive_damage(self.calculate_damage())
                    self.attack_sound.play()
                    self.attack_cooldown = False

                
    def calculate_damage(self):
        attack_hp = self.__getattribute__(self.attack_extremity)
        damage = 0
        if self.attack_extremity == "arm_r":
            damage = ((attack_hp * 0.05) + (self.bone_arm_r * 0.05) + (self.hand_r * 0.05) + (self.fingers_r * 0.05))
        if self.attack_extremity == "arm_l":
            damage = ((attack_hp * 0.05) + (self.bone_arm_l * 0.05) + (self.hand_l * 0.05) + (self.fingers_l * 0.05))
        if self.attack_extremity == "leg_r":
            damage = ((attack_hp * 0.08) + (self.knee_r * 0.05) + (self.foot_r * 0.05))
        if self.attack_extremity == "leg_l":
            damage = ((attack_hp * 0.08) + (self.knee_l * 0.05) + (self.foot_l * 0.05))
        return damage + 1
        
            
    def update(self, owner):
        self.check_alive(owner)
        self.update_current_hp()





    
