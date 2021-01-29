from OpenGL.GLU import *
from OpenGL.GL import *
from view_object import ViewObject

from PIL.Image import open

class DogView(ViewObject):
    
    def __init__(self, game_object):
        super(DogView, self).__init__(game_object)
        image = open('Dog Fur.JFIF')
    
        ix = image.size[0]
        iy = image.size[1]
        image = image.tobytes("raw", "RGB", 0, -1)
        
        self.fur_texture = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, self.fur_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)   
        
    def body(self):
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

    def triangle(self):
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
    
    def draw(self):
        glBindTexture(GL_TEXTURE_2D, self.fur_texture)
        glEnable(GL_TEXTURE_2D)
        
        #Body
        glPushMatrix()
        glTranslate(0.0, 0.0, -2.0)
        self.body()
        glPopMatrix()
        
        #Head
        glPushMatrix()
        glScale(0.5, 0.5, 0.5)
        glTranslate(-5.8, 0.25, -2.0)
        glRotatef(20,0,0,1)
        self.triangle()
        glPopMatrix()

        #Right Leg
        glPushMatrix()
        glScale(0.5, 0.5, 0.5)
        glTranslate(2.5, -2.0, -2.0)
        glRotatef(90,0,0,1)
        self.triangle()
        glPopMatrix()
        
        #Left Leg
        glPushMatrix()
        glScale(0.5, 0.5, 0.5)
        glTranslate(-2.5, -2.0, -2.0)
        glRotatef(90,0,0,1)
        self.triangle()
        glPopMatrix()
        
        #Tail
        glPushMatrix()
        glScale(0.2, 0.2, 0.2)
        glTranslate(8.5, 0.5, -2.0)
        glRotatef(60,0,0,1)
        self.triangle()
        glPopMatrix()
        
        #Ear
        glPushMatrix()
        glScale(0.25, 0.25, 0.25)
        glTranslate(-8.5, 2.75, -2.0)
        glRotatef(40,0,0,1)
        self.triangle()
        glPopMatrix()
