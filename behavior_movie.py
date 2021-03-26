from behavior import Behavior
from movies import Movies
from pubsub import pub

class Movie(Behavior):
    def __init__(self, movie, playevent, loop = False, pauseevent = None, stopevent = None):
        super(Movie, self).__init__()
        
        self.loop = loop
        self.movie = movie
        
        pub.subscribe(self.play, playevent)
        
        if pauseevent:
            pub.subscribe(self.pause, pauseevent)
        if stopevent:   
            pub.subscribe(self.stop, stopevent)
        
    def play(self):
        Movies.play_movie(self.movie, self.loop)
    
    def pause(self):
        Movies.pause_movie(self.movie)
    
    def stop(self):
        Movie.stop_movie(self.movie)
        