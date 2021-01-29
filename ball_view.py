from OpenGL.GLU import *
from OpenGL.GL import *
from view_object import ViewObject

class BallView(ViewObject):
    def ball(self):
        glBegin(GL_QUADS)
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
    
    def draw(self):
        glPushMatrix()
        glScale(0.5, 0.5, 0.5)
        self.ball()
        glPopMatrix()
