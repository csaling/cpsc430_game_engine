from localize import Localize
from pubsub import pub

class GameObject:
    def __init__(self, id, data):
        self.properties = {}
        
        self.position = data['position']
        self.kind = data['kind']
        
        if 'size' not in data:
            self.size = [1.0, 1.0, 1.0]
        
        else:
            self.size = data['size']
                  
        if 'name' not in data:
            self.name = None
        
        else:
            self._name = data['name']
            
        if 'rotation' in data:
            game_object['rotation'] = (0, 0, 0)
                  
        if 'faces' in data:
            self.faces = data['faces']
            
        else:
            self.faces = {}
            
        if 'color' in data:
            self.color = data['color']
            
        else:
            self.color = (1, 0, 0, 1.0)
            
            
        if 'texture' in data:
            self.texture = data['texture']
            
        else:
            self.texture = None
            
            
        if 'invisible' in data:
            self.invisible = True
            
        else:
            self.invisible = False
            
        
        self.id = id
        
        self._x_rotation = 0
        self._y_rotation = 0
        self._z_rotation = 0
        
        self.clicks = 0
        
        self.behaviors = {}
        
        self.collisions = []
        self._moved = False
        self._highlight = False
        
        pub.subscribe(self.clicked, "clicked-" + str(id))
        
        if 'name' in data:
            pub.subscribe(self.clicked, "clicked-" + data['name'])
      
    def delete(self):
        from game_logic import GameLogic
        GameLogic.delete_object(self)
        pub.unsubscribe(self.clicked, "clicked-" + str(self.id))
        
        if self.name:
            pub.unsubscribe(self.clicked, "clicked-" + self.name)
            
        for behavior in self.behaviors:
            self.behaviors[behavior].delete()
      
    def add_behavior(self, behavior):
        self.behaviors[behavior.__class__.__name__] = behavior
        behavior.connect(self)
    
    @property
    def highlight(self):
        return self._highlight
    
    @property
    def name(self):
        return self._name
      
    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def moved(self):
        return self._moved
    
    @property
    def kind(self):
        return self._kind
    
    @kind.setter
    def kind(self, value):
        self._kind = value
        
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value):
        self._size = value
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
        
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = value
        
    @property
    def x_rotation(self):
        return self._x_rotation
    
    @x_rotation.setter
    def x_rotation(self, value):
        self._x_rotation = value
        
    @property
    def y_rotation(self):
        return self._y_rotation
    
    @y_rotation.setter
    def y_rotation(self, value):
        self._y_rotation = value
       
    @property
    def z_rotation(self):
        return self._z_rotation
    
    @z_rotation.setter
    def z_rotation(self, value):
        self._z_rotation = value
       
    def tick(self):
        from game_logic import GameLogic
        
        if GameLogic.get_property('pasued'):
            return
        
        self._moved = False
        self._highlight = False
        
        for behavior in self.behaviors:
            self.behaviors[behavior].tick()
            
        self.collisions = []
    
    def clicked(self, game_object):
        self.clicks += 1
        
        for behavior in self.behaviors:
            self.behaviors[behavior].clicked(game_object)
            
    def hover(self, game_object):
        for behavior in self.behaviors:
            self.behaviors[behavior].hover(game_object)
            
    def get_property(self, key, default = None):
        if key in self.properties:
            return self.properties[key]
        
        return default
    
    def set_property(self, key, value):
        self.properties[key] = value
        
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        