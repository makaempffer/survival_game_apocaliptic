def mapFromTo(x_input, in_range_start, in_range_start_end, out_range_start, out_range_end):
   y=(x_input - in_range_start) / (in_range_start_end-in_range_start) * (out_range_end-out_range_start) + out_range_start
   return y

def apply_resistance(initial_damage, resistance_level, resistance_factor=0.2) -> float:
   """Used to apply armor and other resistances to damage, factor should be always {0,1}."""
   damage = initial_damage - (resistance_level * resistance_factor)
   damage = max(damage, 0)
   return damage

def calculate_damage(initial_damage, skill_level, factor):
   damage = initial_damage + (skill_level * factor)
   damage = max(damage, 0)
   return damage
