from PyQt4.phonon import Phonon

class metaData:
    def __init__(self):
        self.metaInformationResolver = Phonon.MediaObject()
    
    # Hopefully this creates a new MediaSource() otherwise playback
    # and metadata extraction will be impossible
    # Phonon.MetaData() may be a better solution. Can't find doc's
    def extract(self, fileName):
        item = Phonon.MediaSource(fileName)    
        self.metaInformationResolver.setCurrentSource(item)
        self.metaInformationResolver.metaData()
        
        track = metaData.get(QString('TRACKNUMBER'), [QString()])[0]
        title = metaData.get(QString('TITLE'), [QString()])[0]
        if title.isEmpty(): title = self.metaInformationResolver.currentSource().fileName()
        artist = metaData.get(QString('ARTIST'), [QString()])[0]
        album = metaData.get(QString('ALBUM'), [QString()])[0]
        year = metaData.get(QString('DATE'), [QString()])[0]
        genre = metaData.get(QString('GENRE'), [QString()])[0]
        
        return track, title, artist, album, year, genre
        self.metaInformationResolver.clearQueue()

