from PyQt4.QtCore import QThread, QString, SIGNAL
from PyQt4.QtGui import QImage
from webinfo import webInfo
from database import media
from metadata import metaData
import os

class getCover(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        
    def setValues(self, art, alb):
        self.artist = art
        self.album = alb
        
    def run(self):
        info = webInfo()
        result = info.getInfo("cover", self.artist, self.album)
        img = QImage()
        img.loadFromData(result, "JPG")        
        self.emit(SIGNAL("Activated( QImage )"), img)
        
        
class getWiki(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
    
    def setValues(self, art):
        self.artist = art
        
    def run(self):
        info = webInfo()
        result = info.getInfo("info", self.artist)
        result = QString(result)        
        self.emit(SIGNAL("Activated( QString )"), result)
        
        
class buildDB(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        
    def setValues(self, dir):
        self.mediaDir = dir
        
    def run(self):
        oldProg = 0
        tracks = []
        meta = metaData()
        mediaDB = media()
        
        for root, dirname, filename in os.walk(str(self.mediaDir)):
            for x in filename:
                fileNow = os.path.join(root, x)                
                if fileNow.endswith(".ogg") or fileNow.endswith(".mp3") or fileNow.endswith(".flac"):
                    tracks.append(fileNow)
                    
        tracksTotal = len(tracks)

        for n in range(tracksTotal):            
            prog = int(round( 100 * ( float(n) / float(tracksTotal) ) )) # may need a rnd
            if prog > oldProg:
                oldProg = prog
                self.emit(SIGNAL("Activated ( int )"), prog)
            
            track = tracks[n]
            tags = meta.extract(track)
            tags.insert(0, track) # prepends the fileName
            mediaDB.add_media(tags)
        
        status = QString("finished")
        self.emit(SIGNAL("Activated ( QString )"), status)
