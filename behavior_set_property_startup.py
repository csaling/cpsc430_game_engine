from behavior import Behavior
from game_logic import GameLogic

class SetPropertyStartup(Behavior):
    def __init__(self, name, value):
        super(SetPropertyStartup, self).__init__()
        
        self.name = name
        self.value = value
        self.ticks = False
        
    def tick(self):
        if self.ticks == True:
             self.game_object.get_property(self.name, self.value)
             self.ticks = False
             
