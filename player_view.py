import pygame
from pygame.locals import *
from pubsub import pub

from OpenGL.GLU import *
from OpenGL.GL import *

import numpy

from dog_view import DogView

from ball_view import BallView

from house_view import HouseView

from cube_view import CubeView

from localize import *

from localize import _

from game_object import GameObject

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
        
        self.paused = False
        self.player = None
        self.clock = pygame.time.Clock ()
        
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
    
    def tick(self):
        mouseMove = (0, 0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game_logic.set_property('quit', True)
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_click(pos)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    pygame.mouse.set_pos(self.viewCenter)
            
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.clicks += 1
                
                if Localize.current_lang() == 'en':
                    Localize.set_lang("it")
                elif Localize.current_lang() == 'it':
                    Localize.set_lang("en")
                
                self.update_texture()
                
                for id in self.view_objects:
                    self.view_objects[id].update_lang()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.ball.y_rotation = 0
                    
                if event.key == pygame.K_SPACE:
                    self.game_logic.create_object (GameObject, [-2, -3, -30], [0.25, 0.25, 0.25], "ball")
                    
            if not self.paused:
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - self.viewCenter[i] for i in range(2)]
            
                pygame.mouse.set_pos(self.viewCenter)
                
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
            
        if not self.paused:
            self.prepare_3d()
            
            keypress = pygame.key.get_pressed()
            
            
            if keypress[pygame.K_w]:
                pub.sendMessage('key-w')
                
            if keypress[pygame.K_s]:
                pub.sendMessage('key-s')
                
            if keypress[pygame.K_d]:
                pub.sendMessage('key-d')
                
            if keypress[pygame.K_a]:
                pub.sendMessage('key-a')
                
            pub.sendMessage('rotate-y', amount = mouseMove[0] * 0.1)
            pub.sendMessage('rotate-x', amount = mouseMove[1] * 0.1)
            
            if self.player:
                glRotate(self.player.x_rotation, 1.0, 0.0, 0.0)
                glRotate(self.player.y_rotation, 0.0, 1.0, 0.0)
                glTranslate(-self.player.position[0], -self.player.position[1], -self.player.position[2])
                
                self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
            
            glClearColor(0.0, 0.0, 1.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            
            glPushMatrix()
            self.display()
            glPopMatrix()
            
            #self.cube()
            
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
        
    def update_texture(self):
        img = pygame.font.SysFont('Arial', 50).render(_("Clicks: ") + str(self.clicks), True, (255, 255, 255), (0, 0, 0))
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
                
        closest.clicked()
        if closest.kind == 'ball':
            self.ball = closest
            
    def cube(self):
        glTranslate(3, -3, -29.5)
        glScale(0.5, 0.5, 0.5)
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
