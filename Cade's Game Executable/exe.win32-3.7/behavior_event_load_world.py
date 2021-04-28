from behavior import Behavior
from pubsub import pub
import pygame

class EventLoadWorld(Behavior):
    def __init__(self, name, event):
        super(EventLoadWorld, self).__init__()

        self.name = name
        self.event = event
        
        pub.subscribe(self.load_world, self.event)

    def load_world(self, game_object):
        from game_logic import GameLogic
        GameLogic.load_world(self.name)
        pygame.mixer.stop()
