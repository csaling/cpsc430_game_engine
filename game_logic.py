from pubsub import pub
import importlib
import numpy
import json

from game_object import GameObject

"""
from game_object import GameObject
from game_object_player import Player
from behavior_bouncing import Bouncing
from behavior_key_move import KeyMove
from behavior_mouse_rotation import MouseRotation
from behavior_collision import BlockedByObjects
from behavior_slide import Slide
from behavior_spin import Spin
from behavior_move2D import Move2D
from behavior_teleport import Teleport

"""

class GameLogic:
    
    properties = {}
    game_objects = {}
    name_index = {}
    
    next_id = 0
    
    @staticmethod
    def tick():
        for game_object in GameLogic.game_objects:
            if GameLogic.game_objects[game_object].moved:
                for other in GameLogic.game_objects:
                    if GameLogic.game_objects[game_object] == GameLogic.game_objects[other]:
                        continue
                    
                    if GameLogic.collide(GameLogic.game_objects[game_object], GameLogic.game_objects[other]):
                        GameLogic.game_objects[game_object].collisions.append(GameLogic.game_objects[other])
                    
        for id in GameLogic.game_objects:
            GameLogic.game_objects[id].tick()
    
    @staticmethod
    def create_object(name, position, size, color, kind):

        obj = GameObject(position, size, color, kind, GameLogic.next_id, name)
        
        GameLogic.next_id += 1
        GameLogic.game_objects[obj.id] = obj
            
        if name:
            GameLogic.name_index[name] = obj
            
        pub.sendMessage('create', game_object = obj)
        return obj
        
    @staticmethod
    def get_object(id):
        result = None
        
        if id in GameLogic.name_index:
            result = GameLogic.name_index[id]
            
        if id in GameLogic.game_objects:
            result = GameLogic.game_objects[id]
            
        return result
        
        
    @staticmethod
    def load_world(filename):
        
        GameLogic.game_objects = {}
        GameLogic.name_index = {}
        
        with open(filename) as infile:
            level_data = json.load(infile)
            
            if not 'objects' in level_data:
                return False
            
            for game_object in level_data["objects"]:
                size = [1.0, 1.0, 1.0]
                if 'size' in game_object:
                    size = game_object['size']
                  
                name = None
                color = (1, 1, 1, 1)
                if 'name' in game_object:
                    name = game_object['name']
                    
                if 'color' in game_object:
                    color = game_object['color']
                  
                obj = GameLogic.create_object(name, game_object['position'], size, color, game_object['kind'])
                
                if 'behaviors' not in game_object:
                    continue
                
                for behaviors in game_object['behaviors']:
                    module = importlib.import_module(level_data['behaviors'][behaviors])
                    class_ = getattr(module, behaviors)
                    instance = class_(*game_object['behaviors'][behaviors])
                    
                    obj.add_behavior(instance)
                    
        """
        player = GameLogic.create_object ([0, 0, 0], [1.0, 1.0, 1.0], "player")
        player.add_behavior(KeyMove(0.1))
        player.add_behavior(MouseRotation(0.1))
        player.add_behavior(BlockedByObjects())
    
        dog = GameLogic.create_object ([0, -0.5, -2], [1.0, 1.0, 1.0], "dog")
        dog.add_behavior(Bouncing(False, -0.5, 0, -40))
        dog.add_behavior(Teleport(player, 10, 9.5))
        
        ball = GameLogic.create_object ([-1, 1, -22.5], [0.5, 0.5, 0.5], "ball")
        ball.add_behavior(Spin(2.0, 1))
        ball.add_behavior(Move2D(0.1))
        
        ground = GameLogic.create_object ([0, -1, 0], [100.0, 1.0, 100.0], "cube")
        ground.color = (0, 0.9, 0.3)
                                                    #Coordinates      #Scale
        left_wall = GameLogic.create_object ([-9.75, 4, -20], [0.5, 10.0, 10.0], "cube")
        left_wall.color = (0.6, 0.3, 0.3)
        
        right_wall = GameLogic.create_object ([9.75, 4, -20], [0.5, 10.0, 10.0], "cube")
        right_wall.color = (0.6, 0.3, 0.3)
        
        back_wall = GameLogic.create_object ([0, 4, -25], [20, 10.0, 0.5], "cube")
        back_wall.color = (0.6, 0.3, 0.3)
        
        roof = GameLogic.create_object ([0, 9, -20], [20, 0.5, 10], "cube")
        roof.color = (0.6, 0.3, 0.3)
        
        floor = GameLogic.create_object ([0, -0.5, -19.8], [19, 0.5, 10], "cube")
        floor.color = (1.0, 1.0, 0.0)
        
        front_left = GameLogic.create_object ([-6.5, 4, -15], [7, 10.0, 0.5], "cube")
        front_left.color = (0.6, 0.3, 0.3)
        
        front_right = GameLogic.create_object ([6.5, 4, -15], [7, 10.0, 0.5], "cube")
        front_right.color = (0.6, 0.3, 0.3)
        
        door = GameLogic.create_object ([0, 4, -15], [6, 10.0, 0.5], "door")
        door.color = (1.0, 0.0, 0.0)
        door.add_behavior(Slide(player, False, 0.1, 10, 5))
    """
    
    @staticmethod
    def get_property(key):
        if key in GameLogic.properties:
            return GameLogic.properties[key]
        
        return None
    
    @staticmethod
    def set_property(key, value):
        GameLogic.properties[key] = value
    
    @staticmethod
    def collide(object1, object2):
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