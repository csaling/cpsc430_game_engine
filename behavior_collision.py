from behavior import Behavior
from pubsub import pub
import numpy
import math

class BlockedByObjects(Behavior):
    
    def tick(self):
        #Handle Collisions
        if self.game_object.collisions:
            mypos = numpy.array(self.game_object.position)
            
            for other in self.game_object.collisions:
                otherpos = numpy.array(other.position)
                distance = numpy.linalg.norm(mypos - otherpos)
                direction_vector = (mypos - otherpos) / distance
                
                self.game_object.position = otherpos + (distance + 0.1) * direction_vector
