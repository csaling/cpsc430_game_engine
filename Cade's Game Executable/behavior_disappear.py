from behavior import Behavior
from game_logic import GameLogic

class Disappear(Behavior):
    def __init__(self, name, value):
        super(Disappear, self).__init__()
        
        self.name = name
        self.value = value
        
    def clicked(self, game_object):
        if self.game_object.get_property(self.name) == self.value:
            Gamelogic.delete_object(self.game_object)