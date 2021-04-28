from behavior import Behavior
from pubsub import pub

class Invisibility(Behavior):
    def __init__(self, event):
        super(Invisibility, self).__init__()
        
        self.event = event
        
        pub.subscribe(self.toggle, self.event)
        
    def toggle(self):
        self.game_object.invisible = not self.game_object.invisible