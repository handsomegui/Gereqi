from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Playlist:
    def __init__(self, parent):
        self.ui_main = parent          
  
    def __sort_custom(self, mode="FileName"):
        """
        Puts the playlist into a sorting order
        that works only for filename sorting (the only
        order that appears to work)
        """
        # Finds the sorting status of the playlist
        hdr = self.ui_main.track_tbl.horizontalHeader()
        self.sort_order = hdr.sortIndicatorOrder()
        self.sort_pos = hdr.sortIndicatorSection()
        fname_pos = self.header_search(mode)
        
        # Not the default FileName+ascending sort
        if (self.sort_pos != fname_pos) or (self.sort_order != 0) :
            hdr.setSortIndicator(fname_pos, Qt.AscendingOrder)
                    
    def __unsort(self):
        """
        Puts the playlist sorting back to what it was 
        """
        fname_pos = self.header_search("FileName")
        if self.sort_pos != fname_pos or (self.sort_order != 0):
            hdr = self.ui_main.track_tbl.horizontalHeader()
            hdr.setSortIndicator(self.sort_pos, self.sort_order)
    
    def add_list_to_playlist(self, tracks):
        """
        Takes a list of filenames and adds to the playlist
        whilst handling the sorting orders
        """
        self.__sort_custom()
        for trk in tracks:
            # This is for adding a track which has info attached in a tuple
            if isinstance(trk, tuple):
                self.add_to_playlist(trk[0], trk[1])
            else:
                self.add_to_playlist(trk, None)        
        self.__unsort()
    
    def add_to_playlist(self, file_name, info=None):
        """
        Called when adding tracks to the playlist either locally
        or from the database. Does not pull metadata from 
        the database and is passed into the function directly
        """
        # This allows to manually put in info for things we know
        # mutagen cannot handle things like urls for podcasts
        self.ui_main.clear_trktbl_bttn.setEnabled(True)
        metadata = info
        # FIXME: ugly, ugly, ugly
        if metadata is None:
            # see if the track is already in db
            metadata = self.ui_main.media_db.get_info(file_name)
            if metadata is None:
                # get the info using the tag-extractor module
                metadata = self.ui_main.meta.extract(unicode(file_name))
                if metadata is None:
                    return
                else:       
                    trk = "%02u" % int(metadata[5])
                    metadata = {"Track": trk,  "Title": metadata[0],
                                "Artist": metadata[1], "Album": metadata[2],
                                "Year":metadata[3], "Genre": metadata[4],
                                "Length": metadata[6], "Bitrate": metadata[7], 
                                "FileName": file_name}
            else:
                trk = "%02u" % int(metadata["track"])
                metadata = {'Track': trk, "Title": metadata["title"], "Artist": metadata["artist"], 
                            "Album": metadata["album"], "Year": metadata["year"], "Genre": metadata["genre"],
                            "Length": metadata["length"], "Bitrate": metadata["bitrate"], 
                            "FileName": file_name}

        else:
            metadata['Track'] = "%02u" % metadata['Track']
                                  
        row = self.ui_main.track_tbl.rowCount()
        self.ui_main.track_tbl.insertRow(row)
        # Creates each cell for a track based on info
        for key in metadata:
            tbl_wdgt = QTableWidgetItem(metadata[key])
            column = self.header_search(key)
            self.ui_main.track_tbl.setItem(row, column, tbl_wdgt)
        self.ui_main.track_tbl.resizeColumnsToContents()   
        
        
    # This is needed as the highlighted row can be different
    # than the currentRow method of QTableview.
    def current_row(self):
        """
        Finds the playlist row of the
        currently playing track
        """
        file_list = self.gen_file_list()
        current_file = self.ui_main.player.audio_object.current_source()
        
        if current_file is None:
            return self.ui_main.track_tbl.currentRow()
        elif current_file in file_list:
            return file_list.index(current_file)
        
        
    def current_row_info(self):
        row = self.current_row()
        info = {"Track":None,"Title": None,
                "Artist": None, "Album": None,
                "Year":None, "Genre": None,
                "Length": None, "Bitrate": None, 
                "FileName": None}
        
        for key in info.keys():
            col = self.header_search(key)
            info[key] = self.ui_main.track_tbl.item(row,col).text()
            
        return info
            
            
    def gen_file_list(self):
        """
        Creates a list of files in the playlist at its
        current sorting top to bottom
        """
        rows = self.ui_main.track_tbl.rowCount() 
        column = self.header_search("FileName")
        file_list = [self.ui_main.track_tbl.item(row, column).text()
                        for row in range(rows)]
        return file_list           
        
    def del_tracks(self):
        """
        Deletes selected tracks from playlist
        """
        items = self.ui_main.track_tbl.selectedItems()
        for item in items:
            try:
                row = item.row()
                self.del_track(row)
            except RuntimeError:
                # likely deleted already 
                # i.e selected same row but multiple columns
                return 
     
    def del_track(self,row):
        """
            Deletes a single, specified row from the playlist
        """
        self.ui_main.track_tbl.removeRow(row)                
        self.tracknow_colourise(self.current_row())
        
    def header_search(self, val):
        """
        This will eventually allows the column order of the 
        playlist view to be changed.
        Returns the position of the header
        """
        cols = self.ui_main.track_tbl.columnCount()
        headers = [self.ui_main.track_tbl.horizontalHeaderItem(col).text() 
                   for col in range(cols)]
        return headers.index(val)
        
    def tracknow_colourise(self, now=None):
        """
        Instead of using QTableWidget's selectRow function, 
        set the background colour of each item in a row
        until track changes.
        """
        columns = self.ui_main.track_tbl.columnCount()
        rows = self.ui_main.track_tbl.rowCount()
        palette = self.ui_main.track_tbl.palette()
        
        for row in range(rows):
            for col in range(columns):
                item = self.ui_main.track_tbl.item(row, col)
                if row != now:
                    if row % 2:
                        # Odd-row
                        item.setBackground(palette.alternateBase().color())
                    else:
                        # even row
                        item.setBackground(palette.base().color())
                else:
                    highlight = palette.highlight().color()
                    highlight.setAlpha(128)
                    item.setBackground(highlight)
                    self.ui_main.track_tbl.selectRow(now)
                        
    def highlighted_track(self):
        """
        In the playlist
        """
        row = self.ui_main.track_tbl.currentRow()
        column = self.header_search("FileName")
        track = None
        # -1 is the row value for None
        if row > -1:
            track = self.ui_main.track_tbl.item(row, column).text()
        return track        
        
    def clear(self):
        """
        Clears the playlist
        """
        self.ui_main.track_tbl.clearContents()
        rows = self.ui_main.track_tbl.rowCount()
        for cnt in range(rows):
            self.ui_main.track_tbl.removeRow(0)
            
    def gen_full_list(self):
        """
        Get all the info in the playlist
        """
        rows = self.ui_main.track_tbl.rowCount()
        columns = self.ui_main.track_tbl.columnCount()
        headers = [self.ui_main.track_tbl.horizontalHeaderItem(cnt).text()
                        for cnt in range(columns)]
        tracks = []
        for row in range(rows):
            tmp_list = []
            for col in range(columns):
                tmp_list.append(self.ui_main.track_tbl.item(row, col).text())
            tracks.append(tmp_list)        
        return headers, tracks
     
    def track_sorting(self, index):
        """
        A bit of a hack. The table is first sorted by track automatically
        then manually sorting by album by telling the table to auto-sort
        it that way
        """
        hdrs, tracks = self.gen_full_list()
        if hdrs[index] == "Track":
            self.__sort_custom("Album")
        self.tracknow_colourise(self.current_row())
        
    def gen_track_list(self):
        """
        Get a list of filenames in playlist
        """
        rows = self.ui_main.track_tbl.rowCount()
        trk_col = self.header_search("FileName")
        tracks = []
        for row in range(rows):
            tracks.append(self.ui_main.track_tbl.item(row, trk_col).text())
        return tracks
        
        
class PlaylistHistory:
    """
    The playlist history
    """
    def __init__(self):
        self.stack = []
        self.position = 0
    
    def update(self, tracks):
        if self.position != len(self.stack):
            del self.stack[self.position:]
            
        self.stack.append(tracks)
        self.position += 1
        
    def last_list(self):
        if self.position > 0:
            self.position -= 1
            last = self.position == 0
            return self.stack[self.position], last
        
    def next_list(self):
        if self.position < len(self.stack):
            self.position += 1
            first = self.position == (len(self.stack) - 1)
            return self.stack[self.position], first
