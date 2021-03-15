from behavior import Behavior
from pubsub import pub

class StartBehavior(Behavior):
    def __init__(self, name):
        super(StartBehavior, self).__init__()
        
        self.name = name
        
    def clicked(self, game_object):
        pub.sendMessage(self.name)
        