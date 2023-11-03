import pygame as pg
import json
# TODO ADD AMBIENT MUSIC FUNCTION
# Runs in background


with open('./data/items/items.json', 'r') as file:
    item_data = json.load(file)
item_dict = {item['item_id']: item for item in item_data['items']}


class SoundSystem:
    def __init__(self):
        self.sounds = {}
        self.time_ms = 2000
        self.load_item_sounds_from_dict(item_dict)

    def add_sound(self, sound_name: str, path: str, volume=0.5):
        """Add a sound and give it a name"""
        sound = pg.mixer.Sound(path)
        sound.set_volume(volume)
        self.sounds[sound_name] = sound
        print(f"[SOUND-SYS] - ADDED SOUND -> {sound_name}")
    
    def get_sound(self, sound_name: str) -> pg.mixer.Sound:
        if sound_name in self.sounds:
            return self.sounds.get(sound_name) 
        
    def play_sound(self, sound_name, max_time=0, loops=0):
        sound = self.get_sound(sound_name)
        sound.play(loops, max_time, self.time_ms)
    
    def fadeout_sound(self, sound_name, time_ms=2000):
        sound = self.get_sound(sound_name)
        sound.fadeout(time_ms)
        
    def load_item_sounds_from_dict(self, sounds_dict: dict):
        for key, value in sounds_dict.items():
            if 'sound' in value:
                sound_path = value['sound']
                self.add_sound(key, sound_path, 1)
                
    def setup_sounds(self):
        self.add_sound("walk", './sounds/walk.mp3', 0.1)
        self.add_sound("wood_chop", "./sounds/Wood_chop.wav", 0.9)
        self.add_sound("chop_over", "./sounds/Chop_over.wav", 0.5)
        self.add_sound("pistol_reload", './sounds/guns/pistol_reload.wav', 4)
        self.add_sound("pistol_pack", './sounds/guns/pistol_pack.wav', 4)
        self.add_sound("pistol_rack", './sounds/guns/pistol_rack.wav', 4)
        self.add_sound("pistol_dry_fire", './sounds/guns/pistol_dry_fire.wav', 4)
        self.add_sound("knife_cut", "./sounds/knife_cut.wav", 1)
        self.add_sound("bandage", "./sounds/bandage.mp3", 0.4)
        self.add_sound("footstep_gravel", "./sounds/footstep_gravel.wav", 1)
        self.add_sound("smoke", "./sounds/cigarette_smoke.mp3", 0.2)
        print("[SOUND-SYS] - SETUP SOUNDS.")
    
    def stop_sound(self, sound_name: str):
        sound = self.sounds.get(sound_name)
        sound.stop()
        

