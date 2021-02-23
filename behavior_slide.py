from behavior import Behavior

class Slide(Behavior):
    def __init__(self, open, speed, door_length):
        super(Slide, self).__init__()
        
        self.open = open
        self.speed = speed
        self.door_length = door_length
        
    def connect(self, game_object):
        super(Slide, self).connect(game_object)
        self.open_position = self.game_object.position[0] - self.door_length
        self.closed_position = self.game_object.position[0]
                
    def clicked(self):
        if self.open:
            self.open = False
            
        else:
            self.open = True
            
    def tick(self):
        if self.open:
            if self.open_position < self.game_object.position[0]:
                self.game_object.position[0] -= self.speed
        else:
            if self.closed_position > self.game_object.position[0]:
                self.game_object.position[0] += self.speed
            