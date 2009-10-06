"""
This file contains all the necessary threads for the app
to make it easier to manage
"""

from PyQt4.QtCore import QThread, QString, SIGNAL
from PyQt4.QtGui import QImage
from webinfo import Webinfo
from database import Media
from metadata import Metadata
import os



class Getcover(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        
    def set_values(self, art, alb, loc=None):
        self.artist = art
        self.album = alb
        self.locale = loc
      
    def run(self):
        info = Webinfo()
        result = info.get_info("cover", self.locale, self.artist, self.album)
        if result:
            img = QImage()
            img.loadFromData(result, "JPG")
            self.emit(SIGNAL("Activated( QImage )"), img) 
        
        
class Getwiki(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
    
    def set_values(self, art):
        self.artist = art
        
    def run(self):
        info = Webinfo()
        result = info.get_info("info",None,  self.artist)
        result = QString(result)        
        self.emit(SIGNAL("Activated( QString )"), result)
        
        
class Builddb(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        
    def set_values(self, dir):
        self.mediaDir = dir
        
    def run(self):
        formats = ["ogg", "mp3", "flac"]
        old_prog = 0
        tracks = []
        meta = Metadata()
        media_db = Media()
        
        for root, dirname, filenames in os.walk(str(self.mediaDir)):
            for name in filenames:
                fileNow = os.path.join(root, name)
                ender = fileNow.split(".")[-1]
                ender = ender.lower()
                # We only want to get tags for certain file formats as
                # tagpy can only work with certain types
                if ender in formats:
                    tracks.append(fileNow)
                    
        tracksTotal = len(tracks)
        
        #TODO:maybe put in a check to not bother getting tags for
        # an existing file and skipping anyway
        for cnt in range(tracksTotal):
            prog = float(cnt ) /  float(tracksTotal)
            prog = round(100 * prog)
            prog = int(prog)
            if prog > old_prog:
                old_prog = prog
                self.emit(SIGNAL("Activated ( int )"), prog)
            
            track = tracks[cnt ]
            tags = meta.extract(track)
            # prepends the fileName as the DB function expects
            # a certain order to the args passed
            tags.insert(0, track) 
            media_db.add_media(tags)
        
        status = QString("finished")
        self.emit(SIGNAL("Activated ( QString )"), status)
