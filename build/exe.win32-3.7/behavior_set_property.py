from behavior import Behavior
from gameobject import GameObject
from pubsub import pub

class SetProperty(Behavior):
    def __init__(self, name, value):
        super(SetProperty, self).__init__()
        
        self.name = name
        self.value = value

        
    def clicked(self):
        game_object.set_property(self.name, self.value)
        