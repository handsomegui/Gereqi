from PyQt4.QtCore import QThread, QString, SIGNAL
from PyQt4.QtGui import QImage
from webinfo import WEBINFO
from database import MEDIA
from metadata import METADATA
import os

class GETCOVER(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        
    def setValues(self, art, alb, loc=None):
        self.artist = art
        self.album = alb
        self.locale = loc
      
    # Seems threads are self-exiting as I can start this up fine even if
    # the last time I ran it it emitted nothing.
    def run(self):
        info = WEBINFO()
        result = info.get_info("cover", self.locale, self.artist, self.album)
        if result:
            img = QImage()
            img.loadFromData(result, "JPG")
            self.emit(SIGNAL("Activated( QImage )"), img) 
        
        
class GETWIKI(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
    
    def setValues(self, art):
        self.artist = art
        
    def run(self):
        info = WEBINFO()
        result = info.get_info("info",None,  self.artist)
        result = QString(result)        
        self.emit(SIGNAL("Activated( QString )"), result)
        
        
class BUILDDB(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        
    def setValues(self, dir):
        self.mediaDir = dir
        
    def run(self):
        formats = ["ogg", "mp3", "flac"]
        old_prog = 0
        tracks = []
        meta = METADATA()
        media_db = MEDIA()
        
        for root, dirname, filename in os.walk(str(self.mediaDir)):
            for x in filename:
                fileNow = os.path.join(root, x)
                ender = fileNow.split(".")[-1]
                if ender in formats:
                    tracks.append(fileNow)
                    
        tracksTotal = len(tracks)

        for n in range(tracksTotal):            
            prog = int(round( 100 * ( float(n) / float(tracksTotal) ) )) 
            if prog > old_prog:
                old_prog = prog
                self.emit(SIGNAL("Activated ( int )"), prog)
            
            track = tracks[n]
            tags = meta.extract(track)
            tags.insert(0, track) # prepends the fileName
            media_db.add_media(tags)
        
        status = QString("finished")
        self.emit(SIGNAL("Activated ( QString )"), status)
