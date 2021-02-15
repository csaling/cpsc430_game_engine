from game_object import GameObject

class GameObjectRotating(GameObject):
    def __init__(self, position, size, kind, id):
        super(GameObjectRotating, self).__init__(position, size, kind, id)
        
        self.allow_rotation = True
        self.new_rotation = -0.5
        
    def tick(self):
        #self.allow_rotation = False
        if self.allow_rotation:
            
            self.z_rotation += self.new_rotation
            if self.z_rotation <= -40:
                self.new_rotation = 0.5

            if self.z_rotation >= 0:
                self.new_rotation = -0.5
            
    def clicked(self):
        self.allow_rotation = not self.allow_rotation
         