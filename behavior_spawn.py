from behavior import Behavior
from math import pi, cos, sin
from random import random

class Spawn(Behavior):
    def __init__(self, rotation, size, color, kind, radius, amount):
        super(Spawn, self).__init__()
        
        self.rotation = rotation
        self.size = size
        self.radius = radius
        self.color = color
        self.kind = kind
        self.radius = radius
        self.amount = amount
        self.current_amount = 0
      
    def click(self):
        self.current_amount = self.amount
        
    def tick(self):
        if self.current_amount:
            GameLogic.create_object(None, self.point(), self.rotation, size, color, kind)
            self.current_amount -= 1
            
    def point(self):
        theta = random() * 2 * pi
        return self.game_object.position[0] + cos(theta) * self.radius, self.game_object.position[1], self.game_object.position[2] + sin(theta) * self.radius
        
