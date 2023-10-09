

class Skills:
    def __init__(self):
        self.strength = 1
        self.agility = 1
        self.scavenger = 1
        self.perception = 1
        self.accuracy = 1
        self.strength_xp = 0
        self.agility_xp = 0
        self.scavenger_xp = 0
        self.perception_xp = 0
        self.accuracy_xp = 0
        
    def set_skill_level(self, skill, level):
        self.__setattr__(skill, level)