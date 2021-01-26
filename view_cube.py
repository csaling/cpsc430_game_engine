from OpenGL.GLU import *
from OpenGL.GL import *
from view_object import ViewObject

class CubeView(ViewObject):
    def draw(self):
        glBegin(GL_QUADS)
        # Front face
        glColor(1.0, 0.0, 0.0, 1.0)
        glNormal3f( 0.0, 0.0, 1.0)
        
        glVertex3d(-0.75, 1.0, 1.0)
        glVertex3d(-1.0, 0.5, 1.0)
        glVertex3d(0.25, 0.5, 1.0)
        glVertex3d(0.0, 1.0, 1.0)
        
        glVertex3d(-0.75, 0.0, 1.0)
        glVertex3d(-1.0, 0.5, 1.0)
        glVertex3d(0.25, 0.5, 1.0)
        glVertex3d(0.0, 0.0, 1.0)
        glEnd()
