from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds

class ItemTransfer(Behavior):
    def __init__(self, name, value, sound = None):
        super(ItemTransfer, self).__init__()
        
        self.name = name
        self.value = value
        self.sound = sound
        
    def clicked(self, game_object):
         if self.game_object.get_property(self.name) == self.value:
             self.game_object.set_property(self.name, None)
             game_object.set_property(self.name, self.value)
             
         if self.sound:
                Sounds.play_sound(self.sound)
             