from game_logic import GameLogic

class Movies:
    movies = {}
    
    @staticmethod
    def get_frame(tag):
        pass
    
    @staticmethod
    def play_movie(tag):
        if tag in Movies.movies:
            pass
        else:
            if tag in GameLogic.files:
                return
            
            
    
    @staticmethod
    def pause_movie(tag):
        pass
    
    @staticmethod
    def stop_movie(tag):
        pass
    
    @staticmethod
    def tick():
        pass
    