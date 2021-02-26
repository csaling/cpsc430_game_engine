from game_logic import GameLogic
from player_view import PlayerView
class Main:
    def go (self):
        GameLogic.load_world("level1.txt")
        #GameLogic.load_world("level2.txt")
        
        while True:
            GameLogic.tick()
            
            for instance in self.instances:
                instance.tick()
                
            if GameLogic.get_property("quit"):
                break
        
    def __init__ (self):
        self.instances = []
        
        self.instances.append(PlayerView())

if __name__ == '__main__':
    main = Main()
    
    main.go()