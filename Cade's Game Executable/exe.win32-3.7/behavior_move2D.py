from behavior import Behavior
from pubsub import pub

class Move2D(Behavior):
    def __init__(self, speed):
        super(Move2D, self).__init__()
        
        self.speed = speed
        
        pub.subscribe(self.ballLeft, 'ballLeft')
        pub.subscribe(self.ballRight, 'ballRight')
        pub.subscribe(self.ballUp, 'ballUp')
        pub.subscribe(self.ballDown, 'ballDown')
        
    def ballLeft(self):    
        self.game_object.position[0] -= self.speed
      
    def ballRight(self):
        self.game_object.position[0] += self.speed
        
    def ballUp(self):
        self.game_object.position[1] += self.speed
        
    def ballDown(self):
        self.game_object.position[1] -= self.speed
        
        