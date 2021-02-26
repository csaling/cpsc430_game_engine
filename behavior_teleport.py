from behavior import Behavior
import numpy

class Teleport(Behavior):
    def __init__(self, player, radius, leash_length):
        super(Teleport, self).__init__()
        
        from game_logic import GameLogic
        self.player = GameLogic.get_object(player)
        self.radius = radius
        self.leash_length = leash_length

    def tick(self):
        self.game_object.player_position = self.player.position
        
        dog_location = numpy.array(self.game_object.position)
        player_location = numpy.array(self.player.position)  
        distance = numpy.linalg.norm(dog_location - player_location)
        
        direction_vector = (dog_location - player_location) / distance
        
        if distance > self.radius:
            y = self.game_object.position[1]
            self.game_object.position = player_location + self.leash_length * direction_vector
            self.game_object.position[1] = y
            