from pubsub import pub

from game_object import GameObject

from game_object_rotating import GameObjectRotating

from game_object_house import GameObjectHouse

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}
        
        self.next_id = 0
    
    def tick(self):
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
        self.create_object (GameObjectRotating, [3, -3, -30], [1.0, 1.0, 1.0], "dog")
        self.create_object (GameObject, [-2, -3, -30], [0.25, 0.25, 0.25], "ball")
        #self.create_object (GameObjectHouse, [0, 0, -30], [5.0, 5.0, 5.0], "house")
        self.create_object (GameObject, [0, -10, 0], [10.0, 10.0, 10.0], "ground")
    
    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]
        
        return None
    
    def set_property(self, key, value):
        self.properties[key] = value