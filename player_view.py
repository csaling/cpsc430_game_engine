import pygame
from pygame.locals import *
from pubsub import pub

from OpenGL.GLU import *
from OpenGL.GL import *

import numpy

from dog_view import DogView

from ball_view import BallView

class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}
        pub.subscribe(self.new_game_object, 'create')
        
        self.clicks = 0
        
        self.setup()
        
        self.click_texture = glGenTextures(1)
        
        self.update_texture()
        
        self.key_cooldown = 10
        
    def new_game_object(self, game_object):
        if game_object.kind == 'dog':
            self.view_objects[game_object.id] = DogView(game_object)
        
        if game_object.kind == 'ball':
            self.view_objects[game_object.id] = BallView(game_object)
            self.ball = game_object
    
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game_logic.set_property('quit', True)
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_click(pos)
                self.clicks += 1
                self.update_texture()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.ball.y_rotation = 0
                    
                if event.key == pygame.K_SPACE:
                    self.game_logic.create_object ([-2, 0, -10], "ball")
                    
        if self.key_cooldown == 0:
            keys = pygame.key.get_pressed()
        
            if keys[K_LCTRL] or keys[K_RCTRL]:
                if keys[K_LEFT]:
                    self.ball.y_rotation = 1
                    self.ball.z_rotation += 2.0
                    
                if keys[K_RIGHT]:
                    self.ball.y_rotation = 1
                    self.ball.z_rotation -= 2.0

            else:
                if keys[K_LEFT]:
                    self.ball.position[0] -= 0.05
                    
                if keys[K_RIGHT]:
                    self.ball.position[0] += 0.05
                
                if keys[K_UP]:
                    self.ball.position[1] += 0.05
                    
                if keys[K_DOWN]:
                    self.ball.position[1] -= 0.05
                
        if self.key_cooldown > 0:
            self.key_cooldown -= 1
            
        self.prepare_3d()
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        self.display()
        glPopMatrix()
        
        self.render_hud()
        
        pygame.display.flip()
        pygame.time.wait(10)
        
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
        
    def update_texture(self):
        img = pygame.font.SysFont('Arial', 50).render("Clicked: " + str(self.clicks), True, (255, 255, 255), (0, 0, 0))
        w, h = img.get_size()
        data = pygame.image.tostring(img, "RGBA", 1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.click_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glPixelStorei(GL_UNPACK_ROW_LENGTH, 0)
        
    def setup(self):
        pygame.init()
        
        self.window_width = 800
        self.window_height = 600
        
        pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF|OPENGL)
        
        self.field_of_view = 60
        self.aspect_ratio = self.window_width/self.window_height
        self.near_distance = 0.1
        self.far_distance = 100.0
        
        self.prepare_3d()
        
    def handle_click(self, pos):
        windowX = pos[0]
        windowY = self.window_height - pos[1]
        
        glSelectBuffer(20)
        glRenderMode(GL_SELECT)
        
        glMatrixMode(GL_PROJECTION);
        glPushMatrix()
        glLoadIdentity();
        
        gluPickMatrix(windowX, windowY, 20.0, 20.0, glGetIntegerv(GL_VIEWPORT))
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)

        glMatrixMode(GL_MODELVIEW)
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
                
        closest.clicked()
        if closest.kind == 'ball':
            self.ball = closest