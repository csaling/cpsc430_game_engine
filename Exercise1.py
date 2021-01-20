import pygame
from pygame.locals import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from PIL.Image import open

#Tried changing this and it did not seem to change speed/direction
rotation = 0.0
newRotation = -0.5

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
    glColor(0.65,0.16,0.16, 1)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3d(-2.0, 0.0, 1.0)
    glVertex3d(-2.0, -1.0, 1.0)
    glVertex3d(2.0, -1.0, 1.0)
    glVertex3d(2.0, 0.0, 1.0)
    glEnd()

def triangle():
    glBegin(GL_TRIANGLES)
    # Front face
    glColor(0.65,0.16,0.16, 1)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3d(2.0, 1.0, 1.0)
    glVertex3d(2.0, -1.0, 1.0)
    glVertex3d(-1.5, 0.0, 1.0)
    glEnd()

def display():
    global rotation
    global newRotation
    
    glPushMatrix()
    
    #Not working as I want it to
    #If I add 0.0 manually it does not seem to do anything
    glRotatef(rotation,0,0,1)
    rotation += newRotation
    
    if rotation <= -40:
        newRotation = 0.5

    if rotation >= 0:
        newRotation = -0.5
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    # Push the cube into the screen a bit 
    glTranslate(0.0, 0.0, -2.0)
    cube()
    glPopMatrix()
    
    glPushMatrix()
    glScale(0.5, 0.5, 0.5)
    glTranslate(-5.8, 0.25, -2.0)
    glRotatef(20,0,0,1)
    triangle()
    glPopMatrix()

    glPushMatrix()
    glScale(0.5, 0.5, 0.5)
    glTranslate(2.5, -2.0, -2.0)
    glRotatef(90,0,0,1)
    triangle()
    glPopMatrix()
    
    glPushMatrix()
    glScale(0.5, 0.5, 0.5)
    glTranslate(-2.5, -2.0, -2.0)
    glRotatef(90,0,0,1)
    triangle()
    glPopMatrix()
    
    glPushMatrix()
    glScale(0.2, 0.2, 0.2)
    glTranslate(8.9, 0.5, -2.0)
    glRotatef(60,0,0,1)
    triangle()
    glPopMatrix()
    
    glPushMatrix()
    glScale(0.25, 0.25, 0.25)
    glTranslate(-8.5, 2.75, -2.0)
    glRotatef(40,0,0,1)
    triangle()
    glPopMatrix()
    
    glPopMatrix()
    
    return

if __name__ == '__main__':
    main()


