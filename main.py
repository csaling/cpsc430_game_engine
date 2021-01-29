from game_logic import GameLogic
from player_view import PlayerView
class Main:
    def go (self):
        self.game_logic.load_world()
        
        while True:
            for instance in self.instances:
                instance.tick()
                
            if self.game_logic.get_property("quit"):
                break
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self._y_rotation = 0
                    
            if key_cooldown == 0:
                keys = pygame.key.get_pressed()
            
            if keys[K_LCTRL] or keys[K_RCTRL]:
                if keys[K_LEFT]:
                    self._y_rotation = 1
                    ballRotation += 2.0
                    
                if keys[K_RIGHT]:
                    self._y_rotation = 1
                    ballRotation -= 2.0

            else:
                if keys[K_LEFT]:
                    x_translation -= 0.05
                    
                if keys[K_RIGHT]:
                    x_translation += 0.05
                
                if keys[K_UP]:
                    y_translation += 0.05
                    
                if keys[K_DOWN]:
                    y_translation -= 0.05
                
                if key_cooldown > 0:
                    key_cooldown -= 1
        
    def __init__ (self):
        self.instances = []
        
        # create instances
        self.game_logic = GameLogic()
        
        self.instances.append(self.game_logic)
        self.instances.append(PlayerView(self.game_logic))

if __name__ == '__main__':
    main = Main()
    
    main.go()