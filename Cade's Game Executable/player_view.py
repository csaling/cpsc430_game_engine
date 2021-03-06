import pygame
from pygame.locals import *
from pubsub import pub

from OpenGL.GLU import *
from OpenGL.GL import *

import numpy

from dog_view import DogView
from ball_view import BallView
from cube_view import CubeView
from vampire_dog_view import VampireDogView
from localize import *
from localize import _
from game_object import GameObject
from game_logic import GameLogic

class PlayerView:
    def __init__(self):
        
        self.clear_view_objects()
        
        pub.subscribe(self.new_game_object, 'create')
        pub.subscribe(self.delete_game_object, 'delete')
        
        self.setup()
        
        self.click_texture = glGenTextures(1)
        
        self.update_texture()
        
        self.key_cooldown = 10
        
        self.paused = False
        self.player = None
        self.note = False
        self.counter = 0
        self.tag = None
        self.clock = pygame.time.Clock ()
        
        pub.subscribe(self.clear_view_objects, 'view_objects')
        pub.subscribe(self.display_note, 'display_note')
        pub.subscribe(self.hide_note, 'hide_note')
        
    def clear_view_objects(self):
        self.view_objects = {}
        
    def display_note(self, tag, timer):
        self.note = True
        self.tag = tag
        self.counter = timer
        self.update_note()
        
    def update_note(self):
        surface = pygame.Surface((800, 30), flags = pygame.SRCALPHA)
        surface.fill(pygame.Color("lightskyblue"))
        
        text = pygame.font.SysFont('Ariel', 28).render(_(self.tag), True, (255, 255, 255))
        surface.blit(text, (0, 0))
        
        w, h = surface.get_size()
        
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.note_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(surface, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
    def hide_note(self):
        self.note = False

    def new_game_object(self, game_object):
        if game_object.kind == 'dog':
            self.view_objects[game_object.id] = DogView(game_object)
        
        if game_object.kind == 'ball':
            self.view_objects[game_object.id] = BallView(game_object)
            self.ball = game_object
            
        if game_object.kind == 'cube':
            self.view_objects[game_object.id] = CubeView(game_object)
            
        if game_object.kind == 'player':
            self.player = game_object
            
        if game_object.kind == 'door':
            self.view_objects[game_object.id] = CubeView(game_object)
            
        if game_object.kind == 'vampire_dog':
            self.view_objects[game_object.id] = VampireDogView(game_object)
    
    def delete_game_object(self, game_object):
        del self.view_objects[game_object.id]
        
    def tick(self):
        mouseMove = (0, 0)
        clicked = False
        
        if self.counter > 0:
            self.counter -= 1
            
        if self.counter == 0:
            self.hide_note()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                GameLogic.set_property('quit', True)
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    GameLogic.set_property("quit", True)
                    return
                
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    GameLogic.set_property('paused', self.paused)
                    pygame.mouse.set_pos(self.viewCenter)

                if event.key == pygame.K_SPACE:
                    pub.sendMessage('key-jump')
                
                if event.key == pygame.K_e:
                    if Localize.current_lang() == 'en':
                        Localize.set_lang("it")
                        self.update_note()
                    elif Localize.current_lang() == 'it':
                        Localize.set_lang("en")
                        self.update_note()
                
                self.update_texture()
                
                for id in self.view_objects:
                    self.view_objects[id].update_lang()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.ball.y_rotation = 0
                    
            if not self.paused:
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - self.viewCenter[i] for i in range(2)]
            
                pygame.mouse.set_pos(self.viewCenter)
                
        if self.key_cooldown == 0:
            keys = pygame.key.get_pressed()
        
            if keys[K_LCTRL] or keys[K_RCTRL]:
                if keys[K_LEFT]:
                    pub.sendMessage('arrowLeft')
                    
                if keys[K_RIGHT]:
                    pub.sendMessage('arrowRight')

            else:
                if keys[K_LEFT]:
                    pub.sendMessage('ballLeft')
                    
                if keys[K_RIGHT]:
                    pub.sendMessage('ballRight')
                
                if keys[K_UP]:
                    pub.sendMessage('ballUp')
                    
                if keys[K_DOWN]:
                    pub.sendMessage('ballDown')
                
        if self.key_cooldown > 0:
            self.key_cooldown -= 1
            
        self.prepare_3d()
            
        if not self.paused:       
            pos = pygame.mouse.get_pos()
            self.handle_mouse(pos, clicked)
            self.prepare_3d()

            keypress = pygame.key.get_pressed()     
            
            if keypress[pygame.K_w] and not keypress[pygame.K_LCTRL] and not keypress[pygame.K_RCTRL]:
                pub.sendMessage('key-w', camera_direction =  self.camera_direction)
                
            if keypress[pygame.K_s] and not keypress[pygame.K_LCTRL] and not keypress[pygame.K_RCTRL]:
                pub.sendMessage('key-s', camera_direction =  self.camera_direction)
                
            if keypress[pygame.K_d] and not keypress[pygame.K_LCTRL] and not keypress[pygame.K_RCTRL]:
                pub.sendMessage('key-d')
                
            if keypress[pygame.K_a] and not keypress[pygame.K_LCTRL] and not keypress[pygame.K_RCTRL]:
                pub.sendMessage('key-a')
                
            pub.sendMessage('rotate-y', amount = mouseMove[0])
            pub.sendMessage('rotate-x', amount = mouseMove[1])
            
            if self.player:
                glRotate(self.player.x_rotation, 1.0, 0.0, 0.0)
                glRotate(self.player.y_rotation, 0.0, 1.0, 0.0)
                glTranslate(-self.player.position[0], -self.player.position[1], -self.player.position[2])
                
                self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
                
                camera_direction = numpy.linalg.inv(self.viewMatrix)
                camera_direction = camera_direction[2][0:3]
                camera_direction[0] *= -1
                camera_direction[1] *= -1
                camera_direction[2] *= -1
                self.camera_direction = camera_direction
            
            glClearColor(*GameLogic.get_property('background'))
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            
            glPushMatrix()
            self.display()
            glPopMatrix()
            
            self.render_hud()
            
            pygame.display.flip()
            self.clock.tick(60)
        
    def display(self):
        glInitNames()
        
        for id in self.view_objects:
            self.view_objects[id].display()
            
    def prepare_3d(self):
        
        glViewport(0, 0, self.window_width, self.window_height)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glEnable(GL_COLOR_MATERIAL)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        
    def render_hud(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, self.window_width, self.window_height, 0.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.click_texture)
        
        glBegin(GL_QUADS)
        
        glColor3f(1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0, 0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(200, 0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(200, 50)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0, 50)
        
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
        
        if self.note:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.note_texture)
            glBegin(GL_QUADS)
            
            glTexCoord2f(0.0, 1.0)
            glVertex2f(0, 570)
            glTexCoord2f(1.0, 1.0)
            glVertex2f(800, 570)
            glTexCoord2f(1.0, 0.0)
            glVertex2f(800, 600)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(0, 600)
            
            glEnd()
            glDisable(GL_TEXTURE_2D)
        
    def update_texture(self):
        img = pygame.font.SysFont('Arial', 50).render(_("Language") + Localize.current_lang(), True, (255, 255, 255), (0, 0, 0))
        w, h = img.get_size()
        data = pygame.image.tostring(img, "RGBA", 1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.click_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
    def setup(self):
        pygame.init()
        
        self.window_width = 800
        self.window_height = 600
        self.viewCenter = (self.window_width//2, self.window_height//2)
        
        pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF|OPENGL)
        
        self.field_of_view = 60
        self.aspect_ratio = self.window_width/self.window_height
        self.near_distance = 0.1
        self.far_distance = 100.0
        
        self.prepare_3d()
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        
        self.note_texture = glGenTextures(1)
        
    def handle_mouse(self, pos, clicked):
        keys = pygame.key.get_pressed()
        
        if not keys[K_LCTRL] and not keys[K_RCTRL] and not clicked:
            return
        
        windowX = pos[0]
        windowY = self.window_height - pos[1]
        
        glSelectBuffer(500)
        glRenderMode(GL_SELECT)
        
        glMatrixMode(GL_PROJECTION);
        glPushMatrix()
        glLoadIdentity();
        
        gluPickMatrix(windowX, windowY, 20.0, 20.0, glGetIntegerv(GL_VIEWPORT))
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(self.viewMatrix)
        self.display()
        
        glMatrixMode(GL_PROJECTION);
        glPopMatrix()
        
        buffer = glRenderMode(GL_RENDER)
        
        objects = []
        for record in buffer:
            min_depth, max_depth, name = record
            objects += name
        if not objects:
            return
        
        camera = numpy.linalg.inv(glGetFloatv(GL_MODELVIEW_MATRIX))
        camera = camera[3][0:3]
        
        closest = None
        
        for obj in objects:
            obj_pos = self.view_objects[obj].game_object.position
            if not closest or numpy.linalg.norm(obj_pos - camera) < numpy.linalg.norm(closest.position - camera):
                closest = self.view_objects[obj].game_object
        
        if closest:
             closest.hover(self.player)
             
             if clicked:
                 closest.clicked(self.player)
        
        if closest.kind == 'ball':
            self.ball = closest
        