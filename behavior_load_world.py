from behavior import Behavior

class LoadWorld(Behavior):
    def __init__(self, world, name, position, rotation):
        super(LoadWorld, self).__init__()
        
        self.world = world
        self.position = position
        self.name = name
        self.rotation = rotation

    def clicked(self, game_object):
        from game_logic import GameLogic
        GameLogic.load_world(self.world)
        GameLogic.get_object(self.name).position = self.position
        GameLogic.get_object(self.name).x_rotation = self.rotation[0]
        GameLogic.get_object(self.name).y_rotation = self.rotation[1]
        GameLogic.get_object(self.name).z_rotation = self.rotation[2]
        
        #if self.world == "main_world.txt":
            #Check if ball is picked up:
            #GameLogic.load_world(self.world)
        