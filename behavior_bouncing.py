from behavior import Behavior
from sounds import Sounds

class Bouncing(Behavior):
    def __init__(self, allow_rotation, speed, minRot, maxRot, key, sound = None):
        super(Bouncing, self).__init__()
        
        self.allow_rotation = allow_rotation
        self.speed = speed
        self.minRot = minRot
        self.maxRot = maxRot
        self.key = key
        self.sound = sound
        
    def tick(self):
        if self.allow_rotation:
            
            self.game_object.z_rotation += self.speed
            if self.game_object.z_rotation <= self.maxRot:
                self.speed = self.speed * -1

            if self.game_object.z_rotation >= self.minRot:
                self.speed = self.speed * -1
                
    def clicked(self, game_object):
        if game_object.get_property(self.key):
            if self.sound:
                Sounds.play_sound(self.sound)
                
            self.allow_rotation = not self.allow_rotation
        