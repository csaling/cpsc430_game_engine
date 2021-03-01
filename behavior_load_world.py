from behavior import Behavior

class LoadWorld(Behavior):
    def __init__(self, world):
        super(LoadWorld, self).__init__()
        
        self.world = world

    def clicked(self):
        from game_logic import GameLogic
        GameLogic.load_world(self.world)
            