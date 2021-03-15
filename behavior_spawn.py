from behavior import Behavior
from math import pi, cos, sin
from random import random
import copy

class Spawn(Behavior):
    def __init__(self, name, radius, amount, adjust):
        super(Spawn, self).__init__()
        
        self.name = name
        self.radius = radius
        self.amount = amount
        self.current_amount = 0
        self.adjust = adjust
      
    def clicked(self, game_object):
        self.current_amount = self.amount
        
    def tick(self):
        from game_logic import GameLogic
        if self.current_amount:
            obj = GameLogic.get_object(self.name)
            obj = copy.deepcopy(obj)
            obj.name = None
            obj.position = self.point()
            GameLogic.add_object(obj)
            self.current_amount -= 1
            
    def point(self):
        theta = random() * 2 * pi
        return self.game_object.position[0] + cos(theta) * self.radius, self.game_object.position[1] + self.adjust, self.game_object.position[2] + sin(theta) * self.radius
        
