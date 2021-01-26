from OpenGL.GLU import *
from OpenGL.GL import *

class ViewObject:
    def __init__(self, game_object):
        self.game_object = game_object
        
    def display(self):
        glPushMatrix()
        
        glTranslate(*self.game_object.position)
        
        self.draw()
        
        glPopMatrix()
    
    def draw(self):
        pass