from OpenGL.GLU import *
from OpenGL.GL import *
from view_object import ViewObject

from PIL.Image import open

from view_object import ViewObject

class CubeView(ViewObject):
    
     def cube(self):
        glTranslate(3, -3, -29.5)
        glScale(0.5, 0.5, 0.5)
        glBegin(GL_QUADS)
        # Front face
        glColor(1.0, 0.0, 0.0, 1.0)
        glNormal3f( 0.0, 0.0, 1.0)
        glVertex3d(-1.0, 1.0, 1.0)
        glVertex3d(-1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, 1.0)
        glVertex3d(1.0, 1.0, 1.0)
        # Left face
        glColor(0.0, 1.0, 0.0, 1.0)
        glNormal3f( -1.0, 0.0, 0.0)
        glVertex3d(-1.0, 1.0, 1.0)
        glVertex3d(-1.0, -1.0, 1.0)
        glVertex3d(-1.0, -1.0, -1.0)
        glVertex3d(-1.0, 1.0, -1.0)
        # Back face
        glColor(0.0, 0.0, 1.0, 1.0)
        glNormal3f( 0.0, 0.0, -1.0)
        glVertex3d(-1.0, 1.0, -1.0)
        glVertex3d(-1.0, -1.0, -1.0)
        glVertex3d(1.0, -1.0, -1.0)
        glVertex3d(1.0, 1.0, -1.0)
        # Right face
        glColor(1.0, 1.0, 0.0, 1.0)
        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3d(1.0, 1.0, 1.0)
        glVertex3d(1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, -1.0)
        glVertex3d(1.0, 1.0, -1.0)
        # Top face
        glColor(0.0, 1.0, 1.0, 1.0)
        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3d(-1.0, 1.0, 1.0)
        glVertex3d(1.0, 1.0, 1.0)
        glVertex3d(1.0, 1.0, -1.0)
        glVertex3d(-1.0, 1.0, -1.0)
        # Bottom face
        glColor(1.0, 1.0, 1.0, 1.0)
        glNormal3f( 0.0, -1.0, 0.0)
        glVertex3d(-1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, -1.0)
        glVertex3d(-1.0, -1.0, -1.0)
        glEnd()
    
    def draw(self):
        
        self.Cube()