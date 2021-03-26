from game_logic import GameLogic
from OpenGL.GL import *
from PIL import Image

import cv2

class Movies:
    movies = {}
    counter = 0
    
    @staticmethod
    def get_frame(tag):
        if tag not in Movies.movies:
            return None
        
        if Movies.movies[tag]['texture']:
            glBindTexture(GL_TEXTURE_2D, Movies.movies[tag]['texture'])
            glEnable(GL_TEXTURE_2D)
    
    @staticmethod
    def play_movie(tag, loop = False):
        if tag in Movies.movies:
            Movies.movies[tag]['paused'] = False
        else:
            if tag not in GameLogic.files:
                return
            
            capture = cv2.VideoCapture()
            capture.open(GameLogic.files[tag])
            
            Movies.movies[tag] = {'capture': capture, 'paused': False, 'texture': None, 'loop': False}
    
    @staticmethod
    def pause_movie(tag):
        if tag in Movies.movies:
            Movies.movies[tag]['paused'] = True
    
    @staticmethod
    def stop_movie(tag):
        if tag in Movies.movies:
            if Movies.movies[tag]['texture']:
                glDeleteTextures([Movies.movies[tag]['texture']])
                
            Movies.movies[tag]['capture'].release()   
            del Movies.movies[tag]
    
    @staticmethod
    def tick():
        to_delete = []
        
        Movies.counter += 1
        Movies.counter %= 6
        if Movies.counter != 0:
            return
        
        for tag in Movies.movies:
            if Movies.movies[tag]['paused']:
                continue
            
            success, frame = Movies.movies[tag]['capture'].read()
            
            if not success and not Movies.movies[tag]['loop']:
                to_delete.append(tag)
                continue
            
            if not success:
                Movies.movies[tag]['capture'].set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame = Movies.movies[tag]['capture'].read()
                
                if not success:
                    to_delete.append(tag)
                    continue
             
            frame = Image.fromarray(frame)
            ix = frame.size[0]
            iy = frame.size[1]
            frame = frame.tobytes("raw", "RGB", 0, -1)
            
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, frame)
            
            Movies.movies[tag]['texture'] = texture_id
            
        for deletions in to_delete:
            Movies.stop_movies(deletion)
    