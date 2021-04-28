from behavior import Behavior
from pubsub import pub

class PlayMovie(Behavior):
    
    def __init__(self, playevent, begin, start):
        super(PlayMovie, self).__init__()
        
        self.playevent = playevent
        self.start = start
        self.begin = begin
        self.started = False
        
        pub.subscribe(self.start_movie, self.begin)
        
    def start_movie(self):
        self.start = True
        
    def tick(self):
        if not self.started and self.start:
            pub.sendMessage(self.playevent)
            self.started = True        
    