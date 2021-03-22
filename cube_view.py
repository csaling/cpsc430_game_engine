import pygame
from pygame.locals import *

from OpenGL.GLU import *
from OpenGL.GL import *

from view_object import ViewObject
from textures import Textures

class CubeView(ViewObject):
    
     def draw(self):
        self.cube()
    
     def get_color(self, face):
         
         if face in self.game_object.faces:
             if self.game_object.faces[face]['type'] == 'color':
                 return self.game_object.faces[face]['value']
                
         return self.game_object.color
    
     def get_texture(self, face):
         
         if face in self.game_object.faces:
             if self.game_object.faces[face]['type'] == 'texture':
                 Textures.activate_texture(self.game_object.faces[face]['value'])
                 return
                
         Textures.activate_texture(self.game_object.texture)
        
     def cube(self):
         
        # Back face
        self.get_texture("back")
        glBegin(GL_QUADS)
        glColor(*self.get_color("back"))
        glNormal3f( 0.0, 0.0, 1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.5, 0.5, 0.5)
        glEnd()
        Textures.deactivate_texture()
        
        # Left face
        self.get_texture("left")
        glBegin(GL_QUADS)
        glColor(*self.get_color("left"))
        glNormal3f( -1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()
        
        # Front face
        self.get_texture("front")
        glBegin(GL_QUADS)
        glColor(*self.get_color("front"))
        glNormal3f( 0.0, 0.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5, 0.5, -0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()
        
        # Right face
        self.get_texture("right")
        glBegin(GL_QUADS)
        glColor(*self.get_color("right"))
        glNormal3f( 1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()
        
        # Top face
        self.get_texture("top")
        glBegin(GL_QUADS)
        glColor(*self.get_color("top"))
        glNormal3f( 0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()
        
        # Bottom face
        self.get_texture("bottom")
        glBegin(GL_QUADS)
        glColor(*self.get_color("bottom"))
        glNormal3f( 0.0, -1.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5, -0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()
        