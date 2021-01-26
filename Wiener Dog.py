import pygame
from pygame.locals import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from PIL.Image import open

rotation = 0.0
newRotation = -0.5
ballRotation = 0.0
x_translation = -3.0
y_translation = 0.0
y_rotation = 0.0

def main():
    global x_translation
    global y_translation
    global y_rotation
    global rotation
    global ballRotation
    
    key_cooldown = 10
    
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
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    y_rotation = 0
        
        if key_cooldown == 0:
            keys = pygame.key.get_pressed()
            
            if keys[K_LCTRL] or keys[K_RCTRL]:
                if keys[K_LEFT]:
                    y_rotation = 1
                    ballRotation += 2.0
                    
                if keys[K_RIGHT]:
                    y_rotation = 1
                    ballRotation -= 2.0

            else:
                if keys[K_LEFT]:
                    x_translation -= 0.05
                    
                if keys[K_RIGHT]:
                    x_translation += 0.05
                
                if keys[K_UP]:
                    y_translation += 0.05
                    
                if keys[K_DOWN]:
                    y_translation -= 0.05
                
        if key_cooldown > 0:
            key_cooldown -= 1
                
        display()
        
        pygame.display.flip()
        pygame.time.wait(10)

    return

def init ():
    image = open('Dog Fur.JFIF')
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGB", 0, -1)
    
    fur_texture = glGenTextures(1)
    
    glBindTexture(GL_TEXTURE_2D, fur_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glEnable(GL_TEXTURE_2D)
    
    light_ambient = [0.1, 0.1, 0.1, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_position = [0.0, 0.0, 1.0, 1.0]
    
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT1)
    
    glEnable(GL_COLOR_MATERIAL);
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
  
def body():
    glBegin(GL_QUADS)
    glColor(0.5, 0.5, 0.5, 1.0)
    glNormal3f(0.0, 0.0, 1.0)
    
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-2.0, 0.0, 1.0)
    
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-2.0, -1.0, 1.0)
    
    glTexCoord2f(1.0, 0.0)
    glVertex3d(2.0, -1.0, 1.0)
    
    glTexCoord2f(1.0, 1.0)
    glVertex3d(2.0, 0.0, 1.0)
    glEnd()

def triangle():
    glBegin(GL_TRIANGLES)
    glColor(0.5, 0.5, 0.5, 1.0)
    glNormal3f(0.0, 0.0, 1.0)
    
    glTexCoord2f(0.0, 1.0)    
    glTexCoord2f(0.0, 0.0)
    glVertex3d(2.0, 1.0, 1.0)
    
    glTexCoord2f(1.0, 0.0)
    glVertex3d(2.0, -1.0, 1.0)
    
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-1.5, 0.0, 1.0)
    glEnd()
    
def ball():
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

def display():
    global rotation
    global newRotation
    global y_translation
    
    glPushMatrix()
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    glPushMatrix()
    glTranslate(x_translation, y_translation, 0.0)
    glScale(0.5, 0.5, 0.5)
    glRotatef(ballRotation,0,0,1)
    ball()
    glPopMatrix()
    
    glRotatef(rotation,0,0,1)
    rotation += newRotation

    if rotation <= -40:
        newRotation = 0.5

    if rotation >= 0:
        newRotation = -0.5

    glPushMatrix()
    # Push the body into the screen a bit 
    glTranslate(0.0, 0.0, -2.0)
    body()
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


