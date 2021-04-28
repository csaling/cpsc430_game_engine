from game_logic import GameLogic
from player_view_editor import PlayerView
from movies import Movies
from sounds import Sounds

class Main:
    def go (self):
        GameLogic.load_world("final_world - Copy.txt")
        
        while True:
            GameLogic.tick()
            Sounds.tick()
            Movies.tick()
            
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
