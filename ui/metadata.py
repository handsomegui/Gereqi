#from PyQt4.phonon import Phonon
#from PyQt4.QtCore import QString
import tagpy

class metaData:
#    def __init__(self):
#        self.metaInformationResolver = Phonon.MediaObject()
        
    
    # Hopefully this creates a new MediaSource() otherwise playback
    # and metadata extraction will be impossible
    # Phonon.MetaData() may be a better solution. Can't find doc's
    
    def extract(self, fileName):
        tags = tagpy.FileRef(str(fileName))
        
        try:track = tags.tag().track
        except:track = 0
        
        try:
            title = tags.tag().title
            title = title.replace('''"''',"'")
            if not title:
                title = fileName.split("/")[-1]
                title = title.split(".")[0]
        except:
            title = fileName.split("/")[-1]
            title = title.split(".")[0]
        
        try:
            artist = tags.tag().artist
            artist = artist.replace('''"''',"'")
#            artist = artist.strip("'")
#            artist = lower(artist)
        except:artist = ""
            
        try:
            album = tags.tag().album
            album = album.replace('''"''',"'")
#            album = album.strip("'")
#            album = lower(album)
        except:album = ""

        try: 
            genre = tags.tag().genre
            genre = genre.replace('''"''',"'")
#            genre = lower(genre)
        except:genre = ""
        
        try: year = tags.tag().year
        except: year = 0
        
        return [track, title, artist, album, year, genre]
        
        
# If I can get it to work then i'll use it to reduce dependencies
#    def extract(self, fileName):
#        print fileName
#        item = Phonon.MediaSource(fileName)    
#        self.metaInformationResolver.setCurrentSource(item)
#        meta = self.metaInformationResolver.metaData()
#        
#        # This appears to produce nothing. May have 2 use tagpy
#        track = meta.get(QString('TRACKNUMBER'), [QString()])[0]
#        title = meta.get(QString('TITLE'), [QString()])[0]
#        if title.isEmpty(): title = self.metaInformationResolver.currentSource().fileName()
#        artist = meta.get(QString('ARTIST'), [QString()])[0]
#        album = meta.get(QString('ALBUM'), [QString()])[0]
#        year = meta.get(QString('DATE'), [QString()])[0]
#        genre = meta.get(QString('GENRE'), [QString()])[0]
#        
#        return track, title, artist, album, year, genre
#        self.metaInformationResolver.clearQueue()

