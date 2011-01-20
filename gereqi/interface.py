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


from PyQt4.QtGui import *
from PyQt4.QtCore import *

from gereqi.audio import Backend,Cdrom,Formats
from gereqi.storage.Settings import Settings
from gereqi.storage.Collection import CollectionDb
from gereqi.information.tagging import Tagging

from random import choice
import time
from os import path

from threads import Getinfo, Getwiki, Builddb, Finishers, Watcher, DeleteFiles
from Ui_interface import Ui_MainWindow
from configuration import Configuration
from extraneous import Extraneous
from extrawidgets import SetupExtraWidgets, WidgetManips

#from settings import Settings
#from collection import CollectionDb
from about import About
from playlist import Playlist, PlaylistHistory


# The folder watcher poll-time in seconds
WATCHTIME = 30 


class Track:
    def __init__(self, parent):
        self.ui_main = parent
        
    def generate_track(self, mode, row=None):
        """
        As the playlist changes on sorting, the playlist (the immediately 
        next/previous tracks) has to be regenerated before the queing of 
        the next track
        """
        column = self.ui_main.playlisting.header_search("FileName")
        track = None
        if mode == "now":
            track = self.ui_main.track_tbl.item(row, column).text()
        else:
            # If 0 then the playlist is empty
            rows = self.ui_main.track_tbl.rowCount() 
            if rows < 1:
                return
            
            row_now = self.ui_main.playlisting.current_row()
            if row_now is None:
                return
            
            if mode == "back":
                if (row_now - 1) >= 0:
                    track = self.ui_main.track_tbl.item(row_now - 1 , column)
                    track = track.text()
            elif mode == "next":
                # Random playback mode selected
                if self.ui_main.play_type_bttn.isChecked():
                    file_list = self.ui_main.playlisting.gen_track_list()
                    track = [trk for trk in file_list
                             if trk not in self.ui_main.player.recently_played]
                    if len(track) > 0:
                        track = choice(track)
                        
                elif (row_now + 1) < rows:
                    track = self.ui_main.track_tbl.item(row_now + 1, column)
                    track = track.text()
                    
        if track is None:
            return
        
        result = str(track.toUtf8())
        
        if path.exists(result) or result.startswith("cdda"):
            return result
        else:
            result = str(track.toLatin1())
            if path.exists(result):
                return result
            
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
        self.ui_main.art_alb["nowart"] = artist
        self.ui_main.art_alb["nowalb"] = album
        self.ui_main.art_alb["title"] = title
        

class MainWindow(Ui_MainWindow, QMainWindow): 
    """
    Where everything starts from, mostly.
    """    
    
    def __init__(self, parent = None):
        """
        Initialisation of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
        super(MainWindow,self).__init__()
        
        
        self.__settings_init()
        
        
        self.build_lock = self.delete_lock = False
        self.art_alb = {"oldart":None, "oldalb":None, 
                        "nowart":None, "nowalb":None, 
                        "title":None, "oldtit":None} 
        self.old_pos = 0
        
        # The file formats that can be encoded
        self.audio_formats = Formats.Formats().available()
        self.format_filter = ["*.%s" % fmat for fmat in self.audio_formats]
        
        
        # TODO: change ui settings based on saved states/options. QSession
        self.setupUi(self)
        try:
            self.media_db = CollectionDb("main")
        except StandardError, err:
            self.__reset_db_default(err)
            
        try:
            # FIXME: why is this needed on startup?
            self.build_db_thread = Builddb(self)
        except StandardError, err:
            self.__reset_db_default(err)
            
        self.info_thread = Getinfo(self)
        self.html_thread = Getwiki()
        
            
        self.del_thread = DeleteFiles(self)
        self.extras = Extraneous()
        self.meta = Tagging(self.audio_formats)
        self.player = Backend.AudioBackend(self)
        self.playlisting = Playlist(self)
        self.xtrawdgt = SetupExtraWidgets(self)
        self.tracking = Track(self)
        self.wdgt_manip = WidgetManips(self)
        self.finishes = Finishers(self)
        self.play_hist = PlaylistHistory()
        self.__playlist_remembered()
        self.__audiocd_setup()
        self.__tray_menu_appearance()
        
        # new style signalling
        self.build_db_thread.finished.connect(self.finishes.db_build)
        self.play_actn.toggled.connect(self.play_bttn.setChecked)
        self.actionNext_Track.triggered.connect(self.next_bttn.click)
        self.prev_track_actn.triggered.connect(self.prev_bttn.click)
        self.stop_actn.triggered.connect(self.prev_bttn.click)
        self.stat_bttn.pressed.connect(self.quit_build)
        hdr = self.track_tbl.horizontalHeader()
        hdr.sectionClicked.connect(self.playlisting.track_sorting)
        self.collect_tree_hdr.sectionClicked.connect(self.__collection_sort)
        self.html_thread.got_wiki.connect(self.finishes.set_wiki)
        self.build_db_thread.progress.connect(self.stat_prog.setValue)
        self.del_thread.deleted.connect(self.wdgt_manip.setup_db_tree)        
        self.info_thread.got_info.connect(self.__bodger)
        # Cannot do this for some reason
        #self.info_thread.got_info.connect(self.info_view.setHtml)
        
        # Makes the collection search line-edit have the keyboard focus
        self.search_collect_edit.setFocus()
        self.wdgt_manip.setup_db_tree()
        self.wdgt_manip.pop_playlist_view() 

        
    def __reset_db_default(self,err):
        err = "Database Error: %s. Setting Database to default" % str(err)
        err_msg = QErrorMessage()
        err_msg.showMessage(str(err))
        if err_msg.exec_():                
            self.sets_db.add_database_setting("type", "SQLITE")
            self.media_db.media_db.removeDatabase("main")
            self.media_db = CollectionDb("main")
        
    def __tray_menu_appearance(self):
        if self.sets_db.get_interface_setting("trayicon") == "True":
            self.tray_icon.show()
        else:
            self.tray_icon.hide()
        
    # FIXME: HACK ALERT!!!
    def __bodger(self, html):
        """
        needed as the signal cannot be directly connected to
        the webview for unknown reasons
        """    
        self.info_view.setHtml(html)
        
    def __setup_watcher(self):
        watch = self.sets_db.get_collection_setting("watch")  == "True"
        recur = self.sets_db.get_collection_setting("recursive")  == "True"
        
        if (self.media_dir is None) or (watch is False):
            return
        
        try:
            # To stop the possibly already running thread
            self.watch_thread.exit()
        except AttributeError:
            pass
            
        print("WATCHING: ", self.media_dir[0])
        self.watch_thread = Watcher(self)
        self.watch_thread.set_values(self.media_dir, WATCHTIME, recur)
        self.watch_thread.start()
        self.watch_thread.creations.connect(self.__files_created)
        self.watch_thread.deletions.connect(self.__files_deleted)
        
    def __files_deleted(self, deletions):
        """
        When something is deleted in the collection dir
        the filename is put into a list. This list checked every 60secs
        and fed into the DB
        """
        self.del_thread.set_values(deletions)
        self.del_thread.start()
            
    def __files_created(self, creations):
        """
        Via the watcher, newly created/changed files are sent
        to the db to be added or updated
        """
        self.build_db_thread.set_values(None, self.audio_formats, "create", 
                                        creations)
        self.stat_lbl.setText("Auto-Scanning")
        self.stat_prog.setValue(0)
        self.build_db_thread.start()
        
    def __dirs_setup(self):
        """
        Load the collection directories into self
        """
        include = []
        exclude = []
        inc = self.sets_db.get_collection_setting("include")
        exc = self.sets_db.get_collection_setting("exclude")        
        if inc is not None:
            include = inc.split(",")
        if exc is not None:
            exclude = exc.split(",")
        self.media_dir = (include, exclude)
        
    def __settings_init(self):
        """
        Things to perform on startup
        """
        self.sets_db = Settings()
        self.__dirs_setup()
        self.__setup_watcher()
  
        
        
    def __playlist_remembered(self):
        """
        Load the playlist auto-saved(optional)
        on last shutdown
        """
        if self.sets_db.get_interface_setting("remember") == "False":
            return
        tracks = self.media_db.playlist_tracks("!!##gereqi.remembered##!!")
        if len(tracks) > 0:
            self.playlisting.add_list_to_playlist(tracks)
                
    def __audiocd_setup(self):
        """
        As pyCDDB is optional only load cd
        modules if possible
        """
        try:
            self.acd = Cdrom.AudioCD()
        except:
            print("Probably missing python-cddb")
            self.play_cd_actn.setVisible(False)
            
            
    def tray_tooltip(self):
        if self.play_bttn.isChecked() == False:
            msg = "Paused"
        # Puts the current track info in tray tooltip
        else:
            info = self.playlisting.current_row_info()
            msg = "%s by %s" % (info["Title"], info["Artist"])
        self.tray_icon.setToolTip(msg) 
        
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
        now = item.text(0)
        par = item.parent()
        track = album = artist = None
        mode = self.__collection_mode()
        
        if mode == "artist":
            # When we haven't selected an artist
            if par is not None:
                par_par = par.parent()
                # When we select an individual track
                if par_par is not None:
                    artist = par_par.text(0)
                    album = par.text(0)
                    track = now
                # When we've selected an album
                else:
                    album = now
                    artist = par.text(0)
                    
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
                file_name = self.media_db.get_album_file(par.text(0), now)
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
        if track is None:
            return
        self.player.audio_object.stop()
        self.player.audio_object.load(track)
        # Checks to see if the playbutton is in play state
        if self.play_bttn.isChecked():
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
                if (queued != highlighted) and paused: 
                    self.player.audio_object.load(str(highlighted.toUtf8()))
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
                elif paused:
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
        self.tray_tooltip()
        
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
            if self.play_bttn.isChecked():
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
        value = (value / 100.0)
        self.player.audio_object.set_volume(value)
    
    #TODO: not sure if the DB changes are made
    # i.e going from sqlite to mysql or v'-v'
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
            try:
                self.media_db.restart_db("main")
            except StandardError, err:
                # The user has entered duff DB values
                self.__reset_db_default(err)
                
            self.wdgt_manip.setup_db_tree()
            self.wdgt_manip.pop_playlist_view()
            self.__tray_menu_appearance()
            
    @pyqtSignature("")
    def on_actionRescan_Collection_triggered(self):
        """
        Scans through a directory and looks for supported media,
        extracts metadata and adds them to the database,hopefully.
        Really needs to be done in a separate thread as scan could
        take a while.
        """
        print("Deleting media DB and rebuilding") 
        self.collect_tree.clear()
        self.create_collection(fresh=True)
    
    @pyqtSignature("")
    def on_actionQuit_triggered(self):
        """
        Closing Down. Maybe some database interaction.
        """
        if self.sets_db.get_interface_setting("remember") == "True":
            play_name = "!!##gereqi.remembered##!!"
            tracks = self.playlisting.gen_file_list()
            self.media_db.playlist_delete(play_name)
            for trk in tracks:
                self.media_db.playlist_add(play_name,trk)
        self.media_db.shutdown()
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
                        
        if mfiles is None:
            return
        
        for item in mfiles:
            ender = item.split(".")[-1]
            if ender.toLower() in self.audio_formats:
                self.playlisting.add_to_playlist(item)

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
        self.actionUndo.setEnabled(True)
        self.clear_trktbl_bttn.setEnabled(False)
        
    @pyqtSignature("")
    def on_actionSave_triggered(self):
        """
        Save current playlist
        """
        if self.track_tbl.rowCount() < 1:
            return
        
        play_name = QInputDialog.getText(None,
                                         QString("Save Playlist"),
                                         QString("Enter a name for the playlist:"),
                                         QLineEdit.Normal)
         
        if play_name[1] is None:
            # User clicked cancel
            return
        
        if len(self.media_db.playlist_tracks(play_name[0])) > 1:        
            msg = QMessageBox.warning(None,
                QString("Overwrite Playlist?"),
                QString("""A playlist named '%s' already exists. Do you want to overwrite it?"""  
                            % play_name[0]),
                            QMessageBox.StandardButtons(
                                QMessageBox.Cancel | 
                                QMessageBox.No | 
                                QMessageBox.Yes))
            
            if msg == QMessageBox.Cancel:
                return
            elif msg == QMessageBox.No:
                self.on_save_trktbl_bttn_clicked()
                
        tracks = self.playlisting.gen_file_list()            
        for track in tracks:
            self.media_db.playlist_add(play_name[0], track)
        self.wdgt_manip.pop_playlist_view()
    
    
    @pyqtSignature("")
    def on_clear_trktbl_bttn_clicked(self):
        """
        Clears current playlist and sets focus
        on the search linedit
        """
        self.on_actionClear_triggered()
        self.search_collect_edit.setFocus()
        self.next_trktbl_bttn.setEnabled(False)
        self.actionRedo.setEnabled(False)
        self.player.recently_played = []
    
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
            palette = self.track_tbl.palette()
            columns = self.track_tbl.columnCount()
            searched = self.track_tbl.findItems(srch_str, Qt.MatchContains)
            # TODO: make readable
            for search in searched:
                row = search.row()
                if row in rows:
                    continue
                rows.append(row)
                for col in range(columns):
                    item = self.track_tbl.item(row, col)
                    orig = palette.highlight().color().getRgb()
                    new_col = map(lambda x : 255-x, orig)
                    item.setBackgroundColor(QColor(new_col[0],new_col[1],new_col[2], 128))
                        
            for row in range(self.track_tbl.rowCount()):
                if row in rows:
                    continue
                for col in range(columns):
                    item = self.track_tbl.item(row, col)
                    if row % 2:
                        item.setBackgroundColor(palette.alternateBase().color())
                    else:
                        item.setBackgroundColor(palette.base().color())
        else:
            self.playlisting.tracknow_colourise()
                
    @pyqtSignature("bool")
    def on_mute_bttn_toggled(self, checked):
        """
        Mutes audio output and changes button icon accordingly
        """
        self.player.audio_object.mute(checked)
        if checked:
            icon = QIcon(QIcon().fromTheme("process-stop"))
        else:
            vol = (self.volume_sldr.value() / 100.0)
            icon = QIcon().fromTheme("player-volume",QIcon(":/icons/audio-card.png"))
            # The volume-slider may have changed since being muted            
            self.player.audio_object.set_volume(vol)
            
        self.mute_bttn.setIcon(icon)
      
    @pyqtSignature("")  
    def on_progress_sldr_sliderReleased(self):
        """
        Set's an internal seek value for tick() to use
        """
        val = self.progress_sldr.value()
        self.player.audio_object.seek(val)
        self.old_pos = val
        
    @pyqtSignature("int")
    def on_progress_sldr_actionTriggered(self,action):
        ok_actions = [1,2,3,4]
        if action in ok_actions:
            #Does what's needed
            self.on_progress_sldr_sliderReleased()
        elif action == 7:
            val = self.progress_sldr.value()
            self.player.timeval_to_label(val)

    
    @pyqtSignature("")
    def on_actionUpdate_Collection_triggered(self):
        """
        Updates collection for new files. Ignore files already in database
        Removes files if no longer in filesystem
        """
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
        # as self.player.audio_object.play(), just cleaner overall
        self.play_bttn.setChecked(True) 
        self.play_action.setChecked(True)
        
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
                artist = par.text(0)
                album = item.text(0)
            else:
                artist = item.text(0)
                album = None
            
            if (album is not None) and (item.childCount() == 0):
                # Adding tracks to album
                tracks = self.media_db.get_titles(artist, album, filt_time)
               
                for trk in tracks:
                    track = QTreeWidgetItem([ trk["title"] ] )                    
                    item.addChild(track)
      
           # Adding albums to the artist 
           # i.e. the parent has no children    
            elif item.childCount() == 0: 
                albums = self.media_db.get_albums(artist, filt_time)                    
                for alb in albums:
                    cover = self.extras.get_cover_source(artist,alb,True, False)
                    
                    if not cover:
                        cover = ":icons/nocover.png"
                    else:
                        cover = cover.remove("file://")
                    
                    album = QTreeWidgetItem([alb])
                    album.setIcon(0,QIcon(cover))
                    album.setChildIndicatorPolicy(0)
                    item.addChild(album)
                
        else:
            if par is not None:
                album = par.text(0)
                track = item.text(0)
            else:
                album = item.text(0)
                track = None
            
            if (track is None) and (item.childCount() == 0):
                tracks = self.media_db.get_album_titles(album,filt_time) 
                             
                for trk in tracks:      
                    track = QTreeWidgetItem([trk])
                    item.addChild(track)
                
                
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
        The Gereqi about dialog
        """
        About(self).show()
            
    @pyqtSignature("")
    def on_clear_search_bttn_clicked(self):
        """
        Clears the playlist search filter
        """
        # FIXME: the current track needs to re-highlighted
        self.search_trktbl_edit.clear()
        self.playlisting.highlighted_track()
        
    @pyqtSignature("")
    def on_play_cd_actn_triggered(self):
        """
        add tracks from cd
        """
        try:
            cd_tracks = self.acd.get_info()
        except StandardError,err:
            if str(err) == "No medium found":
                msg_box = QMessageBox()
                msg_box.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ok)
                msg_box.setText("Add a CD")
                msg_box.setWindowTitle("No medium found")
                if (msg_box.exec_() == QMessageBox.Ok):
                    self.on_play_cd_actn_triggered()
                    return
                else:
                    return
            else:
                return
        self.playlisting.add_list_to_playlist(cd_tracks)                
        self.clear_trktbl_bttn.setEnabled(True)
                
    @pyqtSignature("")
    def on_save_trktbl_bttn_clicked(self):
        """
        Based on what is in the playlist and chosen name, it'll
        get put into the database
        """
        self.on_actionSave_triggered()
            
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_playlist_tree_itemDoubleClicked(self, item, column):
        """
        Slot documentation goes here.
        """
        try:
            par = item.parent().text(0)
        except  AttributeError:
            return
        
        if par == "Podcasts":
            return
            
        elif par == "Radio Streams":
            return
            
        elif par == "Playlists":
            playlist = item.text(column)
            tracks = self.media_db.playlist_tracks(playlist)
            self.playlisting.add_list_to_playlist(tracks)
            self.clear_trktbl_bttn.setEnabled(True)
        else:
            new_par = item.parent().parent()            
            if new_par.text(0) == "Playlists":
                title, artist = item.text(0).split(" - ")
                track = self.media_db.search_by_titandart(title, artist)
                if len(track) > 0:
                    self.playlisting.add_to_playlist(track[0])
                
            
    @pyqtSignature("bool")
    def on_delete_playlist_bttn_clicked(self, checked):
        """
        Delete a selected playlist from the DB
        """
        playlist = self.playlist_tree.selectedItems()
        if len(playlist) > 0:
            self.media_db.playlist_delete(playlist[0].text(0))
            self.wdgt_manip.pop_playlist_view()
            
    
    @pyqtSignature("bool")
    def on_rename_playlist_bttn_clicked(self, checked):
        """
        Rename the selected playlist
        """
        playlist = self.playlist_tree.selectedItems()
        try:
            par = playlist[0].parent().text(0)
        except  AttributeError:
            return
        except IndexError:
            return
            
        if (len(playlist) < 1) and (par not in ["Podcasts", "Radio Streams",  "Playlists"]):
            return
        
        new_name = QInputDialog.getText(\
            None,
            QString("Rename Playlist"),
            QString("Rename the playlist to:"),
            QLineEdit.Normal)
        
        # Checks if you entered a non-zero length name and that you clicked 'ok'
        if (new_name[1] is None) and (len(new_name[0]) < 1):
            return
        
        #get all the tracks in the selected playlist
        tracks = self.media_db.playlist_tracks(playlist[0].text(0))
        # delete the old playlist
        self.media_db.playlist_delete(playlist[0].text(0))
        # add the tracks back in but with a new name, probably cleaner using an sql query
        for track in tracks:
            self.media_db.playlist_add(new_name[0], track)
        self.wdgt_manip.pop_playlist_view()
            
    @pyqtSignature("bool")
    def on_prev_trktbl_bttn_clicked(self, checked):
        """
        The previous-track button does various
        actions dependin of the payback state
        """
        self.playlisting.clear()

        if self.play_hist.position < len(self.play_hist.stack):
            self.next_trktbl_bttn.setEnabled(True)
            self.actionRedo.setEnabled(True)
            
        tracks, last = self.play_hist.last_list()
        self.playlisting.add_list_to_playlist(tracks)
        self.clear_trktbl_bttn.setEnabled(True)
        
        if last:
            self.prev_trktbl_bttn.setEnabled(False)
            self.actionUndo.setEnabled(False)
        
    @pyqtSignature("bool")
    def on_next_trktbl_bttn_clicked(self, checked):
        """
        The next-track button does various
        actions dependin of the payback state
        """
        self.playlisting.clear()
        self.prev_trktbl_bttn.setEnabled(True)
        self.actionUndo.setEnabled(True)
        tracks, first = self.play_hist.next_list()
        self.playlisting.add_list_to_playlist(tracks)
        self.clear_trktbl_bttn.setEnabled(True)
        
        if first:
            self.next_trktbl_bttn.setEnabled(False)
            self.actionRedo.setEnabled(False)
            
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
            
        
    @pyqtSignature("QModelIndex")
    def on_filesystem_tree_doubleClicked(self, index):
        """
        This takes the filesystem_tree item and deduces whether
        it's a file or directory and populates playlist if possible
        """
        #TODO: check to see if it's avail in db 1st otherwise if it isn't exceptions occur
        if self.dir_model.isDir(index):
            fname = self.dir_model.filePath(index)
            searcher = QDir(fname)
            searcher.setFilter(QDir.Files)
            searcher.setNameFilters(self.format_filter)
            tracks = [item.absoluteFilePath() for item in searcher.entryInfoList()]
            self.playlisting.add_list_to_playlist(tracks)
            self.clear_trktbl_bttn.setEnabled(True)
        else:
            fname = self.dir_model.filePath(index)
            self.playlisting.add_to_playlist(fname)
            self.clear_trktbl_bttn.setEnabled(True)
            
    @pyqtSignature("QModelIndex")
    def on_filesystem_tree_expanded(self):
        """
        Resizes the filesystem_tree to it's contents.
        Because of the '0' this seperate method is needed
        """
        self.filesystem_tree.resizeColumnToContents(0)
        
    @pyqtSignature("")
    def on_actionUndo_triggered(self):
        self.prev_trktbl_bttn.click()
        
    @pyqtSignature("")
    def on_actionRedo_triggered(self):
        self.next_trktbl_bttn.click()

    def aboutToQuit(self):
        print "SPAM"
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
        self.progress_sldr.setPageStep(self.tracking.play_time/10)
        self.progress_sldr.setSingleStep(self.tracking.play_time/25)
        self.t_length = QTime(0, (self.tracking.play_time / 60000) % 60, 
                              (self.tracking.play_time / 1000) % 60)
            
    def minimise_to_tray(self, state):
        """
        Does what it says.
        """
        if state:
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
        mode = "redo" if fresh else "update"
        # If the dialog is cancelled in last if statement the below is ignored
        if self.media_dir is not None:
            self.stat_bttn.setEnabled(True)
            self.build_db_thread.set_values(self.media_dir, self.audio_formats,
                                            mode)
            self.stat_lbl.setText("Scanning Media")
            self.stat_prog.setValue(0)
            self.build_db_thread.start()
    
    # FIXME: this looks horrendously crap
    def set_info(self):
        """
        The wikipedia page + album art to current artist playing
        Typically done on track-change
        """
        art_change = self.art_alb["nowart"] != self.art_alb["oldart"] 
        alb_change = self.art_alb["nowalb"] != self.art_alb["oldalb"]
        tit_change = self.art_alb["title"] != self.art_alb["oldtit"]
        albs = self.media_db.get_albums(self.art_alb["nowart"])
        
        # Wikipedia info
        if art_change and (self.art_alb["nowart"] is not None):
            # passes the artist to the thread
            self.html_thread.set_values(self.art_alb["nowart"]) 
            # starts the thread
            self.html_thread.start() 
            self.art_alb["oldart"] = self.art_alb["nowart"]

        # Album art
        if alb_change and (self.art_alb["nowalb"] is not None):           
            self.info_thread.set_values(artist=self.art_alb["nowart"],  
                                        album=self.art_alb["nowalb"], 
                                        title=self.art_alb["title"],
                                        check=True, albums=albs,
                                        )
            self.info_thread.start()
            self.art_alb["oldalb"] = self.art_alb["nowalb"]
            
        elif tit_change and (self.art_alb["title"] is not None):
            self.info_thread.set_values(artist=self.art_alb["nowart"],
                                        album=self.art_alb["nowalb"],
                                        title=self.art_alb["title"],
                                        check=False, albums=albs,
                                        )
            self.info_thread.start()
            self.art_alb["oldalb"] = self.art_alb["nowalb"]
            
        # Show the context browser
        if self.sets_db.get_interface_setting("context-change") == "True":
            self.vertical_tabs.setCurrentIndex(0)

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
        if self.sets_db.get_interface_setting("trayicon") == "False":
            return
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()

    def __time_filt_now(self):
        """
        Based on the combobox selection, the collection
        browser is filtered by addition date
        """
        index = self.collect_time_box.currentIndex()
        calc = lambda val: int(round(time.time() - val))
        now = time.localtime()
        today_secs = ( ( (now[3] * 60) + now[4] ) * 60 ) + now[5]
        filts = [ today_secs, 604800, 2419200, 7257600, 31557600]   
        if index > 0:
            return calc(filts[index - 1])
        else:
            return 0
        
    def __collection_mode(self):
        # TODO: maybe change the delgate as in album mode the
        # tracks are v big
        text_now = self.collect_tree.headerItem().text(0)
        if text_now == "Artist/Album":            
            return "artist"
        else:
            
            return "album"
        
    def __collection_sort(self, p0):
        mode = self.__collection_mode()
        if mode == "artist":
            self.wdgt_manip.mydel.mode = "album"
            self.collect_tree.headerItem().setText(0, "Album/Artist")
            
        else:
            self.wdgt_manip.mydel.mode = "artist"
            self.collect_tree.headerItem().setText(0, "Artist/Album")

        self.wdgt_manip.setup_db_tree()
