from behavior import Behavior
from pubsub import pub

class SendEventDestination(Behavior):
    def __init__(self, name, event):
        super(SendEventDestination, self).__init__()
        
        self.name = name
        self.event = event
        self.ready_to_click = False
        
        pub.subscribe(self.reached_destination, self.event)
        
    def reached_destination(self, game_object):
        self.ready_to_click = True
    
    def clicked(self, game_object):
        if self.ready_to_click:
            pub.sendMessage(self.name)
        