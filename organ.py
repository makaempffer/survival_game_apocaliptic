class Organ:
    def __init__(self, organ_name, MAX_CAPACITY):
        '''Organ class, capacity works as another hp bar but only
        affects how the organ is working. Ex: high rate in the heart'''
        self.organ_name = organ_name
        self.MAX_CAPACITY = MAX_CAPACITY
        self.capacity = MAX_CAPACITY
        self.healthiness = MAX_CAPACITY
        
    def fill_capacity(self, amount):
        self.capacity += amount
        if self.capacity > self.MAX_CAPACITY:
            self.capacity = self.MAX_CAPACITY
            
    def drain_capacity(self, amount):
        self.capacity -= amount
        if self.capacity < 0:
            self.capacity = 0
            
    def get_capacity(self):
        return self.capacity
            
    def check_capacity(self):
        return self.capacity > 1
    
    def healthiness_decrease(self, amount):
        self.healthiness -= amount
        
    def healthiness_increase(self, amount):
        self.healthiness += amount
        
    def idle_drain(self):
        self.drain_capacity(0.1)
    
    def update(self):
        self.check_healthiness()
        self.check_capacity()
        
    def check_healthiness(self):
        '''If user is unhealthy, his capicity is being decreased constantly.'''
        if self.healthiness < self.MAX_CAPACITY / 3:
            print("UNHEALTHY")
            self.drain_capacity(0.001)
    