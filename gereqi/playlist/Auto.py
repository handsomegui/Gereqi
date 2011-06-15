from PySide.QtGui import QTreeWidgetItem,QIcon,QFont
from gereqi.storage.Collection import CollectionDb
from gereqi.icons.configuration import MyIcons


db = CollectionDb("auto-playlist")

class Unplayed(QTreeWidgetItem):
    def __init__(self,parent=None):
        super(Unplayed,self).__init__(parent)
        self.setText(0,"Unplayed")
        self.setIcon(0, QIcon(MyIcons().icon("folder")))
        self.populate()
        
    def populate(self):
        tracks = db.unplayed()
        for track in tracks:
            self.addChild(QTreeWidgetItem(["%s - %s" %
                             (track["title"], track["artist"]) ]))
            
class Top(QTreeWidgetItem):
    count = 10
    def __init__(self,count=10,parent=None):
        super(Top,self).__init__(parent)
        self.count = count
        self.setText(0,"Top %s" % self.count)
        self.setIcon(0, QIcon(MyIcons().icon("folder")))
        self.populate()
        
    def populate(self):
        tracks = db.top_tracks(self.count)
        for track in tracks:
            self.addChild(QTreeWidgetItem(["%s - %s" %
                             (track["title"], track["artist"]) ]))   