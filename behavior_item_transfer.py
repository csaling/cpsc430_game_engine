from behavior import Behavior
from game_logic import GameLogic

class ItemTransfer(Behavior):
    def __init__(self, name, value):
        super(ItemTransfer, self).__init__()
        
        self.name = name
        self.value = value
        
    def clicked(self, game_object):
         if self.game_object.get_property(self.name) == self.value:
             self.game_object.set_property(self.name, None)
             game_object.set_property(self.name, self.value)
             print("worked!")
             