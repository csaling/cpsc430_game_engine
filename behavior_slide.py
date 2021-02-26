from behavior import Behavior

import numpy

class Slide(Behavior):
    def __init__(self, player, open, speed, radius, door_length):
        super(Slide, self).__init__()
        
        from game_logic import GameLogic
        self.player = GameLogic.get_object(player)
        self.open = open
        self.speed = speed
        self.radius = radius
        self.door_length = door_length
        
    def connect(self, game_object):
        super(Slide, self).connect(game_object)
        self.open_position = self.game_object.position[0] - self.door_length
        self.closed_position = self.game_object.position[0]
        self.start_position = list(self.game_object.position)
            
    def tick(self):
        
        door_location = numpy.array(self.start_position)
        player_location = numpy.array(self.player.position)  
        distance = numpy.linalg.norm(door_location - player_location)
        direction_vector = (door_location - player_location) / distance
        
        if distance < self.radius:         
            self.open = True
            
        else:
            self.open = False
            
        if self.open:
            if self.open_position < self.game_object.position[0]:
                self.game_object.position[0] -= self.speed
        else:
            if self.closed_position > self.game_object.position[0]:
                self.game_object.position[0] += self.speed
            
