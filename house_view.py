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
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(0.5,-0.5,-0.5)
        glVertex3f(0.5,-0.5,0.5)
        glVertex3f(-0.5,-0.5,0.5)

        glEnd()
        
        glBegin(GL_QUADS)
        #Door
        glColor(0.5, 0.3, 0.2, 1.0)
        if self.game_object.door_open:
            glVertex3f(-0.5,-0.5,0.5)
            glVertex3f(-0.5,-0.5,1.5)
            glVertex3f(-0.5,0.5,1.5)
            glVertex3f(-0.5,0.5,0.5)
            
            
        else: 
            glVertex3f(-0.5,-0.5,0.5)
            glVertex3f(0.5,-0.5,0.5)
            glVertex3f(0.5,0.5,0.5)
            glVertex3f(-0.5,0.5,0.5)    

        glEnd()
        
        glBegin(GL_QUADS)
        
        #Ceiling
        glColor(1.0, 0.0, 0.0, 1.0)
        glVertex3f(-0.5,0.5,-0.5)
        glVertex3f(0.5,0.5,-0.5)
        glVertex3f(0.5,0.5,0.5)
        glVertex3f(-0.5,0.5,0.5)
        
        #Back
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(0.5,-0.5,-0.5)
        glVertex3f(0.5,0.5,-0.5)
        glVertex3f(-0.5,0.5,-0.5)

        #Right Side
        glVertex3f(0.5,0.5,0.5)
        glVertex3f(0.5,-0.5,0.5)
        glVertex3f(0.5,-0.5,-0.5)
        glVertex3f(0.5,0.5,-0.5)

        #Left Side
        glVertex3f(-0.5,0.5,0.5)
        glVertex3f(-0.5,-0.5,0.5)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5,0.5,-0.5)
        
        glEnd()
        
    def draw(self):
        glPushMatrix()
        self.house()
        glPopMatrix()
