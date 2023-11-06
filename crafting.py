import json

# Load the JSON data from the file
with open('crafting_recipes.json', 'r') as file:
    data = json.load(file)

# Accessing the crafting recipes
recipes = data["recipes"]

# Accessing individual recipes
recipe_dict = {recipe["product"]: recipe for recipe in recipes}
    
class Crafting:
    def __init__(self, inventory) -> None:
        self.inventory = inventory
        self.screen = inventory.screen
        self.recipes = {}
        self.load_recipe_dict(recipe_dict)
    
    def load_recipe_dict(self, recipes_dict: dict):
        self.recipes = recipes_dict
        print("[CRAFT] - Recipies loaded.")
        
    def get_recipe_inputs(self, item_name):
        recipe = self.recipes[item_name]
        inputs = recipe["input"]
        
        
    
        
    
        
    