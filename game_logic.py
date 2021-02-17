from pubsub import pub

import numpy

from game_object import GameObject
from game_object_rotating import GameObjectRotating
from game_object_player import Player

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
            
    def create_object(self, which, position, size, kind):
        if kind == 'dog':
            #GameObjectRotating
            obj = which(position, size, kind, self.next_id)
            
        elif kind == 'house':
            #GameObjectHouse
            obj = which(position, size, kind, self.next_id)
            
        else:
            #GameObject
            obj = which(position, size, kind, self.next_id)
        
        self.next_id += 1
        self.game_objects[obj.id] = obj
            
        pub.sendMessage('create', game_object = obj)
        return obj
        
    def load_world(self):
        self.create_object (GameObjectRotating, [2, -5, -25], [5.0, 5.0, 5.0], "dog")
        self.create_object (GameObject, [-2, -3, -28], [0.5, 0.5, 0.5], "ball")
        
        ground = self.create_object (GameObject, [0, -1, 0], [100.0, 1.0, 100.0], "cube")
        ground.color = (0, 0.9, 0.3)
                                                    #Coordinates      #Scale
        left_wall = self.create_object (GameObject, [-10, 4, -20], [0.5, 10.0, 10.0], "cube")
        left_wall.color = (0.6, 0.3, 0.3)
        
        right_wall = self.create_object (GameObject, [10, 4, -20], [0.5, 10.0, 10.0], "cube")
        right_wall.color = (0.6, 0.3, 0.3)
        
        back_wall = self.create_object (GameObject, [0, 4, -25], [20, 10.0, 0.5], "cube")
        back_wall.color = (0.6, 0.3, 0.3)
        
        roof = self.create_object (GameObject, [0, 9, -20], [20, 0.5, 10], "cube")
        roof.color = (0.6, 0.3, 0.3)
        
        floor = self.create_object (GameObject, [0, -0.5, -20], [20, 0.5, 10], "cube")
        floor.color = (1.0, 1.0, 0.0)
        
        front_left = self.create_object (GameObject, [-7, 4, -15], [6, 10.0, 0.5], "cube")
        front_left.color = (0.6, 0.3, 0.3)
        
        front_right = self.create_object (GameObject, [7, 4, -15], [6, 10.0, 0.5], "cube")
        front_right.color = (0.6, 0.3, 0.3)
        
        self.create_object (Player, [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], "player")
    
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