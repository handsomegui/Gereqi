#Copyright 2009 Jonathan.W.Noble <jonnobleuk@gmail.com>

# This file is part of Gereqi.
#
# Gereqi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gereqi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gereqi.  If not, see <http://www.gnu.org/licenses/>.


from PyQt4.QtGui import QMainWindow, QFileDialog, \
QTableWidgetItem, QDesktopServices, QSystemTrayIcon, \
QIcon, QTreeWidgetItem, QPixmap, QMessageBox, QColor, \
QSystemTrayIcon, QInputDialog, QLineEdit, QDialog
from PyQt4.QtCore import QString, Qt, QTime, SIGNAL, \
SLOT, QDir, pyqtSignature

from random import randrange
import time

from tagging import Tagging
from threads import Getinfo, Getwiki, Builddb, Finishers, \
Watcher, DeleteFiles

from Ui_interface import Ui_MainWindow
from equaliser import Equaliser
from configuration import Configuration

from extraneous import Extraneous
from extrawidgets import SetupExtraWidgets, WidgetManips
from audiocd import AudioCD
from backend import AudioBackend
from settings import Settings
from collection import CollectionDb


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
        self.sort_order = self.ui_main.track_tbl.horizontalHeader().sortIndicatorOrder()
        self.sort_pos = self.ui_main.track_tbl.horizontalHeader().sortIndicatorSection()
        fname_pos = self.header_search(mode)
        
        # Not the default FileName+ascending sort
        if (self.sort_pos != fname_pos) or (self.sort_order != 0) :
            self.ui_main.track_tbl.horizontalHeader().setSortIndicator(fname_pos, 0)
            
    def __unsort(self):
        """
        Puts the playlist sorting back to what it was 
        """
        fname_pos = self.header_search("FileName")
        if self.sort_pos != fname_pos or (self.sort_order != 0):
            self.ui_main.track_tbl.horizontalHeader().setSortIndicator(self.sort_pos, self.sort_order)
    
    def add_list_to_playlist(self, tracks):
        """
        Takes a list of filenames and adds to the playlist
        whilst handling the sorting orders
        """
        self.__sort_custom()
        for trk in tracks:
            # This is for adding a track which has info attached in a tuple
            if isinstance(trk, tuple):
                print trk
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
        if info is None:
            info = self.ui_main.media_db.get_info(file_name)
            if info is None:
                info = self.ui_main.meta.extract(file_name)
                if info is None:
                    return
                else:       
                    metadata = {"Track": ("%02u" % info[5]), "Title": info[0], "Artist": info[1], 
                                        "Album": info[2], "Year": unicode(info[3]), "Genre": info[4], "Length": info[6],
                                        "Bitrate": unicode(info[7]), "FileName": file_name}
            else:
                metadata = {'Track': ("%02u" % info[6]), "Title": info[1], "Artist": info[2], "Album": info[3], 
                                    "Year": unicode(info[4]), "Genre": info[5], "Length": info[7], 
                                    "Bitrate": unicode(info[8]), "FileName": file_name}
                                    
        row = self.ui_main.track_tbl.rowCount()
        self.ui_main.track_tbl.insertRow(row)
        # Creates each cell for a track based on info
        for key in metadata:
            tbl_wdgt = QTableWidgetItem(QString(metadata[key]))
            column = self.header_search(key)
            self.ui_main.track_tbl.setItem(row, column, tbl_wdgt)
        self.ui_main.track_tbl.resizeColumnsToContents()   
        
        
    # This is needed as the higlighted row can be different
    # than the currentRow method of Qtableview.
    def current_row(self):
        """
        Finds the playlist row of the
        currently playing track
        """
        file_list = self.gen_file_list()
        current_file = self.ui_main.player.audio_object.current_source()
        
        if current_file is None:
            return self.ui_main.track_tbl.currentRow()
        else:
            return file_list.index(current_file)
        
        
    def gen_file_list(self):
        """
        Creates a list of files in the playlist at its
        current sorting top to bottom
        """
        rows = self.ui_main.track_tbl.rowCount() 
        column = self.header_search("FileName")
        file_list = [unicode(self.ui_main.track_tbl.item(row, column).text())
                        for row in range(rows)]
        return file_list           
        
    def del_track(self):
        """
        Deletes selected tracks from playlist
        """
        items = self.ui_main.track_tbl.selectedItems()
        for item in items:
            try:
                row = item.row()
                self.ui_main.track_tbl.removeRow(row)
                self.tracknow_colourise()
            except RuntimeError:
                # likely deleted already i.e selected same row but multiple columns
                return 
        
    def header_search(self, val):
        """
        This will eventually allows the column order of the 
        playlist view to be changed         
        """
        cols = self.ui_main.track_tbl.columnCount()
        headers = [self.ui_main.track_tbl.horizontalHeaderItem(col).text() 
                   for col in range(cols)]
        return headers.index(val)
        
    #TODO: use native/theme colours for odd/even colours
    def tracknow_colourise(self, now=None):
        """
        Instead of using QTableWidget's selectRow function, 
        set the background colour of each item in a row
        until track changes.
        """       
        columns = self.ui_main.track_tbl.columnCount()
        rows = self.ui_main.track_tbl.rowCount()
        for row in range(rows):
            for col in range(columns):
                item = self.ui_main.track_tbl.item(row, col)
                if row != now:
                    if row % 2:
                        item.setBackgroundColor(self.ui_main.colours["odd"])
                    else:
                        item.setBackgroundColor(self.ui_main.colours["even"])
                else:
                    item.setBackgroundColor(self.ui_main.colours["now"])
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
        # For some reason can only remove from bot to top
        for cnt in range(rows, -1, -1):
            self.ui_main.track_tbl.removeRow(cnt)
            
    def gen_full_list(self):
        rows = self.ui_main.track_tbl.rowCount()
        columns = self.ui_main.track_tbl.columnCount()
        headers = [unicode(self.ui_main.track_tbl.horizontalHeaderItem(cnt).text())
                                                                                  for cnt in range(columns)]
        tracks = []
        for row in range(rows):
            tmp_list = []
            for col in range(columns):
                tmp_list.append(unicode(self.ui_main.track_tbl.item(row, col).text()))
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
        
class PlaylistHistory:
    """
    The playlist history
    """
    stack = []
    position = 0
    
    def update(self, tracks):
        if PlaylistHistory.position != len(PlaylistHistory.stack):
            del PlaylistHistory.stack[PlaylistHistory.position:]
            
        PlaylistHistory.stack.append(tracks)
        PlaylistHistory.position += 1
        
    def last_list(self):
        if PlaylistHistory.position > 0:
            PlaylistHistory.position -= 1
            last = PlaylistHistory.position == 0
            return PlaylistHistory.stack[PlaylistHistory.position], last
        
    def next_list(self):
        if PlaylistHistory.position < len(PlaylistHistory.stack):
            PlaylistHistory.position += 1
            first = PlaylistHistory.position == (len(PlaylistHistory.stack) - 1)
            return PlaylistHistory.stack[PlaylistHistory.position], first

class Track:
    def __init__(self, parent):
        self.ui_main = parent
        
    def generate_track(self, mode, row=None):
        """
        As the playlist changes on sorting, the playlist (the immediately next/previous 
        tracks) has to be regenerated before the queing of the next track
        """
        # So that it can be dynamic later on when columns can be moved
        column = self.ui_main.playlisting.header_search("FileName")
        track = None
        if mode == "now":
            track = self.ui_main.track_tbl.item(row, column).text()
        else:
            # If 0 then the playlist is empty
            rows = self.ui_main.track_tbl.rowCount() 
            if rows > 0:
                row_now = self.ui_main.playlisting.current_row()
                if row_now is not None:
                    if mode == "back":
                        if (row_now - 1) >= 0:
                            track = self.ui_main.track_tbl.item(row_now - 1 , column)
                            track = track.text()
                    elif mode == "next":
                        if self.ui_main.play_type_bttn.isChecked() is True:
                            # Here we need to randomly choose the next track
                            row = randrange(0, rows)
                            track = self.ui_main.track_tbl.item(row, column)
                            track = track.text()
                        elif (row_now + 1) < rows:
                            track = self.ui_main.track_tbl.item(row_now + 1, column)
                            track = track.text()
        if track:
            return str(track)
            
    def generate_info(self):
        """
        This retrieves data from the playlist table, not the database. 
        This is because the playlist may contain tracks added locally.        
        """
        row = self.ui_main.playlisting.current_row()
        hdr = self.ui_main.playlisting.header_search
        title = self.ui_main.track_tbl.item(row, hdr("Title")).text()
        artist = self.ui_main.track_tbl.item(row, hdr("Artist")).text()
        album = self.ui_main.track_tbl.item(row, hdr("Album")).text()
        minu, sec = self.ui_main.track_tbl.item(row, hdr("Length")).text().split(":")
        self.play_time = 1000 * ((int(minu) * 60) + int(sec))
        
        self.msg_status = "Playing: %s by %s on %s" % (title, artist, album)
        self.ui_main.stat_lbl.setText(self.msg_status)
        self.ui_main.playlisting.tracknow_colourise(row)
        self.ui_main.art_alb["nowart"] = unicode(artist)
        self.ui_main.art_alb["nowalb"] = unicode(album)
        self.ui_main.art_alb["title"] = unicode(title)
        

class MainWindow(Ui_MainWindow, QMainWindow): 
    """
    Where everything starts from, mostly.
    """    
    
    def __init__(self, parent = None):
        """
        Initialisation of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
        self.__settings_init()
        
        self.build_lock = self.delete_lock = False
        self.art_alb = {"oldart":None, "oldalb":None, 
                                "nowart":None, "nowalb":None, 
                                "title":None, "oldtit":None} 
        self.old_pos = 0
        self.locale = ".com"
        self.audio_formats = ["flac", "mp3", "ogg",  "m4a"]
        self.format_filter = ["*.ogg", "*.flac", "*.mp3",  "*.m4a"]
        self.colours = {
           "odd": QColor(220, 220, 220, 128), 
           "even": QColor(255, 255, 255), 
           "now": QColor(128, 184, 255, 128), 
           "search": QColor(255, 128, 128, 128)}
           
        QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        # TODO: change ui settings based on saved states/options
        self.setupUi(self)
        
     
        self.info_thread = Getinfo(self)
        self.html_thread = Getwiki()
        self.build_db_thread = Builddb(self)
        self.del_thread = DeleteFiles(self)
        self.extras = Extraneous()
        self.meta = Tagging(self.audio_formats)
        self.player = AudioBackend(self)
        self.playlisting = Playlist(self)
        self.xtrawdgt = SetupExtraWidgets(self)
        self.tracking = Track(self)
        self.wdgt_manip = WidgetManips(self)
        self.finishes = Finishers(self)
        self.play_hist = PlaylistHistory()

        # TODO: use the new PyQt4 signal/slot convention
        
        #new style signalling
        self.build_db_thread.finished.connect(self.finishes.db_build)
        self.filesystem_tree.expanded.connect(self.__resize_filesystem_tree)
        self.filesystem_tree.doubleClicked.connect(self.__filesystem_tree_item)
        self.play_actn.toggled.connect(self.play_bttn.setChecked)
        self.actionNext_Track.triggered.connect(self.next_bttn.click)
        self.prev_track_actn.triggered.connect(self.prev_bttn.click)
        self.stop_actn.triggered.connect(self.prev_bttn.click)
        self.stat_bttn.pressed.connect(self.quit_build)
        self.play_type_bttn.toggled.connect(self.wdgt_manip.set_play_type)
        self.track_tbl.horizontalHeader().sectionClicked.connect(self.playlisting.track_sorting)
        self.collect_tree_hdr.sectionClicked.connect(self.__collection_sort)
        self.html_thread.got_wiki.connect(self.finishes.set_wiki)
        self.build_db_thread.progress.connect(self.stat_prog.setValue)
        self.del_thread.deleted.connect(self.wdgt_manip.setup_db_tree)
        
        # Old style signalling
        self.connect(self.info_thread, SIGNAL("got-info ( QString ) "), self.info_view.setHtml)
        
        
        # Make the collection search line-edit have the keyboard focus on startup.
        self.search_collect_edit.setFocus()
        self.wdgt_manip.setup_db_tree()
        self.wdgt_manip.pop_playlist_view()        
        
    def __setup_watcher(self):
        watch = self.sets_db.get_collection_setting("watch")  == "True"
        recur = self.sets_db.get_collection_setting("recursive")  == "True"
        
        if (self.media_dir is not None) and watch is True:
            try:
                # To stop the possibly already running thread
                self.watch_thread.exit()
            except AttributeError:
                pass
                
            print("WATCHING: ", self.media_dir[0])
            self.watch_thread = Watcher(self)
            self.watch_thread.set_values(self.media_dir, 60, recur)
            self.watch_thread.start()
            self.connect(self.watch_thread, SIGNAL('deletions ( QStringList )'), self.__files_deleted)
            self.connect(self.watch_thread, SIGNAL('creations ( QStringList )'), self.__files_created)
        
    def __files_deleted(self, deletions):
        """
        When something is deleted in the collection dir
        the filename is put into a list. This list checked every 60secs
        and fed into the DB
        """
        self.del_thread.set_values(deletions)        
        self.del_thread.start()
            
    def __files_created(self, creations):
        self.build_db_thread.set_values(None, self.audio_formats, False, creations)
        self.stat_lbl.setText("Auto-Scanning")
        self.stat_prog.setValue(0)
        self.build_db_thread.start()
        
    def __db_setup(self):
        try:
            del self.media_db
        except AttributeError:
            pass
            
        self.db_type = self.sets_db.get_database_setting("type")        
        if self.db_type is None :
            self.media_db = CollectionDb(mode="SQLITE")
        elif self.db_type == "SQLITE":
            self.media_db = CollectionDb(mode="SQLITE")
        elif self.db_type == "MYSQL":
            self.mysql_args = {"hostname": self.sets_db.get_database_setting("hostname"), 
                            "username":  self.sets_db.get_database_setting("username"), 
                            "password": self.sets_db.get_database_setting("password"), 
                            "dbname": self.sets_db.get_database_setting("dbname") }
            self.media_db = CollectionDb("MYSQL", self.mysql_args)
            
    def __dirs_setup(self):
        func = lambda x : x if not None else []
        includes = self.sets_db.get_collection_dirs("include")
        excludes = self.sets_db.get_collection_dirs("exclude")
        self.media_dir = (func(includes), func(excludes))
        
    def __settings_init(self):
        self.sets_db = Settings()
        self.__dirs_setup()
        self.__db_setup()
        self.__setup_watcher()
            
    @pyqtSignature("QString")  
    def on_search_collect_edit_textChanged(self, srch_str):
        """
        This allows the filtering of the collection tree
        """
        self.wdgt_manip.setup_db_tree()       
    
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_collect_tree_itemDoubleClicked(self, item, column):
        """
        When double click and abum in the collection browser
        add the album's tracks to the playlist.
        """
        now = unicode(item.text(0))
        par = item.parent()
        track = album = artist = None
        mode = self.__collection_mode()
        
        if mode == "artist":
            # When we haven't selected an artist
            if par is not None:
                par_par = par.parent()
                # When we select an individual track
                if par_par is not None:
                    artist = unicode(par_par.text(0))
                    album = unicode(par.text(0))
                    track = now
                # When we've selected an album
                else:
                    album = now
                    artist = unicode(par.text(0))
                    
            # In any case we'll have an artist
            # Just an artist selected
            if artist is None:
                artist = now
                tracks = self.media_db.get_artists_files(artist)
                self.playlisting.add_list_to_playlist(tracks)

            elif track is not None:
                file_name = self.media_db.get_file(artist, album, track)
                self.playlisting.add_to_playlist(file_name)
            elif album is not None:
                tracks = self.media_db.get_files(artist, album)
                self.playlisting.add_list_to_playlist(tracks)
        else:
            if par is not None:
                file_name = self.media_db.get_album_file(unicode(par.text(0)), now)
                self.playlisting.add_to_playlist(file_name)
                
            else:
                file_names = self.media_db.get_album_files(now)
                self.playlisting.add_list_to_playlist(file_names)
    
    @pyqtSignature("")
    def on_prev_bttn_pressed(self):
        """
        Skip to previous track in viewable playlist
        if possible
        """
        track = self.tracking.generate_track("back")
        if track is not None:
            self.player.audio_object.stop()
            self.player.audio_object.load(track)
            # Checks to see if the playbutton is in play state
            if self.play_bttn.isChecked() is True:
                self.player.audio_object.play()
            else:
                self.playlisting.tracknow_colourise(self.playlisting.current_row())

    @pyqtSignature("bool")
    def on_play_bttn_toggled(self, checked):
        """
        The play button either resumes or starts playback.
        Not possible to play a highlighted row.
        """
        paused = self.player.audio_object.is_paused()
        playing = self.player.audio_object.is_playing()
        
        # The button is set
        if checked is True:
            queued = self.player.audio_object.current_source()
            highlighted = self.playlisting.highlighted_track()            
            # Something in the playlist is selected
            if highlighted is not None:      
                # The track in backend is not the same as selected and paused
                if (queued != highlighted) and (paused is True): 
                    self.player.audio_object.load(unicode(highlighted))
                # Nothing already loaded into playbin
                elif queued is None:
                    selected = self.track_tbl.currentRow()
                    # A row is selected
                    if selected >= 0:
                        selected = self.tracking.generate_track("now", selected)
                        self.player.audio_object.load(selected)
                    # Nothing to play
                    else:
                        # Just reset the play button and stop here
                        self.play_bttn.setChecked(False)                        
                # Just unpausing
                elif paused is True:
                    # Makes sure the statusbar text changes from
                    # paused back to the artist/album/track string
                    self.stat_lbl.setText(self.tracking.msg_status)                    
                self.player.audio_object.play()
                self.stop_bttn.setEnabled(True)
                self.wdgt_manip.icon_change("play")
                
            # Nothing to play
            else:
                self.play_bttn.setChecked(False)
                return
                
        # The button is unset
        else:
            if playing is True:
                self.player.audio_object.pause()
            self.wdgt_manip.icon_change("pause")
            if self.track_tbl.currentRow() >= 0:
                self.stat_lbl.setText("Paused")
            else:
                self.stat_lbl.setText("Finished")
                
        # Oblivious to it all. Not sure if these should be part
        # of the "Nothing to play" situations also.
        self.play_action.setChecked(checked)
        self.play_actn.setChecked(checked)
        
    @pyqtSignature("")    
    def on_stop_bttn_pressed(self):
        """
        To stop current track.
        """
        self.horizontal_tabs.setTabEnabled(1, False)
        self.horizontal_tabs.setTabEnabled(2, False)
        self.player.audio_object.stop()
        self.play_bttn.setChecked(False)
        self.stop_bttn.setEnabled(False)
        
    @pyqtSignature("")
    def on_next_bttn_pressed(self):
        """
        Go to next item in playlist(down)
        """
        track = self.tracking.generate_track("next")
        if track is not None:
            self.player.audio_object.stop() 
            self.player.audio_object.load(track)
            if self.play_bttn.isChecked() is True:
                self.player.audio_object.play()
            else:
                self.playlisting.tracknow_colourise(self.playlisting.current_row())
        else:
            # TODO: some tidy up thing could go here
            return
     
    @pyqtSignature("int")
    def on_volume_sldr_valueChanged(self, value):
        """
        Self explanatory
        """        
        value = (value / 100.0) ** 2
        self.player.audio_object.set_volume(value)
    
    @pyqtSignature("")
    def on_actionConfigure_triggered(self):
        """
       Brings up the configuration Dialog
        """
        config = Configuration(self)
        config.show()        
        if config.exec_():
            self.__dirs_setup()
            self.__setup_watcher() 
            self.__db_setup()
            self.wdgt_manip.setup_db_tree()
            
    @pyqtSignature("")
    def on_actionRescan_Collection_triggered(self):
        """
        Scans through a directory and looks for supported media,
        extracts metadata and adds them to the database,hopefully.
        Really needs to be done in a separate thread as scan could
        take a while.
        """
        print("Deleting media DB and rebuilding")        
        self.create_collection(fresh=True)
    
    @pyqtSignature("")
    def on_actionQuit_triggered(self):
        """
        Closing Down. Maybe some database interaction.
        """
        #self.watch_thread.exit()
        exit()
    
    @pyqtSignature("")
    def on_play_media_actn_triggered(self):
        """
        Extract music files and shove into current playlist.
        """        
        mfiles = QFileDialog.getOpenFileNames(\
                        None, 
                        QString("Select Music Files"),
                        QDesktopServices.storageLocation(QDesktopServices.MusicLocation), 
                        QString(" ".join(self.format_filter)), 
                        None)       
                        
        if mfiles is not None:
            for item in mfiles:
                ender = unicode(item).split(".")[-1]
                if ender.lower() in self.audio_formats:
                    self.playlisting.add_to_playlist(unicode(item))

    @pyqtSignature("bool")
    def on_minimise_tray_actn_toggled(self, checked):
        self.minimise_to_tray(checked)
    
    @pyqtSignature("")
    def on_actionClear_triggered(self):
        """
        Clear current playlist and if no music playing
        clear self.player.audio_object
        """
        tracks = self.playlisting.gen_file_list()
        self.play_hist.update(tracks)
        self.playlisting.clear()
        self.prev_trktbl_bttn.setEnabled(True)
        self.clear_trktbl_bttn.setEnabled(False)
    
    @pyqtSignature("")
    def on_clear_trktbl_bttn_clicked(self):
        """
        Clears current playlist and sets focus
        on the search linedit
        """
        self.on_actionClear_triggered()
        self.search_trktbl_edit.setFocus()
        self.next_trktbl_bttn.setEnabled(False)
    
    @pyqtSignature("QString")
    def on_search_trktbl_edit_textChanged(self, srch_str):
        """
        Filters current playlist based on input.
        Not sure whether to highlight row or item
        """
        # Resets before searching again
        now = self.playlisting.current_row()
        if now is not None:
            self.playlisting.highlighted_track()
        
        # Checks if the search edit isn't empty
        if len(str(srch_str).strip()) > 0:
            rows = []
            columns = self.track_tbl.columnCount()
            searched = self.track_tbl.findItems(srch_str, Qt.MatchContains)
            for search in searched:
                row = search.row()
                if row not in rows:
                    rows.append(row)
                    for col in range(columns):
                        item = self.track_tbl.item(row, col)
                        item.setBackgroundColor(self.colours["search"])
            for row in range(self.track_tbl.rowCount()):
                if row not in rows:
                    for col in range(columns):
                        item = self.track_tbl.item(row, col)
                        if row % 2:
                            item.setBackgroundColor(self.colours["odd"])
                        else:
                            item.setBackgroundColor(self.colours["even"])
        else:
            self.playlisting.tracknow_colourise()
                
    @pyqtSignature("bool")
    def on_mute_bttn_toggled(self, checked):
        """
        Mutes audio output and changes button icon accordingly
        """
        self.player.audio_object.mute(checked)
        if checked is True:
            icon = QIcon(QPixmap(":/Icons/audio-volume-muted.png"))
            self.mute_bttn.setIcon(icon)
        else:
            vol = (self.volume_sldr.value() / 100.0) ** 2
            icon = QIcon(QPixmap(":/Icons/audio-volume-high.png"))
            self.mute_bttn.setIcon(icon)
            self.player.audio_object.set_volume(vol)
      
    @pyqtSignature("")  
    def on_progress_sldr_sliderReleased(self):
        """
        Set's an internal seek value for tick() to use
        """
        val = self.progress_sldr.value()
        self.player.audio_object.seek(val)
        self.old_pos = val
    
    @pyqtSignature("")
    def on_actionUpdate_Collection_triggered(self):
        """
        Updates collection for new files. Ignore files already in database
        """
        # TODO: not completed yet. See self.create_collection
        print("Rebuild: Ensure the db is ON CONFLICT IGNORE")
        self.create_collection()

    @pyqtSignature("int, int")
    def on_track_tbl_cellDoubleClicked(self, row, column):
        """
        When item is doubleclicked. Play its row.
        """
        #This won't actualy stop. It'll pause instead.
        self.play_bttn.setChecked(False)
        
        self.player.audio_object.stop()
        track = self.tracking.generate_track("now", row)
        self.player.audio_object.load(track)
        # Checking the button is the same
        #  as self.player.audio_object.play(), just cleaner overall
        self.play_bttn.setChecked(True) 
        self.play_action.setChecked(True)
        
    @pyqtSignature("")
    def on_actionHelp_activated(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.information(None,
            QString("Help"),
            QString("""Boo!"""))

    @pyqtSignature("QTreeWidgetItem*")
    def on_collect_tree_itemExpanded(self, item):
        """
        Generates the albums to go with the artists in
        the collection tree when expanded. Only if empty.
        """
        filt_time = self.__time_filt_now()
        par = item.parent()
        mode = self.__collection_mode()
        
        if mode == "artist":
        # If we've expanded an album
            if par is not None:
                artist = unicode(par.text(0))
                album = unicode(item.text(0))
            else:
                artist = unicode(item.text(0))
                album = None
            
            if (album is not None) and (item.childCount() == 0):
                # Adding tracks to album
                if filt_time is None:
                    tracks = self.media_db.get_titles(artist, album)
                else:
                    tracks = self.media_db.get_titles_timed(artist, album, filt_time)
                 
                # Found this via Schwartzian transform. Only 2/3rds of full transform
                tracks = [(trk[1], trk[0]) for trk in tracks]
                tracks.sort()
                
                for cnt in range(len(tracks)):
                    track = QTreeWidgetItem([tracks[cnt][1]] )
                    item.insertChild(cnt, track)
      
           # Adding albums to the artist 
           # i.e. the parent has no children    
            elif item.childCount() == 0: 
                if filt_time is None:
                    albums = self.media_db.get_albums(artist)
                else:
                    albums = self.media_db.get_albums_timed(artist, filt_time)                
                for cnt in range(len(albums)):      
                    album = QTreeWidgetItem([albums[cnt]])
                    album.setChildIndicatorPolicy(0)
                    item.insertChild(cnt, album)
                
        else:
            if par is not None:
                album = unicode(par.text(0))
                track = unicode(item.text(0))
            else:
                album = unicode(item.text(0))
                track = None
            
            if (track is None) and (item.childCount() == 0):
                if filt_time is None:
                    tracks = self.media_db.get_album_titles(album)
                else:
                    tracks = self.media_db.get_album_titles_timed(album, filt_time)                
                for cnt in range(len(tracks)):      
                    track = QTreeWidgetItem([tracks[cnt]])
                    item.insertChild(cnt, track)
                
                
    @pyqtSignature("")
    def on_clear_collect_bttn_clicked(self):
        """
        Clears the collection search widget and in turn
        resets the collection tree
        """
        self.search_collect_edit.clear()
        self.search_collect_edit.setFocus()

    @pyqtSignature("int")
    def on_collect_time_box_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        self.wdgt_manip.setup_db_tree()
        
    @pyqtSignature("")
    def on_actionAbout_Gereqi_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.aboutQt(None, 
            QString(""))
            
    @pyqtSignature("")
    def on_clear_search_bttn_clicked(self):
        """
        Clears the playlist search filter
        """
        self.search_trktbl_edit.clear()
        self.playlisting.highlighted_track()
        
    @pyqtSignature("")
    def on_play_cd_actn_triggered(self):
        """
        Slot documentation goes here.
        """
        check = QMessageBox.question(None,
            QString("Play Audio-CD?"),
            QString("""Playback of CDs works up to a point at the moment. 
            Until Gstreamer-10.26 is released this situation will not change.  
            You can give it a try anyway."""),
            QMessageBox.StandardButtons(\
                QMessageBox.No | \
                QMessageBox.Yes))        
        
        if check == QMessageBox.Yes:
            acd = AudioCD()
            cd_tracks = acd.get_info()
            tracks = [(trk[-1],  trk) for trk in cd_tracks]
            self.playlisting.add_list_to_playlist(tracks)                
            self.clear_trktbl_bttn.setEnabled(True)
                
    @pyqtSignature("")
    def on_save_trktbl_bttn_clicked(self):
        """
        Based on what is in the playlist and chosen name, it'll
        get put into the database
        """
        play_name = QInputDialog.getText(\
            None,
            QString("Save Playlist"),
            QString("Enter a name for the playlist:"),
            QLineEdit.Normal)
            
        if play_name[1] is True:
            check = self.media_db.playlist_tracks(unicode(play_name[0]))
            if len(check) > 0:
                msg = QMessageBox.warning(None,
                    QString("Overwrite Playlist?"),
                    QString("""A playlist named '%s' already exists. Do you want to overwrite it?"""  
                                % unicode(play_name[0])),
                    QMessageBox.StandardButtons(\
                        QMessageBox.Cancel | \
                        QMessageBox.No | \
                        QMessageBox.Yes))
                
                if msg == QMessageBox.Yes:
                    pass
                elif msg == QMessageBox.Cancel:
                    return
                elif msg == QMessageBox.No:
                    self.on_save_trktbl_bttn_clicked()
                    
            tracks = self.playlisting.gen_file_list()            
            for track in tracks:
                self.media_db.playlist_add(unicode(play_name[0]), track)
            self.wdgt_manip.pop_playlist_view()
            
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_playlist_tree_itemDoubleClicked(self, item, column):
        """
        Slot documentation goes here.
        """
        try:
            par = unicode(item.parent().text(0))
        except  AttributeError:
            return
        
        if par == "Podcasts":
            return
            
        elif par == "Radio Streams":
            return
            
        elif par == "Playlists":
            playlist = item.text(column)
            tracks = self.media_db.playlist_tracks(unicode(playlist))
            self.playlisting.add_list_to_playlist(tracks)
            self.clear_trktbl_bttn.setEnabled(True)
        else:
            new_par = item.parent().parent()            
            if new_par.text(0) == "Playlists":
                artist, title = unicode(item.text(0)).split(" - ")
                track = self.media_db.search_by_titandart(artist, title)[0]
                self.playlisting.add_to_playlist(track)
                
            
    @pyqtSignature("bool")
    def on_delete_playlist_bttn_clicked(self, checked):
        """
        Delete a selected playlist from the DB
        """
        playlist = self.playlist_tree.selectedItems()
        if len(playlist) > 0:
            self.media_db.playlist_delete(unicode(playlist[0].text(0)))
            self.wdgt_manip.pop_playlist_view()
            
    
    @pyqtSignature("bool")
    def on_rename_playlist_bttn_clicked(self, checked):
        """
        Rename the slected playlist
        """
        playlist = self.playlist_tree.selectedItems()
        try:
            par = unicode(playlist[0].parent().text(0))
        except  AttributeError:
            return        
            
        if (len(playlist) > 0) and (par in ["Podcasts", "Radio Streams",  "Playlists"]):
            new_name = QInputDialog.getText(\
                None,
                QString("Rename Playlist"),
                QString("Rename the playlist to:"),
                QLineEdit.Normal)
            
            # Checks if you entered a non-zero length name and that you clicked 'ok'
            if (new_name[1] is True) and (len(unicode(new_name[0])) > 0):
                #get all the tracks in the selected playlist
                tracks = self.media_db.playlist_tracks(unicode(playlist[0].text(0)))
                # delete the old playlist
                self.media_db.playlist_delete(unicode(playlist[0].text(0)))
                # add the tracks back in but with a new name, probably cleaner using an sql query
                for track in tracks:
                    self.media_db.playlist_add(unicode(new_name[0]), track)
                self.wdgt_manip.pop_playlist_view()
            
    @pyqtSignature("bool")
    def on_prev_trktbl_bttn_clicked(self, checked):
        """
        The previous-track button does various
        actions dependin of the payback state
        """
        self.playlisting.clear()

        if PlaylistHistory.position < len(PlaylistHistory.stack) :
            self.next_trktbl_bttn.setEnabled(True)
        tracks, last = self.play_hist.last_list()
        self.playlisting.add_list_to_playlist(tracks)
        self.clear_trktbl_bttn.setEnabled(True)
        
        if last is True:
            self.prev_trktbl_bttn.setEnabled(False)
        
    @pyqtSignature("bool")
    def on_next_trktbl_bttn_clicked(self, checked):
        """
        The next-track button does various
        actions dependin of the payback state
        """
        self.playlisting.clear()
        self.prev_trktbl_bttn.setEnabled(True)
        tracks, first = self.play_hist.next_list()
        self.playlisting.add_list_to_playlist(tracks)
        self.clear_trktbl_bttn.setEnabled(True)
        
        if first is True:
            self.next_trktbl_bttn.setEnabled(False)
     
    @pyqtSignature("")
    def on_actionEqualiser_activated(self):
        dialog = Equaliser(self)
        dialog.show()
        
    @pyqtSignature("")
    def on_menuTools_aboutToShow(self):
        """
        Disables the db interaction actions if in useless state
        """
        self.media_dir[0]
        if len(self.media_dir[0]) < 1:
            self.actionUpdate_Collection.setEnabled(False)
            self.actionRescan_Collection.setEnabled(False)
        else:
            self.actionUpdate_Collection.setEnabled(True)
            self.actionRescan_Collection.setEnabled(True)
            
#######################################
#######################################
        
        
    #TODO: it's possible a few of these functions could be moved to wdgt_manip
    def quit_build(self):
        """
        Cancels the collection build if running
        """
        print(self.build_db_thread.stop_now())

    def set_prog_sldr(self):
        """
        Linked to the current time of
        track being played
        """
        self.progress_sldr.setRange(0, self.tracking.play_time)
        self.t_length = QTime(0, (self.tracking.play_time / 60000) % 60, 
                              (self.tracking.play_time / 1000) % 60)
            
    def minimise_to_tray(self, state):
        """
        Does what it says.
        """
        if state is True:
            self.show()
            self.setWindowState(Qt.WindowActive)
        else:
            self.hide()
        self.view_action.setChecked(state)
        self.minimise_tray_actn.setChecked(state)
    
    def create_collection(self, fresh=False):
        """
        Either generates a new DB or adds new files to it
        Not finished
        """
        # If the dialog is cancelled in last if statement the below is ignored
        if self.media_dir is not None:
            self.stat_bttn.setEnabled(True)
            self.build_db_thread.set_values(self.media_dir, self.audio_formats, fresh)
            self.stat_lbl.setText("Scanning Media")
            self.stat_prog.setValue(0)
            self.build_db_thread.start()
    
    # FIXME: this looks horrendously crap
    def set_info(self):
        """
        The wikipedia page + album art to current artist playing
        """
        art_change = self.art_alb["nowart"] != self.art_alb["oldart"] 
        alb_change = self.art_alb["nowalb"] != self.art_alb["oldalb"]
        tit_change = self.art_alb["title"] != self.art_alb["oldtit"]
        albs = self.media_db.get_albums(self.art_alb["nowart"])
        
        # Wikipedia info
        if (art_change is True) and (self.art_alb["nowart"] is not None):
            # passes the artist to the thread
            self.html_thread.set_values(self.art_alb["nowart"]) 
            # starts the thread
            self.html_thread.start() 
            self.art_alb["oldart"] = self.art_alb["nowart"]

        # Album art
        if (alb_change is True) and (self.art_alb["nowalb"] is not None):
            
            self.info_thread.set_values(artist=self.art_alb["nowart"],  album=self.art_alb["nowalb"], 
                                                    title=self.art_alb["title"], check=True, albums=albs)
            self.info_thread.start()
            self.art_alb["oldalb"] = self.art_alb["nowalb"]
            
        # TODO: maybe tell to not check for covers as we should have them by now
        elif (tit_change is True) and (self.art_alb["title"] is not None):
            self.info_thread.set_values(artist=self.art_alb["nowart"],  album=self.art_alb["nowalb"], 
                                                    title=self.art_alb["title"], check=False, albums=albs)
            self.info_thread.start()
            self.art_alb["oldalb"] = self.art_alb["nowalb"]

    def tray_event(self, event):
        """
        Things to perform on user-interaction of the tray icon
        other than bringing up it's menu
        """
        # Left click to hide/show program
        if event == 3:
            hidden = self.isVisible() is False
            self.minimise_to_tray(hidden)
        # Middle-click to pause/play
        elif event == 4:
            stopped = self.player.audio_object.is_playing() is False
            self.play_bttn.setChecked(stopped)

    def closeEvent(self, event):
        """
        When the 'X' button or alt-f4 is triggered
        """
        if self.sets_db.get_interface_setting("trayicon") == "True":
            if self.tray_icon.isVisible() is True:
                self.hide()
                event.ignore()
            
    def __resize_filesystem_tree(self):
        """
        Resizes the filesystem_tree to it's contents.
        Because of the '0' this seperate method is needed
        """
        self.filesystem_tree.resizeColumnToContents(0)
        
    def __filesystem_tree_item(self, index):
        """
        This takes the filesystem_tree item and deduces whether
        it's a file or directory and populates playlist if possible
        """
        if self.dir_model.isDir(index) is True:
            fname = self.dir_model.filePath(index)
            searcher = QDir(fname)
            searcher.setFilter(QDir.Files)
            searcher.setFilter(QDir.Files)
            searcher.setNameFilters(self.format_filter)
            tracks = [unicode(item.absoluteFilePath()) for item in searcher.entryInfoList()]
            self.playlisting.add_list_to_playlist(tracks)
            self.clear_trktbl_bttn.setEnabled(True)
        else:
            fname = self.dir_model.filePath(index)
            self.playlisting.add_to_playlist(unicode(fname))
            self.clear_trktbl_bttn.setEnabled(True)
            
    def __time_filt_now(self):
        """
        Based on the combobox selection, the collection
        browser is filtered by addition date
        """
        index = self.collect_time_box.currentIndex()
        calc = lambda val: int(round(time.time() - val))
        now = time.localtime()
        filts = [(now[3] * now[4]) + now[5], 604800, 2419200, 7257600, 31557600]   
        if index > 0:
            return calc(filts[index - 1])
        
    def __collection_mode(self):
        text_now = unicode(self.collect_tree.headerItem().text(0))
        if text_now == "Artist/Album":
            return "artist"
        else:
            return "album"
        
    def __collection_sort(self, p0):
        mode = self.__collection_mode()
        if mode == "artist":
            self.collect_tree.headerItem().setText(0, unicode("Album/Artist"))
        else:
            self.collect_tree.headerItem().setText(0, unicode("Artist/Album"))

        self.wdgt_manip.setup_db_tree()
