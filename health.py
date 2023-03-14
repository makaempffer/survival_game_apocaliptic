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
        self.create_instance(type)
    
    def __del__(self):
        del self
        
    
    def check_alive(self, owner):
        if self.body_avg <= 0:
            owner.kill()
            return False

    
    def get_total_hp(self) -> int:
        ignored_value = "body_avg"
        hp_sum = 0
        for attribute, value in self.__dict__.items():
            if type(value) == int and attribute != ignored_value:
                hp_sum += value
        return hp_sum
    
    def create_instance(self, type: str):
        """Create a Health object for instance from type"""
        if type == "Player":
            self.head = 100
            self.eye_r = 100
            self.eye_l = 100
            self.mouth = 100
            self.chest = 100
            self.stomach = 100
            self.arm_r = 100
            self.bone_arm_r = 100
            self.hand_r = 100
            self.arm_l = 100
            self.bone_arm_l = 100
            self.hand_l = 100    
            self.fingers_l = 100
            self.fingers_r = 100
            self.leg_l = 100
            self.knee_l = 100
            self.foot_l = 100
            self.leg_r = 100
            self.knee_r = 100  
            self.foot_r = 100
            self.body_avg = self.get_total_hp()

        if type == "zombie":
            self.head = 100
            self.eye_r = 20
            self.eye_l = 20
            self.mouth = 60
            self.chest = 60
            self.stomach = 100
            self.arm_r = random.randint(60, 140)
            self.bone_arm_r = 100
            self.hand_r = 100
            self.arm_l = random.randint(60, 140)
            self.bone_arm_l = 100
            self.hand_l = 30  
            self.fingers_l = 30
            self.fingers_r = 30
            self.leg_l = random.randint(40, 140)
            self.knee_l = 100
            self.foot_l = 100
            self.leg_r = random.randint(40, 140)
            self.knee_r = 50 
            self.foot_r = random.randint(40, 140)
            self.body_avg = self.get_total_hp()

    def update_current_hp(self):
        self.body_avg = self.get_total_hp()

    def choose_random_body_part(self):
        body_part_hit = random.choice(list(self.__dict__.items()))
        body_part, hp = body_part_hit
        return body_part

    def get_body_part_hp(self, body_part: str):
        hp = self.__getattribute__(body_part)
        return hp

    def receive_damage(self, damageAmount: int):
        if self.body_avg >= 1:
            body_part_hit = self.choose_random_body_part()
            if self.__getattribute__(body_part_hit) >= damageAmount:
                self.__setattr__(body_part_hit, self.get_body_part_hp(body_part_hit) - damageAmount)
            else:
                self.__setattr__(body_part_hit, self.get_body_part_hp(body_part_hit) - self.get_body_part_hp(body_part_hit))
            self.update_current_hp()
            #print("[HEALTH] - LAST HIT ON", body_part_hit,"TOTAL HP:", self.body_avg)


    def give_damage(self, target, amount: int):
        if target:
            if target.body_avg >= 1:
                target.receive_damage(amount)

            
    def update(self, owner):
        self.check_alive(owner)





    