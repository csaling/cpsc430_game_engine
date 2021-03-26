from OpenGL.GLU import *
from OpenGL.GL import *

from view_object import ViewObject

class BallView(ViewObject):
    
    def __init__(self, game_object):
        super(BallView, self).__init__(game_object)
        self.quadric = gluNewQuadric()
        
    def get_color(self):
         if self.game_object.get_property('highlight_color') and self.game_object.highlight:
             return self.game_object.get_property('highlight_color')
            
         return self.game_object.color
    
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glColor(*self.get_color())
        gluSphere(self.quadric , .5 , 36 , 18)
        glDisable(GL_TEXTURE_2D)
