import pygame
from pygame.locals import *

from OpenGL.GLU import *
from OpenGL.GL import *

from view_object import ViewObject

from PIL.Image import open

from localize import _

class BallView(ViewObject):
    
    def __init__(self, game_object):
        super(BallView, self).__init__(game_object)
        self.quadric = gluNewQuadric()
    
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glColor(*self.game_object.color)
        gluSphere(self.quadric , .5 , 36 , 18)
        glDisable(GL_TEXTURE_2D)
