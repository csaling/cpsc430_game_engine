from behavior import Behavior
from game_object import GameObject
from pubsub import pub
import numpy

class Chase(Behavior):
    def __init__(self, name, speed, distance, event):
        super(Chase, self).__init__()

        self.name = name
        self.speed = speed
        self.distance = distance
        self.event = event

    def tick(self):
        
        from game_logic import GameLogic

        player = GameLogic.get_object(self.name)
        
        if player:

            dog_location = numpy.array(self.game_object.position)
            player_location = numpy.array(player.position)
            distance = numpy.linalg.norm(player_location - dog_location)
            
            direction_vector = (player_location - dog_location) / distance
            
            y = self.game_object.position[1]
            self.game_object.position = (self.game_object.position + self.speed * direction_vector).tolist()
            self.game_object.position[1] = y
            
            if distance < self.distance:
                pub.sendMessage(self.event, game_object = self.game_object)
