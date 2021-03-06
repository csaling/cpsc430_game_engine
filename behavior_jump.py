from behavior import Behavior
from pubsub import pub

class Jump(Behavior):
    def __init__(self, speed, adjust, event):
        super(Jump, self).__init__()
        
        self.speed = speed
        self.adjust = adjust
        self.current = self.speed
        self.event = event
        self.jump_counter = 0
        
        self.jumping = False
        
        pub.subscribe(self.jump, self.event)
        
    def delete(self):
        pub.unsubscribe(self.jump, self.event)
        
    def jump(self):
        #Remove if not statement for infinite jumping
        if not self.game_object.get_property("falling"):
            self.jumping = True
        
    def tick(self):
        if not self.jumping:
            return
        
        if self.current <= 0.0:
            self.jumping = False
            self.current = self.speed
            return
        
        self.game_object.set_property('y_velocity', self.game_object.get_property('y_velocity', 0.0) + self.current)
        self.game_object.position[1] += self.current
        self.game_object._moved = True
        self.current -= self.adjust
