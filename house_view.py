import pygame
from pygame.locals import *

from OpenGL.GLU import *
from OpenGL.GL import *

from view_object import ViewObject

class HouseView(ViewObject):
    def house(self):
        glBegin(GL_QUADS)
        #Floor
        glColor(1.0, 1.0, 0.0, 1.0)
        glVertex3f(-1,-1,-1)
        glVertex3f(1,-1,-1)
        glVertex3f(1,-1,1)
        glVertex3f(-1,-1,1)

        glEnd()
        
        glBegin(GL_QUADS)
        #Door
        glColor(0.5, 0.3, 0.2, 1.0)
        if self.game_object.door_open:
            glVertex3f(-1,-1,1)
            glVertex3f(-1,-1,3)
            glVertex3f(-1,1,3)
            glVertex3f(-1,1,1)
            
            
        else: 
            glVertex3f(-1,-1,1)
            glVertex3f(1,-1,1)
            glVertex3f(1,1,1)
            glVertex3f(-1,1,1)    

        glEnd()
        
        glBegin(GL_QUADS)
        
        #Ceiling
        glColor(1.0, 0.0, 0.0, 1.0)
        glVertex3f(-1,1,-1)
        glVertex3f(1,1,-1)
        glVertex3f(1,1,1)
        glVertex3f(-1,1,1)
        
        #Back
        glVertex3f(-1,-1,-1)
        glVertex3f(1,-1,-1)
        glVertex3f(1,1,-1)
        glVertex3f(-1,1,-1)

        #Right Side
        glVertex3f(1,1,1)
        glVertex3f(1,-1,1)
        glVertex3f(1,-1,-1)
        glVertex3f(1,1,-1)

        #Left Side
        glVertex3f(-1,1,1)
        glVertex3f(-1,-1,1)
        glVertex3f(-1,-1,-1)
        glVertex3f(-1,1,-1)
        
        glEnd()
        
    def draw(self):
        glPushMatrix()
        self.house()
        glPopMatrix()
