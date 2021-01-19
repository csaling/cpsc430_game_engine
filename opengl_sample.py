import pygame
from pygame.locals import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from PIL.Image import open

rotation = 0.0

def main():
    pygame.init()
    windowSize = (800,600)
    pygame.display.set_mode(windowSize, DOUBLEBUF|OPENGL)
    
    gluPerspective(60, (windowSize[0]/windowSize[1]), 0.1, 100.0)

    glTranslatef(0.0, 0.0, -5)

    init ()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        display()
        
        pygame.display.flip()
        pygame.time.wait(10)

    return

def init ():
    glEnable(GL_COLOR_MATERIAL);
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    
def cube():
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

def display():
    global rotation
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    
    # Push the cube into the screen a bit 
    glTranslate(0.0, 0.0, -2.0)
    
    glRotatef(rotation,1,1,1)
    rotation -= 0.5
    
    cube()

    glPopMatrix()
    
    return

if __name__ == '__main__':
    main()




