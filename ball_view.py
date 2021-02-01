import pygame
from pygame.locals import *

from OpenGL.GLU import *
from OpenGL.GL import *

from view_object import ViewObject

from PIL.Image import open

class BallView(ViewObject):
    
    def __init__(self, game_object):
        super(BallView, self).__init__(game_object)
        
        img = pygame.font.SysFont('Arial', 50).render("Red Ball", True, (255, 255, 255), (0, 0, 0))
        #image = open('Dog Fur.JFIF')
    
        #w = image.size[0]
        #h = image.size[1]
        #data = image.tobytes("raw", "RGB", 0, -1)
        
        w, h = img.get_size()
        data = pygame.image.tostring(img, "RGBA", 1)
        self.top_texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glPixelStorei(GL_UNPACK_ROW_LENGTH, w)
        glPixelStorei(GL_UNPACK_SKIP_ROWS, h//2)
        glBindTexture(GL_TEXTURE_2D, self.top_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h/2, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
        self.bottom_texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glPixelStorei(GL_UNPACK_ROW_LENGTH, w)
        glPixelStorei(GL_UNPACK_SKIP_ROWS, 0)
        glBindTexture(GL_TEXTURE_2D, self.bottom_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h/2, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
    def ball(self):
        glBindTexture(GL_TEXTURE_2D, self.top_texture)
        glBegin(GL_QUADS)
        glColor(0.5, 0.5, 0.5, 1.0)
        glNormal3f( 0.0, 0.0, 1.0)
        
        #Top Half
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.75, 1.0, 1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-1.0, 0.5, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.25, 0.5, 1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.0, 1.0, 1.0)
        glEnd()
        
        #Bottom Half
        glBindTexture(GL_TEXTURE_2D, self.bottom_texture)
        glBegin(GL_QUADS)
        glColor(0.5, 0.5, 0.5, 1.0)
        glNormal3f( 0.0, 0.0, 1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.75, 0.0, 1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-1.0, 0.5, 1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.25, 0.5, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.0, 0.0, 1.0)
        glEnd()
    
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glPushMatrix()
        glScale(1.0, 1.25, 1.0)
        self.ball()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
