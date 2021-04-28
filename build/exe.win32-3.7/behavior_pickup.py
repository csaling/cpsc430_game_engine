from behavior import Behavior
from game_logic import GameLogic
from pubsub import pub

class Pickup(Behavior):
    def __init__(self, name, value, begin):
        super(Pickup, self).__init__()
        
        self.name = name
        self.value = value
        self.begin = begin
        
        pub.subscribe(self.set_begin, self.begin)
        
    def set_begin(self, game_object):
        game_object.set_property(self.name, self.value)
        self.game_object.delete()
        
    def delete(self):
        pub.unsubscribe(self.set_begin, self.begin)