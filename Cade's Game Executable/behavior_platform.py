from behavior import Behavior
from game_logic import GameLogic
import numpy

class Platform(Behavior):
    def __init__(self, destination, speed, transport, begin):
        super(Platform, self).__init__()
        
        self.start = None
        self.distance = None
        self.destination = destination
        self.speed = speed
        self.transport = transport
        self.begin = begin
        
    def clicked(self, game_object):
        self.begin = not self.begin
        
    def connect(self, game_object):
        super(Platform, self).connect(game_object)
        
        self.start = numpy.array(game_object.position)
        
    def get_destination(self):
        result = None
        
        if type(self.destination) == list:
            result = self.destination
            
        if type(self.destination) == str:
            obj = GameLogic.get_object(self.destination)
            
            if obj:
                result = obj.position

        return result
        
    def tick(self):
        if self.begin:
            
            destination = self.get_destination()
            
            if not destination:
                return
            
            destination = numpy.array(destination)
            current = numpy.array(self.game_object.position)
            distance = numpy.linalg.norm(self.start - current)
            
            if not self.distance:
                self.distance = numpy.linalg.norm(destination - self.start)
                self.direction_vector = (destination - self.start) / self.distance
            
            riders = []
            
            if self.transport:
                self.game_object.position[1] += 0.1
                
                for other in GameLogic.game_objects:
                
                    if not GameLogic.collide(self.game_object, GameLogic.game_objects[other]):
                        continue
                    
                    if GameLogic.game_objects[other] in self.game_object.collisions:
                        continue
                    
                    riders.append(GameLogic.game_objects[other])
                    
                self.game_object.position[1] -= 0.1
            
            if distance >= self.distance:
                self.direction_vector = -(1 / numpy.linalg.norm(self.direction_vector)) * self.direction_vector
                self.game_object.position = (destination).tolist()
                temp = self.start
                self.start = destination
                self.destination = temp.tolist()
            else:
                self.game_object.position = (self.start + (distance + self.speed) * self.direction_vector).tolist()
                self.move_riders(riders, self.direction_vector, self.speed)
            self.game_object._moved = True
        
    def move_riders(self, riders, direction_vector, speed):
        for rider in riders:
            rider.position = (rider.position + direction_vector * speed).tolist()