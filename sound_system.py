import pygame as pg

# TODO ADD AMBIENT MUSIC FUNCTION
# Runs in background
class SoundSystem:
    def __init__(self):
        self.sounds = {}
        self.time_ms = 2000

    def add_sound(self, sound_name: str, path: str, volume=0.4):
        """Add a sound and give it a name"""
        self.sounds[sound_name] = pg.mixer.Sound(path)
        sound: pg.mixer.Sound = self.get_sound(sound_name)
        sound.set_volume(volume)
        print(f"[SOUND-SYS] - ADDED SOUND -> {sound_name}")
    
    def get_sound(self, sound_name: str) -> pg.mixer.Sound:
        if sound_name in self.sounds:
            return self.sounds.get(sound_name) 
        
    def play_sound(self, sound_name, max_time=0, loops=1):
        sound = self.get_sound(sound_name)
        sound.play(loops, max_time, self.time_ms)
    
    def fadeout_sound(self, sound_name, time_ms=2000):
        sound = self.get_sound(sound_name)
        sound.fadeout(time_ms)
    
    def setup_sounds(self):
        self.add_sound("walk", './sounds/walk.mp3')
        self.add_sound("wood_chop", "./sounds/Wood_chop.wav")
        print("[SOUND-SYS] - SETUP SOUNDS.")
    
    def stop_sound(self, sound_name: str):
        sound = self.sounds.get(sound_name)
        sound.stop()
        

