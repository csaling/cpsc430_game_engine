
class GameObject:
    def __init__(self, position, kind, id):
        self.position = position
        self.kind = kind
        self.id = id

    @property
    def kind(self):
        return self._kind
    
    @kind.setter
    def kind(self, value):
        self._kind = value
        
    @property
    def id(self):
        return self._id
    
    @kind.setter
    def id(self, value):
        self._id = value
        
    @property
    def position(self):
        return self._position
    
    @kind.setter
    def position(self, value):
        self._position = value
        
    def tick(self):
        pass
