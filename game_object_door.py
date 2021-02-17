from game_object import GameObject

class GameObjectDoor(GameObject):
    def __init__(self, position, size, kind, id):
        super(GameObjectDoor, self).__init__(position, size, kind, id)
        
        self.open = False
        self.open_position =  self.position[0] - 5
        self.closed_position =  self.position[0]
                
    def clicked(self):
        if self.open:
            self.open = False
            
        else:
            self.open = True
            
    def tick(self):
        if self.open:
            if self.open_position < self.position[0]:
                self.position[0] -= 0.1
        else:
            if self.closed_position > self.position[0]:
                self.position[0] += 0.1
            