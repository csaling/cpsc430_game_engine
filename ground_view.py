import pygame
from pygame.locals import *

from OpenGL.GLU import *
from OpenGL.GL import *

from view_object import ViewObject

class GroundView(ViewObject):
    def ground(self):
        glBegin(GL_QUADS)
        #Floor
        glVertex3f(-1,-1,-1);
        glVertex3f(1,-1,-1);
        glVertex3f(1,-1,1);
        glVertex3f(-1,-1,1);

        #Ceiling
        glVertex3f(-1,1,-1);
        glVertex3f(1,1,-1);
        glVertex3f(1,1,1);
        glVertex3f(-1,1,1);
        #Walls
        glVertex3f(-1,-1,1);
        glVertex3f(1,-1,1);
        glVertex3f(1,1,1);
        glVertex3f(-1,1,1);

        glVertex3f(-1,-1,-1);
        glVertex3f(1,-1,-1);
        glVertex3f(1,1,-1);
        glVertex3f(-1,1,-1);

        glVertex3f(1,1,1);
        glVertex3f(1,-1,1);
        glVertex3f(1,-1,-1);
        glVertex3f(1,1,-1);

        glVertex3f(-1,1,1);
        glVertex3f(-1,-1,1);
        glVertex3f(-1,-1,-1);
        glVertex3f(-1,1,-1);
        
        glEnd()
        
    def draw(self):
        glPushMatrix()
        glScale(100.0, 0.0, 100.0)
        glColor(0.0, 1.0, 0.0, 1.0)
        self.ground()
        glPopMatrix()