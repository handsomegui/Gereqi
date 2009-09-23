from PyQt4.QtCore import QThread, QString, SIGNAL
from PyQt4.QtGui import QImage
from webinfo import webInfo

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
