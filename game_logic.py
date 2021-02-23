from pubsub import pub

import numpy

from game_object import GameObject
from game_object_player import Player
from behavior_bouncing import Bouncing
from behavior_key_move import KeyMove
from behavior_mouse_rotation import MouseRotation
from behavior_collision import BlockedByObjects
from behavior_slide import Slide
from behavior_spin import Spin
from behavior_move2D import Move2D

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}
        
        self.next_id = 0
    
    def tick(self):
        for game_object in self.game_objects:
            if self.game_objects[game_object].moved:
                for other in self.game_objects:
                    if self.game_objects[game_object] == self.game_objects[other]:
                        continue
                    
                    if self.collide(self.game_objects[game_object], self.game_objects[other]):
                        self.game_objects[game_object].collisions.append(self.game_objects[other])
                    
        for id in self.game_objects:
            self.game_objects[id].tick()
            
    def create_object(self, position, size, kind):

        obj = GameObject(position, size, kind, self.next_id)
        
        self.next_id += 1
        self.game_objects[obj.id] = obj
            
        pub.sendMessage('create', game_object = obj)
        return obj
        
    def load_world(self):
    
        dog = self.create_object ([3, -0.5, -20], [5.0, 5.0, 5.0], "dog")
        dog.add_behavior(Bouncing(True, -0.5, 0, -40))
        
        ball = self.create_object ([-1, 1, -22.5], [0.5, 0.5, 0.5], "ball")
        ball.add_behavior(Spin(2.0, 1))
        ball.add_behavior(Move2D(0.1))
        
        ground = self.create_object ([0, -1, 0], [100.0, 1.0, 100.0], "cube")
        ground.color = (0, 0.9, 0.3)
                                                    #Coordinates      #Scale
        left_wall = self.create_object ([-9.75, 4, -20], [0.5, 10.0, 10.0], "cube")
        left_wall.color = (0.6, 0.3, 0.3)
        
        right_wall = self.create_object ([9.75, 4, -20], [0.5, 10.0, 10.0], "cube")
        right_wall.color = (0.6, 0.3, 0.3)
        
        back_wall = self.create_object ([0, 4, -25], [20, 10.0, 0.5], "cube")
        back_wall.color = (0.6, 0.3, 0.3)
        
        roof = self.create_object ([0, 9, -20], [20, 0.5, 10], "cube")
        roof.color = (0.6, 0.3, 0.3)
        
        floor = self.create_object ([0, -0.5, -19.8], [19, 0.5, 10], "cube")
        floor.color = (1.0, 1.0, 0.0)
        
        front_left = self.create_object ([-6.5, 4, -15], [7, 10.0, 0.5], "cube")
        front_left.color = (0.6, 0.3, 0.3)
        
        front_right = self.create_object ([6.5, 4, -15], [7, 10.0, 0.5], "cube")
        front_right.color = (0.6, 0.3, 0.3)
        
        door = self.create_object ([0, 4, -15], [6, 10.0, 0.5], "door")
        door.color = (1.0, 0.0, 0.0)
        door.add_behavior(Slide(False, 0.1, 5))
        
        player = self.create_object ([0.0, 0.0, 0.0], [1.0, 1.0, 1.0], "player")
        player.add_behavior(KeyMove(0.1))
        player.add_behavior(MouseRotation(0.1))
        player.add_behavior(BlockedByObjects())
        
    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]
        
        return None
    
    def set_property(self, key, value):
        self.properties[key] = value
        
    def collide(self, object1, object2):
        radius1 = max(object1.size)
        
        mypos = numpy.array(object1.position)
        otherpos = numpy.array(object2.position)
        
        distance = numpy.linalg.norm(mypos - otherpos)
        direction_vector = (mypos - otherpos) / distance
        
        max_direction = max(direction_vector, key = abs)
        
        indices = [i for i, j in enumerate(direction_vector) if j == max_direction]
        sizes = [object2.size[j] for i, j in enumerate(indices)]
        radius2 = max(sizes)
        
        return distance <  radius1 + radius2