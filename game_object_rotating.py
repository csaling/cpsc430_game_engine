from game_object import GameObject

class GameObjectRotating(GameObject):
    def __init__(self, position, kind, id):
        super(GameObjectRotating, self).__init__(position, kind, id)
        
        self.allow_rotation = True
        self.new_rotation = -0.5
        self.ball_rotation = 0.0
        
    def tick(self):
        if self.allow_rotation:
            
            self.z_rotation += self.new_rotation
            if self.z_rotation <= -40:
                self.new_rotation = 0.5

            if self.z_rotation >= 0:
                self.new_rotation = -0.5
            
    def clicked(self):
        self.allow_rotation = not self.allow_rotation
         