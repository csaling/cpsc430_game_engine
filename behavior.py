class Behavior:
    def _init_(self):
        self.game_object = None
        
    def connect(self, game_object):
        self.game_object = game_object
        
    def tick(self):
        pass
    
    def clicked(self, game_object):
        pass
    
    def hover(self, game_object):
        pass
    
    def delete(self):
        pass