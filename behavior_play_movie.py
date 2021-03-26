from behavior import Behavior
from pubsub import pub

class PlayMovie(Behavior):
    
    def __init__(self, playevent, start):
        super(PlayMovie, self).__init__()
        
        self.playevent = playevent
        self.start = start
        self.started = False
        
    def tick(self):
        if not self.started and self.start:
            pub.sendMessage(self.playevent)
            self.started = True        
    