from behavior import Behavior
import numpy

class Pull(Behavior):
    def __init__(self, kind, speed):
        super(Pull, self).__init__()

        self.speed = speed
        self.kind = kind

    def tick(self):
        
        from game_logic import GameLogic
        
        for game_object in GameLogic.game_objects:
            if game_object.kind == self.kind:
        
                dog_location = numpy.array(game_object.position)
                player_location = numpy.array(self.game_object.position)
                distance = numpy.linalg.norm(dog_location - player_location)
                
                direction_vector = (dog_location - player_location) / distance
                
                y = game_object.position[1]
                game_object.position = player_location + self.speed * direction_vector
                game_object.position[1] = y
            
