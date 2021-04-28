from behavior import Behavior
from game_logic import GameLogic
from pubsub import pub

import numpy

class Goto(Behavior):
    def __init__(self, begin, destination, speed, distance, start, event = None):
        super(Goto, self).__init__()
        
        self.destination = destination
        self.speed = speed
        self.distance = distance
        self.start = start
        self.event = event
        self.begin = begin
        self.sent_event = False
        
        pub.subscribe(self.set_begin, self.begin)
        
    def delete(self):
        pub.unsubscribe(self.set_begin, self.begin)
        
    def set_begin(self):
        self.start = True
    
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
        if self.start:
            destination = self.get_destination()
            
            if not destination:
                return
            
            destination = numpy.array(destination)
            current = numpy.array(self.game_object.position)
            distance = numpy.linalg.norm(destination - current)
            
            if distance <= self.distance:
                if self.event and not self.sent_event:
                    pub.sendMessage(self.event, game_object = self.game_object)
                    self.sent_event = True
                    
                return
            
            self.sent_event = False
            direction_vector = (destination - current) / distance
            self.game_object.position = (current + self.speed * direction_vector).tolist()
            self.game_object._moved = True
            
