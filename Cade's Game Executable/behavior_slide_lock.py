from behavior import Behavior
from sounds import Sounds
from pubsub import pub

import numpy

class SlideLock(Behavior):
    def __init__(self, player, name, open, speed, radius, door_length, opening = None, closing = None):
        super(SlideLock, self).__init__()
        
        from game_logic import GameLogic
        self.player = GameLogic.get_object(player)
        self.name = name
        self.open = open
        self.speed = speed
        self.radius = radius
        self.door_length = door_length
        self.opening = opening
        self.closing = closing
        self.previous_open = self.open
        self.unlocked = False
        
        pub.subscribe(self.unlock, self.name)
        
    def unlock(self):
        self.unlocked = True
        
    def connect(self, game_object):
        super(SlideLock, self).connect(game_object)
        self.open_position = self.game_object.position[0] - self.door_length
        self.closed_position = self.game_object.position[0]
        self.start_position = list(self.game_object.position)
            
    def tick(self):
        if self.unlocked:
            door_location = numpy.array(self.start_position)
            player_location = numpy.array(self.player.position)  
            distance = numpy.linalg.norm(door_location - player_location)
            direction_vector = (door_location - player_location) / distance
            
            if distance < self.radius:         
                self.open = True
                
            else:
                self.open = False
                
            if self.previous_open != self.open:
                if self.open == True:
                    if self.opening:
                        Sounds.play_sound(self.opening)
                
                if self.open == False:
                    if self.closing:
                        Sounds.play_sound(self.closing)

            if self.open:                
                if self.open_position < self.game_object.position[0]:
                    self.game_object.position[0] -= self.speed
            else:                
                if self.closed_position > self.game_object.position[0]:
                    self.game_object.position[0] += self.speed
                
            self.previous_open = self.open
