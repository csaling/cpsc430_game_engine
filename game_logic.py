from pubsub import pub
import importlib
import numpy
import json

from game_object import GameObject

class GameLogic:
    
    properties = {}
    game_objects = {}
    name_index = {}
    files = {}
    
    deletions = []
    additions = []
    
    next_id = 0
    
    @staticmethod
    def tick():
        for game_object in GameLogic.game_objects:
            if GameLogic.game_objects[game_object].moved:
                for other in GameLogic.game_objects:
                    if GameLogic.collide(GameLogic.game_objects[game_object], GameLogic.game_objects[other]):
                        GameLogic.game_objects[game_object].collisions.append(GameLogic.game_objects[other])
                    
        for id in GameLogic.game_objects:
            GameLogic.game_objects[id].tick()
            
        GameLogic.process_deletions()
        GameLogic.process_additions()
    
    @staticmethod
    def create_object(data):

        obj = GameObject(GameLogic.next_id, data)
       
        return GameLogic.register_object(obj)
       
    @staticmethod
    def register_object(obj):
        obj.id = GameLogic.next_id
        GameLogic.next_id += 1
        GameLogic.game_objects[obj.id] = obj
            
        if obj.name:
            GameLogic.name_index[obj.name] = obj
            
        pub.sendMessage('create', game_object = obj)
        return obj
    
    @staticmethod
    def delete_object(obj):
        GameLogic.deletions.append(obj)
        
    @staticmethod
    def process_deletions():
        for obj in GameLogic.deletions:
            if obj.name:
                del GameLogic.name_index[obj.name]
            del GameLogic.game_objects[obj.id]
            pub.sendMessage('delete', game_object = obj)
            
        GameLogic.deletions = []
        
    @staticmethod
    def add_object(obj):
        GameLogic.additions.append(obj)
        
    @staticmethod
    def process_additions():
        for obj in GameLogic.additions:
            GameLogic.register_object(obj)
            
        GameLogic.additions = []
        
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
        pub.sendMessage('view_objects')
        
        with open(filename) as infile:
            level_data = json.load(infile)
            
            if not 'objects' in level_data:
                return False
            
            for game_object in level_data["objects"]:
                if game_object['kind'][0] == '#':
                    continue
                
                if 'size' not in game_object:
                    game_object['size'] = [1.0, 1.0, 1.0]
                  
                if 'name' not in game_object:
                    game_object['name'] = None
                    
                if 'rotation' in game_object:
                    game_object['rotation'] = (0, 0, 0)
                  
                obj = GameLogic.create_object(game_object)
                
                if 'behaviors' not in game_object:
                    continue
                
                for behaviors in game_object['behaviors']:
                    module = importlib.import_module(level_data['behaviors'][behaviors])
                    class_ = getattr(module, behaviors)
                    instance = class_(*game_object['behaviors'][behaviors])
                    
                    obj.add_behavior(instance)
                    
            for file in level_data['files']:
                GameLogic.files[file] = level_data['files'][file]
                
            if 'level' in level_data:
                if 'music' in level_data['level']:
                    from sounds import Sounds
                    Sounds.play_music(*level_data['level']['music'])
    
    @staticmethod
    def get_property(key, default = None):
        if key in GameLogic.properties:
            return GameLogic.properties[key]
        
        return default
    
    @staticmethod
    def set_property(key, value):
        GameLogic.properties[key] = value
    
    @staticmethod
    def collide(object1, object2):
        if object1 == object2:
            return False
        minx1 = object1.position[0] - object1.size[0] / 2
        maxx1 = object1.position[0] + object1.size[0] / 2
        miny1 = object1.position[1] - object1.size[1] / 2
        maxy1 = object1.position[1] + object1.size[1] / 2
        minz1 = object1.position[2] - object1.size[2] / 2
        maxz1 = object1.position[2] + object1.size[2] / 2
        
        minx2 = object2.position[0] - object2.size[0] / 2
        maxx2 = object2.position[0] + object2.size[0] / 2
        miny2 = object2.position[1] - object2.size[1] / 2
        maxy2 = object2.position[1] + object2.size[1] / 2
        minz2 = object2.position[2] - object2.size[2] / 2
        maxz2 = object2.position[2] + object2.size[2] / 2
        
        return minx1 < maxx2 and minx2 < maxx1 and miny1 < maxy2 and miny2 < maxy1 and minz1 < maxz2 and minz2 < maxz1
    
    