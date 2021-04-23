from behavior import Behavior
from pubsub import pub

class TimedMessage(Behavior):
    def __init__(self, time, message):
        super(TimedMessage, self).__init__()
        
        self.time = time
        self.message = message
        self.ticks_passed = 0
 
    def tick(self):
        self.ticks_passed += 1
        
        if self.ticks_passed >= self.time:
            pub.sendMessage(self.message, game_object = self.game_object)
