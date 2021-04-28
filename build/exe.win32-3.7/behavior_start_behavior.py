from behavior import Behavior
from pubsub import pub

class StartBehavior(Behavior):
    def __init__(self, name):
        super(StartBehavior, self).__init__()
        
        self.name = name
        self.ticks = True
        
    def tick(self):
        if self.ticks:
            pub.sendMessage(self.name)
            self.ticks = False
        