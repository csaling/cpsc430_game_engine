from OpenGL.GLU import *
from OpenGL.GL import *
from view_object import ViewObject

from PIL.Image import open

from textures import Textures

class DogView(ViewObject):
        
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
         
    def rectangle(self):
        
    #Left Side
        self.get_texture("left")
        glBegin(GL_QUADS)
        glColor(*self.get_color("left"))
        glNormal3f(0.0, 0.0, 0.0)
        #Top Left
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2.0, 0.0, 1.0)
        
        #Bottom Left
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-2.0, -1.0, 1.0)
        
        #Bottom Right 
        glTexCoord2f(1.0, 0.0)
        glVertex3d(2.0, -1.0, 1.0)
        
        #Top Right
        glTexCoord2f(1.0, 1.0)
        glVertex3d(2.0, 0.0, 1.0)
        glEnd()
        Textures.deactivate_texture()
        
    #Right Side
        self.get_texture("right")
        glBegin(GL_QUADS)
        glColor(*self.get_color("right"))
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2.0, 0.0, 0.0)
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-2.0, -1.0, 0.0)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3d(2.0, -1.0, 0.0)
        
        glTexCoord2f(1.0, 1.0)
        glVertex3d(2.0, 0.0, 0.0)
        glEnd()
        Textures.deactivate_texture()
        
        
    #Top
        self.get_texture("top")
        glBegin(GL_QUADS)
        glColor(*self.get_color("top"))
        #Top Left
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2.0, 0.0, 0.0)
        
        #Bottom Left
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-2.0, 0.0, 1.0)
        
        #Bottom Right 
        glTexCoord2f(1.0, 0.0)
        glVertex3d(2.0, 0.0, 1.0)
        
        #Top Right
        glTexCoord2f(1.0, 1.0)
        glVertex3d(2.0, 0.0, 0.0)
        glEnd()
        Textures.deactivate_texture()
        
    #Bottom
        self.get_texture("bottom")
        glBegin(GL_QUADS)
        glColor(*self.get_color("bottom"))
        #Top Left
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2.0, -1.0, 0.0)
        
        #Bottom Left
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-2.0, -1.0, 1.0)
        
        #Bottom Right 
        glTexCoord2f(1.0, 0.0)
        glVertex3d(2.0, -1.0, 1.0)
        
        #Top Right
        glTexCoord2f(1.0, 1.0)
        glVertex3d(2.0, -1.0, 0.0)
        glEnd()
        Textures.deactivate_texture()
        
    #Chest
        self.get_texture("chest")
        glBegin(GL_QUADS)
        glColor(*self.get_color("chest"))
        #Chest Top Left
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2.0, 0.0, 1.0)
        
        #Chest Bottom Left
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-2.0, -1.0, 1.0)
        
        #Chest Bottom Right 
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-2.0, -1.0, 0.0)
        
        #Chest Top Right
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-2.0, 0.0, 0.0)
        glEnd()
        Textures.deactivate_texture()
        
    #Butt
        self.get_texture("butt")
        glBegin(GL_QUADS)
        glColor(*self.get_color("butt"))
        #Butt Top Left
        glTexCoord2f(0.0, 1.0)
        glVertex3d(2.0, 0.0, 1.0)
        
        #Butt Bottom Left
        glTexCoord2f(0.0, 0.0)
        glVertex3d(2.0, -1.0, 1.0)
        
        #Butt Bottom Right 
        glTexCoord2f(1.0, 0.0)
        glVertex3d(2.0, -1.0, 0.0)
        
        #Butt Top Right
        glTexCoord2f(1.0, 1.0)
        glVertex3d(2.0, 0.0, 0.0)
        glEnd()
        Textures.deactivate_texture()
        
    def leash(self):
        glBegin(GL_QUADS)
        glColor(0.7, 0.4, 0.0, 1.0)
        glNormal3f(0.0, 0.0, 1.0)
        
        #Top Left
        glVertex3d(-0.15, 0.50, -0.35)
        
        #Bottom Left
        glVertex3d(-0.15, 0.50, -0.45)
        
        #Bottom Right
        glVertex3d(self.game_object.player_position[0] - self.game_object.position[0], self.game_object.player_position[1] - self.game_object.position[1] - 0.5, self.game_object.player_position[2] - self.game_object.position[2])
        
        #Top Right
        glVertex3d(self.game_object.player_position[0] - self.game_object.position[0], self.game_object.player_position[1] - self.game_object.position[1] - 0.5, self.game_object.player_position[2] - self.game_object.position[2] + 0.10)
        
        glEnd()
    
    def draw(self):

        glPushMatrix()
        glTranslate(0.1, 0.5,-0.5)
        glScale(0.15, 0.15, 0.15)
        
        #Body
        glPushMatrix()
        glTranslate(0.0, 0.0, 0.0)
        self.rectangle()
        glPopMatrix()
        
        #Head
        glPushMatrix()
        glScale(0.5, 0.5, 0.5)
        glTranslate(-5.8, 0.25, 0.5)
        glRotatef(20,0,0,1)
        self.rectangle()
        glPopMatrix()

        #Right Leg
        glPushMatrix()
        glScale(0.5, 0.5, 0.5)
        glTranslate(2.5, -2.0, 0.5)
        glRotatef(90,0,0,1)
        self.rectangle()
        glPopMatrix()
        
        #Left Leg
        glPushMatrix()
        glScale(0.5, 0.5, 0.5)
        glTranslate(-3.5, -2.0, 0.5)
        glRotatef(90,0,0,1)
        self.rectangle()
        glPopMatrix()
        
        #Tail
        glPushMatrix()
        glScale(0.2, 0.2, 0.2)
        glTranslate(10.0, 1.0, 2.0)
        glRotatef(60,0,0,1)
        self.rectangle()
        glPopMatrix()
        
        #Ear
        glPushMatrix()
        glScale(0.25, 0.25, 0.25)
        glTranslate(-8.5, 2.75, 1.5)
        glRotatef(40,0,0,1)
        self.rectangle()
        glPopMatrix()
        
        glPopMatrix()
        
        #Leash
        self.leash()
        
        glDisable(GL_TEXTURE_2D)
