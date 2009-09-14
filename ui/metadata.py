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
        except:print "no track"
        
        try:
            title = tags.tag().title
#            title = title.replace("&","and")
#            title = title.strip("'")
#            title = lower(title)
        except:print "no title"
        
        try:
            artist = tags.tag().artist
#            artist = artist.replace("&","and")
#            artist = artist.strip("'")
#            artist = lower(artist)
        except:print "no artist"
            
        try:
            album = tags.tag().album
#            album = album.replace("&","and")
#            album = album.strip("'")
#            album = lower(album)
        except:print "no album"

        try: genre = tags.tag().genre
#            genre = lower(genre)
        except:print "no genre"
        
        try: year = tags.tag().year
        except: print "no year"
        
        return track, title, artist, album, year, genre
        
        
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

