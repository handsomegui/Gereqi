#!/usr/bin/env python

from storage.Collection import CollectionDb


connection = CollectionDb("media-object")

class Artist:    
    def __init__(self,name):
        self.name = name       
          
    def __repr__(self):
        return "Artist('%s')" % self.name
          
    def albums(self):
        return (Album(self,alb) for alb 
                in connection.get_albums(self.name))

        
    
class Album:
    def __init__(self,artist,name):        
        self.artist = artist
        self.name = name
        
    def __repr__(self):
        return "Album('%s' by '%s')" % (self.name, self.artist.name)
    
    def tracks(self):
        return (Track(self,self.artist,trk['title']) for trk
                in connection.get_titles(self.artist.name,self.name))
        
class Track:
    def __init__(self,album,artist,name):
        self.album = album
        self.artist = artist
        self.name = name
        info = connection.get_info_from_info(artist.name, album.name, name)
        self.file_name  = info['file_name']
        self.year       = info['year']
        self.genre      = info['genre']
        self.track      = info['track']
        self.length     = info['length']
        self.bitrate    = info['bitrate']
        self.added      = info['added']
        self.rating     = info['rating']
        
    def __repr__(self):
        return "Track('%s' from '%s' by '%s' at %s)" % (self.name, self.album.name,
                                           self.artist.name, self.file_name)
                                           
    def set_rating(self,val):
        """
        
        """
        pass
        

        
def test():
    artists = connection.get_artists()
    for art in artists:
        for alb in Artist(art).albums():
            for trk in alb.tracks():
                print trk
                
if __name__ == "__main__":
    test()
