from behavior import Behavior
from game_logic import GameLogic
import numpy

class Goto(Behavior):
    def __init__(self, destination, speed, distance, start):
        super(Goto, self).__init__()
        
        self.destination = destination
        self.speed = speed
        self.distance = distance
        self.start = start
        
    def clicked(self, game_object):
        self.start = True
    
    def get_destination(self):
        result = None
        
        if type(self.destination) == list:
            result = self.desetination
            
        if type(self.destination) == str:
            obj = GameLogic.get_object(self.destination)
            
            if obj:
                result = obj.position
        
        return result
    
    def tick(self):
        if self.start:
            destination = self.get_destination()
            
            if not destination:
                return
            
            destination = numpy.array(destination)
            current = numpy.array(self.game_object.position)
            distance = numpy.linalg.norm(destination - current)
            
            if distance <= self.distance:
                return
            
            direction_vector = (destination - current) / distance
            self.game_object.position = (current + self.speed * direction_vector).tolist()
            self.game_object._moved = True
            
