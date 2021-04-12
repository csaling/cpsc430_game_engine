from behavior import Behavior

class FallTeleport(Behavior):
    def __init__(self, world, name):
        super(FallTeleport, self).__init__()
        
        self.world = world
        self.name = name
    
    def tick(self):
        from game_logic import GameLogic
        if GameLogic.get_object(self.name).position[1] < -10:
            GameLogic.load_world(self.world)
