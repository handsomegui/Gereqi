from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QSize, pyqtSignal
from os import path
import operator

#import audio.MediaTypes 

class PlaylistTable(QTableWidget):
    headers = ["Track", "Title", "Artist",
               "Album", "Year", "Genre",  
               "Length", "Bitrate", "FileName"]
    
    sort_mode = "FileName"
    
    play_this = pyqtSignal(str, int)
    populated = pyqtSignal()
    
    def __init__(self, ui):
        super(PlaylistTable, self).__init__()
        self.ui = ui
        
        self._tracks = []
        
        self.setShowGrid(False)
        self.setGridStyle(Qt.DashLine)
        self.setWordWrap(False)
        self.setCornerButtonEnabled(True)
        self.verticalHeader().setVisible(False)
        self.setMinimumSize(QSize(400, 200))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().setMovable(True)
        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.customContextMenuRequested.connect(self.__context_menu)
        self.horizontalHeader().customContextMenuRequested.connect(self.__header_menu)
        self.horizontalHeader().sectionClicked.connect(self.__resort)
        self.cellDoubleClicked.connect(self.__throw_track_now)
        self.horizontalHeader().setSortIndicatorShown(True)
        
        self.__init_headers()
    
    def __init_headers(self):
        self.hdr_menu = QMenu()
        for hdr in self.headers:
            # add the header text
            self.insertColumn(self.headers.index(hdr))
            # Add action to the menu
            action = self.hdr_menu.addAction(hdr)
            action.setCheckable(True)
            action.setChecked(True)            
        self.setHorizontalHeaderLabels(self.headers)
        
    def __resort(self, pos):
        self.sort_mode = unicode(self.horizontalHeaderItem(pos).text())
        self.update()
        self.horizontalHeader().setSortIndicator(pos, Qt.AscendingOrder)        
        
    def __context_menu(self,pos):
        # do nothing if table is empty
        if self.rowCount() < 1:
            print("Nothing to do")
        else:
            rows = []            
            for r in self.selectedItems():
                r_now = self.row(r)
                if r_now not in rows:
                    rows.append(r_now)
                    
                    
            item_now = self.itemAt(pos)
            #The coulmn we clicked in
            col_now = self.column(item_now)
            tag_name = self.horizontalHeaderItem(col_now).text()
            
            menu = QMenu()
            icon = QIcon().fromTheme("media-playback-start")
            play_action = menu.addAction(icon, "Play")
            menu.addSeparator()
            
            remove_action = menu.addAction("Remove From Playlist")
            
            menu.addSeparator()
            
            icon = QIcon().fromTheme("document-open")
            manage_menu = QMenu("Manage File")
            manage_menu.setIcon(icon)
            manage_organise = manage_menu.addAction("Organise File")
            manage_delete = manage_menu.addAction("Delete File")
            
            menu.addMenu(manage_menu)
            
            icon = QIcon().fromTheme("edit-copy", QIcon(":/icon/edit-copy.png"))
            # Can't change these aspects of the file
            copy_tags_action = menu.addAction(icon, "Copy Tags to Clipboard")
            if tag_name not in ["FileName","Length", "Bitrate"]:
                edit_tag = menu.addAction("Edit Tag '%s'" % tag_name)
            
            action = menu.exec_(self.mapToGlobal(pos))
            if not action:
                return
                        
            row = item_now.row()
            
            if action == play_action:
                # Stop playback then start again 
                self.ui.play_bttn.setChecked(False)
                self.ui.play_bttn.setChecked(True)
                
            # Honestly, I have no idea what use this is. 
            # At least it's easy to implement
            elif action == copy_tags_action:
                row = self.itemAt(pos).row()
                col = self.ui.playlisting.header_search("Title")
                tag = self.item(row,col).text()
                clip = QApplication.clipboard()
                clip.setText(tag)
                
            elif action == remove_action:
                self.ui.playlisting.del_track(row)
                
            elif action == manage_organise:
                print "ORGANISE?"
                
            elif action == manage_delete:
                print "YEAH, I'M NOT DELETING"
                
            elif action == edit_tag:
                text = QInputDialog.getText(None, tag_name,
                                         "Change the tag to:",
                                         QLineEdit.Normal,
                                         item_now.text())
                
                if text[1]:
                    col = self.ui.playlisting.header_search("FileName")
                    for row in rows:                        
                        fname = self.item(row,col).text()
#                        self.ui.media_db.update_tag(fname,tag_name.lower(),text[0])
                        self.item(row,col_now).setText(text[0])
    
    def __header_menu(self,pos): 
        """
        The names of each header column is checkable
        for viewing of its column
        """
        action = self.hdr_menu.exec_(self.horizontalHeader().mapToGlobal(pos))
        hdr_pos = self.header_search(action.iconText())
        hdr_view = False if action.isChecked() else True
        self.setColumnHidden(hdr_pos,hdr_view)
        
    def __throw_track_now(self, row, column):
        col = self.header_search("FileName")
        item_now = self.item(row,col).text()
        self.play_this.emit(item_now, 0)
        
    def __row_of_filename(self, file_name):
        for row, trk in enumerate(self.tracks):
            if trk['FileName'] == file_name:
                # found the file_name's row in the table
                return row
        err_msg = "Trying to find %s in the Playlist Table" % file_name
        raise Exception(err_msg)
        
    def __checks(self,track):
        if path.exists(track) or track.startswith("cdda"):
            return track
        
    def clear_rows(self):
        for i in range(self.rowCount(),0,-1):
            self.removeRow(i-1)
        
    def header_search(self, val):
        headers_now = [self.horizontalHeaderItem(col).text() 
                   for col in range(self.columnCount())]
        return headers_now.index(val)   
    
    def update(self):
        self.tracks.sort(key=operator.itemgetter(self.sort_mode))
        self.clear_rows()
        for trk in self._tracks:
            # Ensure track number is zero-padded
            trk['Track'] = "%02u" % int(trk['Track'])
            row = self.rowCount()
            self.insertRow(row)
            # Creates each cell for a track based on info
            for key in trk:
                tbl_wdgt = QTableWidgetItem(trk[key])
                column = self.header_search(key)
                self.setItem(row, column, tbl_wdgt)
            self.resizeColumnsToContents()
        self.populated.emit()

    def current_track(self,info=False):
        if info:
            pass
        else:
            return self.tracks[self.currentRow()]
    
    def next(self):
        row = self.currentRow()
        if row < 0:
            # nothing selected
            return   
        if (row + 1) < self.rowCount():
            # There is a next track possible
            trk = self.tracks[row+1]["FileName"]
            return self.__checks(trk)
        
    def previous(self):
        row = self.currentRow()
        if row is None:
            return     
        if (row - 1) >= 0:
            trk = self.tracks[row-1]["FileName"]
            return self.__checks(trk)

    def colourise(self, row_now):
        """
        Reset the colours and highlight a row
        """
        
        # TODO:allow row_now to be an integer or string
        # if a string(filename), find the integer
        if isinstance(row_now, int):
            # given a row
            pass
        else:
            # assume a str/unicode i.e. filename
            row_now = self.__row_of_filename(row_now)
        
        
        # cannot set an entire row's colour. Must do each cell
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if row != row_now:
                    if row % 2:
                        # Odd-row
                        item.setBackground(self.palette().alternateBase().color())
                    else:
                        # even row
                        item.setBackground(self.palette().base().color())
                else:
                    # Highlight the current track(row)
                    highlight = self.palette().highlight().color()
                    highlight.setAlpha(128)
                    item.setBackground(highlight)
                    self.selectRow(row_now)  


    def tracknow_colourise(self):
        """
        Instead of using QTableWidget's selectRow function, 
        set the background colour of each item in a row
        until track changes.
        """
        self.colourise(self.currentRow())
               
    def del_tracks(self):
        tracks = []     
                    
    @property
    def tracks(self):
        #TODO: sort them by what is shown
        return self._tracks 
    
    @tracks.setter
    def tracks(self, items):
        self._x = items
        
    @tracks.deleter
    def tracks(self):
        del self._x
