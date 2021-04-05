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
        
        self.clicks = 0
        
        self.setup()
        
        self.click_texture = glGenTextures(1)
        
        self.update_texture()
        
        self.key_cooldown = 10
        
        self.paused = False
        self.player = None
        self.clock = pygame.time.Clock ()
        
        GameLogic.set_property('paused', True)
        self.camera_direction = [0.0, 0.0, -1.0]
        self.edit_mode = False
        self.distance = 1.5
        
        self.textures = []
        self.current_texture = 0
        self.position_mode = False
        self.size_mode = False
        self.input_mode = False
        self.get_name = False
        
        pub.subscribe(self.clear_view_objects, 'view_objects')
        
    def clear_view_objects(self):
        self.view_objects = {}
        
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
        
    def find_textures(self):
        self.textures = []
        
        for file in GameLogic.files:
            if GameLogic.files[file].startswith('images/'):
                self.textures.append(file)
        
    def tick(self):
        if not self.textures:
            self.find_textures()
            
        mouseMove = (0, 0)
        clicked = False
        self.apply_texture = False
        self.clear_texture = False
        self.position_adjust = 0.0
        self.size_adjust = 0.0
        self.set_name = False
        
        if self.get_name:
            self.update_hud_texture()
            
        self.get_name = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                GameLogic.set_property('quit', True)
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    GameLogic.set_property("quit", True)
                    return
                    
                if self.input_mode:
                    if event.key == pygame.K_RETURN:
                        self.input_mode = False
                        self.set_name = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.input = self.input[:-1]
                    else:
                        self.input += event.unicode
                        
                    self.update_hud_texture()
                   
                if not self.input_mode:
                    if event.key == pygame.K_n:
                        self.input_mode = True
                        self.get_name = True
                        self.input = ""
                        
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                        GameLogic.set_property('paused', self.paused)
                        pygame.mouse.set_pos(self.viewCenter)

                    if event.key == pygame.K_SPACE:
                        pub.sendMessage('key-jump')
                        
                    if event.key == pygame.K_s and pygame.key.get_mods() and pygame.KMOD_CTRL:
                        GameLogic.save_world()
                        
                    if event.key == pygame.K_e:
                        self.edit_mode = not self.edit_mode
                        
                    if event.key == pygame.K_t:
                        self.current_texture = (self.current_texture + 1) % len(self.textures)
                        
                    if event.key == pygame.K_r:
                        self.apply_texture = True
                        
                    if event.key == pygame.K_z:
                        self.clear_texture = True
                        
                    if event.key == pygame.K_f:
                        self.position_mode = not self.position_mode
                        
                    if event.key == pygame.K_c:
                        self.size_mode = not self.size_mode
            
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
                    
            if not self.paused:
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - self.viewCenter[i] for i in range(2)]
            
                pygame.mouse.set_pos(self.viewCenter)
                
                if event.type == pygame.MOUSEWHEEL:
                    if self.edit_mode:
                        self.distance = max(1.5, self.distance + event.y)
                        
                    if self.position_mode:
                        self.position_adjust = event.y * 0.1
                    
                    if self.size_mode:
                        self.size_adjust = event.y * 0.1
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True
                    
                    if self.edit_mode:
                        self.create_object()
                
        if self.key_cooldown == 0:
            keys = pygame.key.get_pressed()
            
            if not self.input_mode:
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
            
            if not self.input_mode:
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
            
            self.draw_guide()
            
            self.render_hud()
            
            pygame.display.flip()
            self.clock.tick(60)
            
    def draw_guide(self):
        if not self.edit_mode:
            return
        
        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position)
        
        position = (current + self.distance * camera_direction).tolist()
        
        position[0] = round(position[0])
        position[1] = round(position[1])
        position[2] = round(position[2])
        
        glPushMatrix()
        
        glTranslate(*position)
        
        glBegin(GL_QUADS)
        glColor(0.25, 0.25, 0.25, 0.5)
        # Back face
        glNormal3f( 0.0, 0.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        
        # Left face
        glNormal3f( -1.0, 0.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        
        # Front face
        glNormal3f( 0.0, 0.0, -1.0)
        glVertex3d(-0.5, 0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, 0.5, -0.5)
        
        # Right face
        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, 0.5, -0.5)
        
        # Top face
        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        
        # Bottom face
        glNormal3f( 0.0, -1.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glEnd()
        
        glPopMatrix()
        
    def create_object(self):
        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position)
        
        position = (current + self.distance * camera_direction).tolist()
        
        position[0] = round(position[0])
        position[1] = round(position[1])
        position[2] = round(position[2])
        
        GameLogic.create_object({'kind': 'cube', 'position': position})
        
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
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
    def update_hud_texture(self):
        surface = pygame.Surface((800, 30), flags = pygame.SRCALPHA)
        surface.fill(pygame.Color("lightskyblue"))
        
        text = pygame.font.SysFont('Ariel', 28).render(self.input, True, (255, 255, 255))
        surface.blit(text, (0, 0))
        
        w, h = surface.get_size()
        
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.hud_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(surface, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
    def render_hud(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, self.window_width, self.window_height, 0.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        if self.input_mode:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.hud_texture)
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
        
        self.hud_texture = glGenTextures(1)
        
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
             
             if self.set_name:
                 closest._name = self.input
                 
             if self.get_name:
                 self.input = closest.name
                 
             if self.apply_texture:
                 for face in self.get_faces(closest):
                     closest.faces[face] = {'type': 'texture', 'value': self.textures[self.current_texture]}
            
             if self.clear_texture:
                for face in self.get_faces(closest):
                     del closest.faces[face]
                     
             if self.position_mode and self.position_adjust:
                 for face in self.get_faces(closest):
                     if face == 'front':
                         closest.position[2] += self.position_adjust
                         
                     if face == 'back':
                         closest.position[2] -= self.position_adjust
                         
                     if face == 'left':
                         closest.position[0] += self.position_adjust
                         
                     if face == 'right':
                         closest.position[0] -= self.position_adjust
                         
                     if face == 'top':
                         closest.position[1] -= self.position_adjust
                         
                     if face == 'bottom':
                         closest.position[1] += self.position_adjust
                
             if self.size_mode and self.size_adjust:
                 for face in self.get_faces(closest):
                     if face == 'front' or face == 'back':
                         closest.size[2] += self.size_adjust
                         
                     if face == 'left' or face == 'right':
                         closest.size[0] += self.size_adjust
                         
                     if face == 'top' or face == 'bottom':
                         closest.size[1] += self.size_adjust
             
             if clicked:
                 closest.clicked(self.player)
        
        if closest.kind == 'ball':
            self.ball = closest
            
    def get_faces(self, game_object):
        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position)
        
        mypos = current + 1.5 * camera_direction
        
        otherpos = numpy.array(game_object.position)
        distance = numpy.linalg.norm(mypos - otherpos)
        direction_vector = (mypos - otherpos) / distance
        
        max_direction = max(direction_vector, key = abs)
        indices = [i for i, j in enumerate(direction_vector) if j == max_direction]
        
        results = []
        
        for index in indices:
            if index == 0 and direction_vector[index] < 0:
                results.append('left')
                
            if index == 0 and direction_vector[index] > 0:
                results.append('right')
            
            if index == 1 and direction_vector[index] < 0:
                results.append('bottom')
                
            if index == 1 and direction_vector[index] > 0:
                results.append('top')
            
            if index == 2 and direction_vector[index] < 0:
                results.append('front')
                
            if index == 2 and direction_vector[index] > 0:
                results.append('back')
            
        return results
