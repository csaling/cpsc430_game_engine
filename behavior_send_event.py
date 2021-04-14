from behavior import Behavior
from pubsub import pub

class SendEvent(Behavior):
    def __init__(self, event):
        super(SendEvent, self).__init__()

        self.event = event
    
    def clicked(self, game_object):
        pub.sendMessage(self.event)
        