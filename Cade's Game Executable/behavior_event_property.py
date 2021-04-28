from behavior import Behavior
from sounds import Sounds

class EventProperty(Behavior):
    def __init__(self, name, event):
        super(EventProperty, self).__init__()
        
        self.name = name
        self.event = event
                
    def clicked(self, game_object):
        if game_object.get_property(self.name):
            pub.sendMessage(self.event)
        
