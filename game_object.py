from localize import Localize

class GameObject:
    def __init__(self, name, position, rotation, size, color, kind, id):
        self.properties = {}
        
        self.position = position
        self._name = name
        self.kind = kind
        self.size = size
        self.id = id
        self._x_rotation = rotation[0]
        self._y_rotation = rotation[1]
        self._z_rotation = rotation[2]
        self.clicks = 0
        self.color = color
        
        self.behaviors = []
        
        self.collisions = []
        self._moved = False
      
    def add_behavior(self, behavior):
        self.behaviors.append(behavior)
        behavior.connect(self)
      
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
        self._moved = False
        
        for behavior in self.behaviors:
            behavior.tick()
            
        self.collisions = []
    
    def clicked(self, game_object):
        self.clicks += 1
        
        for behavior in self.behaviors:
            behavior.clicked(game_object)
        
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
        