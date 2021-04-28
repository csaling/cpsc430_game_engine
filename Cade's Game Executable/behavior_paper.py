from behavior import Behavior
from localize import *
from localize import _
from pubsub import pub

class Paper(Behavior):
    def __init__(self, tag, timer):
        super(Paper, self).__init__()
        
        self.tag = tag
        self.timer = timer
        self.hide_text = False
        
    def clicked(self, game_object):
        if self.hide_text == False:
            pub.sendMessage('display_note', tag = self.tag, timer = self.timer)
            self.hide_text = True
            
        elif self.hide_text == True:
            pub.sendMessage('hide_note')
            self.hide_text = False
        

