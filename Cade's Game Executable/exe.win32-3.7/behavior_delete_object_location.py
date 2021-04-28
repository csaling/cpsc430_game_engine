from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds
from pubsub import pub

class DeleteAtLocation(Behavior):
    def __init__(self, event, sound = None):
        super(DeleteAtLocation, self).__init__()
        
        self.event = event
        self.sound = sound
        self.ready_to_click = False
        
        pub.subscribe(self.reached_destination, self.event)
    
    def reached_destination(self, game_object):
        self.ready_to_click = True
    
    def clicked(self, game_object):
        if self.ready_to_click:
            self.game_object.delete()
            
            if self.sound:
                Sounds.play_sound(self.sound)
