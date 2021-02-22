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
        self.ball.y_rotation = rotation
        self.ball.z_rotation += speed
      
    def arrowRight(self):
        self.ball.y_rotation = rotation
        self.ball.z_rotation -= speed
