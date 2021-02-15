import pygame
from pygame.locals import *

from OpenGL.GLU import *
from OpenGL.GL import *

from view_object import ViewObject

class CubeView(ViewObject):
    
     def cube(self):
        glColor(*self.game_object.color)
        glBegin(GL_QUADS)
        # Front face
        glNormal3f( 0.0, 0.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        # Left face
        glNormal3f( -1.0, 0.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        # Back face
        glNormal3f( 0.0, 0.0, -1.0)
        glVertex3d(-0.5, 0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, 0.5, -0.5)
        # Right face
        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, 0.5, -0.5)
        # Top face
        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        # Bottom face
        glNormal3f( 0.0, -1.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glEnd()
        
     def draw(self):
        self.cube()
        