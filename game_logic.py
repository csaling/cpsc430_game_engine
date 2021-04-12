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
    level_data = {}
    
    filename = None
    
    deletions = []
    additions = []
    
    next_id = 0
    
    @staticmethod
    def tick():
        GameLogic.world_world_loaded = False
        for game_object in GameLogic.game_objects:
            if GameLogic.game_objects[game_object].moved:
                for other in GameLogic.game_objects:
                    if GameLogic.collide(GameLogic.game_objects[game_object], GameLogic.game_objects[other]):
                        GameLogic.game_objects[game_object].collisions.append(GameLogic.game_objects[other])
                    
        for id in GameLogic.game_objects:
            GameLogic.game_objects[id].tick()
            if GameLogic.world_world_loaded:
                GameLogic.world_world_loaded = False
                break
            
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
        GameLogic.filename = filename
        GameLogic.world_world_loaded = True
        pub.sendMessage('view_objects')
        
        with open(filename) as infile:
            level_data = json.load(infile)
            GameLogic.level_data = level_data
            
            if not 'objects' in level_data:
                return False
            
            for game_object in level_data["objects"]:
                if game_object['kind'][0] == '#':
                    continue
                
                obj = GameLogic.create_object(game_object)
                
                if 'behaviors' not in game_object:
                    continue
                
                for behavior in game_object['behaviors']:
                    module = importlib.import_module(level_data['behaviors'][behavior])
                    class_ = getattr(module, behavior)
                    instance = class_(*game_object['behaviors'][behavior])
                    instance.arguments = game_object['behaviors'][behavior]
                    
                    obj.add_behavior(instance)
                    
            for file in level_data['files']:
                GameLogic.files[file] = level_data['files'][file]
                
            if 'level' in level_data:
                if 'music' in level_data['level']:
                    from sounds import Sounds
                    Sounds.play_music(*level_data['level']['music'])
                    
                if 'background' in level_data['level']:
                    GameLogic.set_property('background', level_data['level']['background'])
                    
    
    @staticmethod
    def save_world():
        if 'objects' in GameLogic.level_data:
            del GameLogic.level_data['objects']
            
        GameLogic.level_data['objects'] = []
        
        for game_object in GameLogic.game_objects:
            GameLogic.save_object(GameLogic.game_objects[game_object])
            
        with open(GameLogic.filename, 'w') as outfile:
            json.dump(GameLogic.level_data, outfile, sort_keys = False, indent = 4)
    
    @staticmethod
    def save_object(game_object):
        data = {}
        
        data['kind'] = game_object.kind
        data['position'] = game_object.position
        data['size'] = game_object.size
        
        if game_object.faces:
            data['faces'] = game_object.faces
        
        if game_object.name:
            data['name'] = game_object.name
        
        if game_object.color:
            data['color'] = game_object.color
            
        if game_object.texture:
            data['texture'] = game_object.texture
        
        data['behaviors'] = {}
        for behavior in game_object.behaviors:
            data['behaviors'][behavior] = game_object.behaviors[behavior].arguments
        
        GameLogic.level_data['objects'].append(data)
        
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
    
    