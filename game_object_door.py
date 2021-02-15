from game_object import GameObject

class GameObjectDoor(GameObject):
    def __init__(self, position, size, kind, id):
        super(GameObjecDoor, self).__init__(position, size, kind, id)

        self.door_open = False
                
    def clicked(self):
        self.door_open = not self.door_open