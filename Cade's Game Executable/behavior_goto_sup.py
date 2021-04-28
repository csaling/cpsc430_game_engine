from behavior import Behavior
from game_logic import GameLogic
from pubsub import pub

import numpy

class GotoSupervisor(Behavior):
    def __init__(self, event, steps):
        super(GotoSupervisor, self).__init__()
        
        self.event = event
        self.steps = steps
        self.next_step = 0
        self.num_steps = len(self.steps)
        
        pub.subscribe(self.process_event, self.event)
        
    def delete(self):
        pub.unsubscribe(self.process_event, self.event)
        
    def process_event(self, game_object):
        
        pub.sendMessage(self.steps[self.next_step][0], game_object = self.game_object)
        
        if len(self.steps[self.next_step]) > 1:
            self.game_object.behaviors["Goto"].destination = self.steps[self.next_step][1]
            
        self.next_step += (self.next_step + 1) % self.num_steps            
