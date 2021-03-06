from behavior import Behavior
from game_logic import GameLogic

class Gravity(Behavior):
    def __init__(self, speed):
        super(Gravity, self).__init__()
        
        self.speed = speed
        self.old_y = 0.0
        
    def tick(self):
        if self.game_object.position[1]:
            self.game_object.set_property('falling', False)
            self.game_object.position[1] = 0.0
            return
        
        self.old_y = self.game_object.position[1]
        self.game_object.position[1] -= self.speed
        
        for other in GameLogic.game_objects:
            if not GameLogic.collide(self.game_object, GameLogic.game_objects[other]):
                continue
            
            if GameLogic.game_objects[other] in self.game_object.collisions:
                continue
            
            self.game_object.position[1] += self.speed
            self.game_object.set_property('falling', False)
            return
        
        if self.old_y != self.game_object.position[1]:
            self.game_object.set_property('falling', True)
        else:
            self.game_object.set_property('falling', False)
        
        self.game_object.set_property('y_velocity', self.game_object.get_property('y_velocity', 0.0) + self.speed)
        self.game_object._moved = True