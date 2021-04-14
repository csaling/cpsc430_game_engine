from behavior import Behavior
from game_logic import GameLogic
from pubsub import pub

class DeleteAtLocation(Behavior):
    def __init__(self, event):
        super(DeleteAtLocation, self).__init__()
        
        self.event = event
        self.ready_to_click = False
        
        pub.subscribe(self.reached_destination, self.event)
    
    def reached_destination(self, game_object):
        self.ready_to_click = True
    
    def clicked(self, game_object):
        if self.ready_to_click:
            self.game_object.delete()
