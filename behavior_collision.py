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
                
                max_direction = max(direction_vector, key = abs)
                indices = [i for i, j in enumerate(direction_vector) if j == max_direction]
        
                velocity = 0.0
                for index in indices:
                    if index == 0:
                        velocity = max(velocity, self.game_object.get_property('x_velocity', 0.1))
                    
                    if index == 1:
                        velocity = max(velocity, self.game_object.get_property('y_velocity', 0.1))
                    
                    if index == 2:
                        velocity = max(velocity, self.game_object.get_property('z_velocity', 0.1))
        
                self.game_object.position = otherpos + (distance + velocity) * direction_vector
