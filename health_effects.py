from settings import *
# Add hunger and thirst to the health object

class HealthEffects:
    """Class that applies all the corresponding effects to the user,
    bleeding, broken bones, etc.
    ## Requires a health object reference."""
    def __init__(self, user_health_ref, inventory_ref):
        self.health = user_health_ref
        self.inventory = inventory_ref
        self.bleeding: bool = False
        self.stomach_size = 50
        self.bladder_size = 50
        
    def physical_updates(self):
        amount = 0.1
        self.health.hunger -= amount
        self.health.thirst -= amount
        
    def consume_item_effect(self, item):
        if item.item_type:
            print(f"[HEALTH-EFFECTS] -> ITEM: {item}")
            if item.item_type == "hemostat":
                print("[HEALTH-EFFECTS] - HEMOSTAT APPLIED.")
                self.bleeding = False
                
            elif item.item_type == "food":
                satisfy_amount = float(item.amount)
                consumed_sum = self.health.hunger + satisfy_amount
                if consumed_sum > self.stomach_size:
                    print(f"[HEALTH-EFFECTS] - CONSUMED FOOD {item.item_id} {item.amount}")
                    self.health.stomach -= satisfy_amount
                    self.health.hunger += satisfy_amount
                    
            elif item.item_type == "drink":
                satisfy_amount = float(item.amount)
                consumed_sum = self.health.thirst + satisfy_amount
                if consumed_sum > self.bladder_size:
                    self.health.stomach -= satisfy_amount
                    self.health.thirst += satisfy_amount
                    print(f"[HEALTH-EFFECTS] - CONSUMED DRINK {item.item_id} {item.amount}")
                    
            elif item.item_type == "analgesic":
                print(f"[HEALTH-EFFECTS] - CONSUMED ANALGESIC. {item.item_id} {item.amount}")
                