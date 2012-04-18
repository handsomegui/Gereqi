from ..media import Artist,Album,Track,TrackInfo
from ..storage.Collection import CollectionDb
from .. import extraneous 
from ..icons import icons_resource
from PyQt4.QtGui import *
from PyQt4.QtCore import *

connection = CollectionDb("collection-tree")


class CollectionTree(QTreeWidget):
    time_filter = 0
    text_filter = ""
    mode = 0 # 0 --> artist; 1 --> album
    items_for_playlist = pyqtSignal(list)
    def __init__(self, parent=None, mode=0):
        super(CollectionTree, self).__init__(parent)
        self.mode = mode
        
        # Widget setups
        self.header().setClickable(True)
        self.setAlternatingRowColors(True)
        self.setIndentation(10)        
        self.setAnimated(True)
        self.setExpandsOnDoubleClick(False)
        self.headerItem().setText(0, "Artist/Album")
        self.setItemDelegate(MyDelegate())
        self.setIconSize(QSize(46,46))
        
        self.itemExpanded.connect(self.__item_expanded)
        self.itemDoubleClicked.connect(self.__item_doubled)
        
    def __item_expanded(self,item):
        """
        When the user expands an item, ensure it has been populated
        """
        item.populate()
        
    def __item_doubled(self,item):
        info = item.playlist_insertion_info()
        self.items_for_playlist.emit(info)

    def __artists_to_albums(self,artists):
        albums = []
        for art in artists:
            for alb in Artist(art).albums():
                albums.append(alb)
                
        albums = sorted(albums,key=lambda alb : alb.name.lower())
        return albums
    
    def pop_albs(self):
        albums = connection.get_albums_all(self.time_filter, self.text_filter)
        last_alb = None
        for alb in albums:
            alb_obj = Album(Artist(alb['artist']), alb['album'])
            try:
                next_alb = albums[albums.index(alb) + 1]['album']
            except IndexError:
                next_alb = None 
            if alb['album'] == next_alb:
                name = "%s - %s" % (alb['album'], alb['artist'])
            else:
                name = alb['album']
            now = CollectionTreeItem(name, alb_obj, self.mode)
            self.addTopLevelItem(now)

    def populate(self):
        self.clear()
        if self.mode == 1:
                self.pop_albs()
                return          
            
        items = connection.get_artists(self.time_filter, self.text_filter)
#        if self.mode == 1:
#            items = self.__artists_to_albums(items)
        # Empty the tree
        
        for item in items:
            # Adding an artist is relatively trivial
            now = CollectionTreeItem(item, None, self.mode)
            self.addTopLevelItem(now)

#            else:
#                # Identify that albums of differing artists
#                if connection.get_album_count(item.name) > 1:
#                    name = "%s - %s" % (item.name,item.artist.name)
#                else:
#                    name = item.name
#                now = CollectionTreeItem(name,item,self.mode)
#            self.addTopLevelItem(now)
            

    def set_mode(self,val):
        self.mode = val
        self.itemDelegate().mode = val

        
        
class CollectionTreeItem(QTreeWidgetItem):
    __mode = 0
    populated = False
    def __init__(self,name,parent=None,mode=0):
        """
        mode == 0 --> artist
        mode == 1 --> album
        mode == 2 --> track
        """
        super(CollectionTreeItem,self).__init__()
        self.setText(0,name)
        self.name = name
        self.__mode = mode
        if mode == 0:
            self.__info = Artist(name)
        else:
            self.__info = parent
            
        # Tracks cannot be expanded
        if mode != 2:
            self.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            
        # Set album cover
        if mode == 1:   
            self.__set_icon()         
            
    def __set_icon(self):
        cover = extraneous.get_cover_source(self.__info.artist.name,
                                                  self.name, True, False)
        if cover:
            cover = cover.replace("file://", '')
        else:
            cover = ":icons/nocover.png"      
        self.setIcon(0, QIcon(cover))
            
    def populate(self):
        """
        Populate the treewidgetitem with its children
        """
        # It can be a lengthy process so don't
        # do it again if not needed
        if self.populated:
            return
        # Tracks have nothing to populate
        if self.__mode == 2:
            return
        # Adding an album
        elif self.__mode == 0:
            for alb in self.__info.albums():
                self.addChild(CollectionTreeItem(alb.name, alb, 1))
        # Adding a track
        elif self.__mode == 1:
            for trk in self.__info.tracks():
                self.addChild(CollectionTreeItem(trk.name, trk, 2))
                
        self.populated = True
            
    def playlist_insertion_info(self):
        """
        When double-clicking the item it is required that the item(s) are
        added to the playlist
        """
        metadata = []
        # Get all tracks by an artist
        if self.__mode == 0:
            for alb in self.__info.albums():
                for trk in alb.tracks():
                    metadata.append(self.__format_info(trk))
        # Get all tracks in an album
        elif self.__mode == 1:
            for trk in self.__info.tracks():
                metadata.append(self.__format_info(trk))
        # Single track
        elif self.__mode == 2:
            return [self.__format_info(self.__info)]    
        
        return metadata
        
    def __format_info(self,i):
        """
        Take the dat from a media-object and put into a way playlist needs
        """
        info = TrackInfo()
        info.track      = int(i.track)
        info.title      = i.name
        info.artist     = i.artist.name
        info.album      = i.album.name
        info.year       = i.year
        info.genre      = i.genre
        info.length     = i.length
        info.bitrate    = i.bitrate
        info.filename   = i.file_name
        return info
       
        
class MyDelegate(QItemDelegate):
    mode = 0
    def __init__(self,parent=None):
        super(MyDelegate,self).__init__(parent)
        self.mode = 0
        
    def sizeHint(self,option,index):
        parent = index.parent()
        if parent.isValid() and not parent.parent().isValid():
            if self.mode == 0:
                return QSize(48,48)
            else:
                return QSize(24,24)
            
        if self.mode == 0:
            return QSize(24,24)
        else:
            return QSize(48,48)
