from behavior import Behavior
from pubsub import pub

class Spin(Behavior):
    def __init__(self, speed, rotation):
        super(Spin, self).__init__()
        
        self.speed = speed
        self.rotation = rotation
        
        pub.subscribe(self.arrowLeft, 'arrowLeft')
        pub.subscribe(self.arrowRight, 'arrowRight')
        
    def arrowLeft(self):
        self.game_object.y_rotation = self.rotation
        self.game_object.z_rotation += self.speed
      
    def arrowRight(self):
        self.game_object.y_rotation = self.rotation
        self.game_object.z_rotation -= self.speed
