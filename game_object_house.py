from game_object import GameObject

class GameObjectHouse(GameObject):
    def __init__(self, position, kind, id):
        super(GameObjectHouse, self).__init__(position, kind, id)

        self.door_open = False
                
    def clicked(self):
        self.door_open = not self.door_open
        