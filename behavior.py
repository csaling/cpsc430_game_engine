class Behavior:
    def _init_(self):
        self.game_object = None
        
    def connect(self, game_object):
        self.game_object = game_object
        
    def tick(self):
        pass
    
    def clicked(self):
        pass