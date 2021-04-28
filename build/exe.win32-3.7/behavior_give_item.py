from behavior import Behavior
import numpy

class GiveItem(Behavior):
    def __init__(self, name, value):
        super(GiveItem, self).__init__()
        
        self.name = name
        self.value = value
        
    def connect(self, game_object):
        super(GiveItem, self).connect(game_object)
        self.game_object.set_property(self.name, self.value)
