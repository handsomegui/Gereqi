# -*- coding: utf-8 -*-
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
from audio import Backend, Formats, MediaTypes
from storage.Settings import Settings
from storage.Collection import CollectionDb
from information.tagging import Tagging
from information.cue_sheet import CueSheet
from icons.configuration import MyIcons
from widgets.collection_tree import CollectionTree,CollectionTreeItem
try:
    from audio import Cdrom
    CDS_OK = True
except ImportError:
    print("Missing CDRom dependencies")
    CDS_OK = False
from random import choice
import time
from os import path
from threads import Builddb, Finishers, Watcher, DeleteFiles, WikiPage, InfoPage
from Ui_interface import Ui_MainWindow
from configuration import Configuration
import extraneous
from extrawidgets import SetupExtraWidgets, WidgetManips
from about import About

# The folder watcher poll-time in seconds
WATCHTIME = 30 


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
        self.parent = parent
        
        self.__settings_init()
        
        self.build_lock = self.delete_lock = False
        self.art_alb = {"oldart":   None, "oldalb": None, 
                        "nowart":   None, "nowalb": None, 
                        "title":    None, "oldtit": None} 
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
                
                
        self.collect_tree = CollectionTree(self.collectionTab)
        self.verticalLayout_2.addWidget(self.collect_tree)
        self.collect_tree.populate()
            
        self.del_thread = DeleteFiles(self)
        self.meta = Tagging(self.audio_formats)
        
        self.xtrawdgt = SetupExtraWidgets(self)
        self.player = Backend.AudioBackend(self)
        self.wdgt_manip = WidgetManips(self)
        self.finishes = Finishers(self)
        self.__tray_menu_appearance()
        self.wiki_thread = WikiPage()
        self.infopage_thread = InfoPage()
        
        # new style signalling
        self.build_db_thread.finished.connect(self.finishes.db_build)
        self.play_actn.toggled.connect(self.play_bttn.setChecked)
        self.actionNext_Track.triggered.connect(self.next_bttn.click)
        self.prev_track_actn.triggered.connect(self.prev_bttn.click)
        self.stop_actn.triggered.connect(self.prev_bttn.click)
        self.stat_bttn.pressed.connect(self.quit_build)
        self.collect_tree.header().sectionClicked.connect(self.collection_sort)
        self.collect_tree.items_for_playlist.connect(self.__items_for_playlist)
        self.build_db_thread.progress.connect(self.stat_prog.setValue)
        self.del_thread.deleted.connect(self.collect_tree.populate)        
        self.wiki_thread.html.connect(self.setWiki)
        self.infopage_thread.html.connect(self.__set_infopage)
        self.actionQuit.triggered.connect(self.shutdown)
        self.playlist_table.play_this.connect(self.__load_and_play)
        self.playlist_table.populated.connect(self.__ready_to_go)
        
        # Makes the collection search line-edit have the keyboard focus
        self.search_collect_edit.setFocus()
        self.wdgt_manip.pop_playlist_view()
        
        self.play_cd_actn.setVisible(CDS_OK)
        self.icons = MyIcons()
        
        
    def __ready_to_go(self):
        self.clear_trktbl_bttn.setEnabled(True)
    
    def __load_and_play(self, track, type):
        self.player.audio_object.stop()
        self.player.audio_object.clear()
        self.player.audio_object.load(track, type)
        self.player.audio_object.play()
        self.stop_bttn.setEnabled(True)
        self.play_bttn.setChecked(True)
        self.wdgt_manip.icon_change("play")

    def __items_for_playlist(self, items):
        self.playlist_table.tracks += items
        self.playlist_table.update()

    def __set_infopage(self, html):
        self.info_view.setHtml(html)        
        

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
        
    def __collection_mode(self):
        text_now = self.collect_tree.headerItem().text(0)
        if text_now == "Artist/Album":            
            return "artist"
        else:            
            return "album"
        
    def __volume_icon(self,value=None):
        value = value if value else self.volume_sldr.value()
        if (value > 66):
            return self.icons.icon("volume-max")
        elif (value > 33):
            return self.icons.icon("volume-mid")
        elif (value > 0):
            return self.icons.icon("volume-low")
        else:
            return self.icons.icon("mute")
   
    def __setup_watcher(self):
        watch = (self.sets_db.get_collection_setting("watch")  == "True")
        recur = (self.sets_db.get_collection_setting("recursive")  == "True")
        
        if (self.media_dir is None) or (watch is False):
            return
        
        try:
            # To stop the possibly already running thread
            self.watch_thread.exit()
        except AttributeError:
            pass
            
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
        if inc:
            include = inc.split(",")
        if exc:
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
        tracks = self.media_db.last_playlist()
        if len(tracks) > 0:
            self.playlist_table.add_list_to_playlist(tracks)
                
    def tray_tooltip(self):
        if self.play_bttn.isChecked():
            info    = self.playlist_table.current_track()
            msg     = "%s by %s" % (info.title, info.artist)
            
        # Puts the current track info in tray tooltip
        else:
            msg = "Paused"
        self.tray_icon.setToolTip(msg) 
        
        
        
    @pyqtSignature("QString")
    def setInfo(self, html):
        """
        needed as the signal cannot be directly connected to
        the webview for unknown reasons
        """            
        self.info_view.setHtml(html)
        self.horizontal_tabs.setTabEnabled(2,True)
        
        
    def setWiki(self,html):
        """
        Things to perform when a new wikipedia page is retrieved
        """
        if html != "None":
            self.horizontal_tabs.setTabEnabled(2, True)
            self.wiki_view.setHtml(html)
        else:
            self.horizontal_tabs.setTabEnabled(2, False)
        
        
    @pyqtSignature("QString")
    def on_search_collect_edit_textChanged(self, srch_str):
        """
        This allows the filtering of the collection tree
        """
        self.collect_tree.text_filter = srch_str
        self.collect_tree.populate()
    
    @pyqtSignature("")
    def on_prev_bttn_pressed(self):
        """
        Skip to previous track in viewable playlist
        if possible
        """
        track = self.playlist_table.previous()
        # See if there is a track previous
        if not track:
            return
        self.player.audio_object.stop()
        self.player.audio_object.clear()
        self.player.audio_object.load(track)
        # Checks to see if the playbutton is in play state
        if self.play_bttn.isChecked():
            self.player.audio_object.play()

    @pyqtSignature("bool")
    def on_play_bttn_toggled(self, checked):
        """
        The play button either resumes or starts playback.
        Not possible to play a highlighted row.
        """
        paused  = self.player.audio_object.is_paused()
        playing = self.player.audio_object.is_playing()
        
        if checked:
            # The button is set
            queued  = self.player.audio_object.current_source()
            trk     = self.playlist_table.current_track()
            if trk:      
                # Something in the playlist is selected                
                if (queued['source'] != trk.filename) and paused: 
                    # The track in backend is not the same as selected and paused
                    self.player.audio_object.load(trk.filename)
                elif queued['type'] == MediaTypes.EMPTY:
                    # Nothing already loaded
                    cur_trk = self.playlist_table.current_track()
                    if cur_trk:
                        # A row is selected
                        self.player.audio_object.load(cur_trk)                    
                    else:
                        # Nothing to play. Just reset the play button and stop here
                        self.play_bttn.setChecked(False)
                        return
                elif paused:
                    # Just unpausing
                    # Makes sure the statusbar text changes from
                    # paused back to the artist/album/track string
                    self.generate_info()
                                        
                self.player.audio_object.play()
                self.stop_bttn.setEnabled(True)
                self.wdgt_manip.icon_change("play")
            else:
                # Nothing to play
                self.play_bttn.setChecked(False)
                return
        else:
            # The button is unset
            if playing:
                # pause playback
                self.player.audio_object.pause()
                
            self.wdgt_manip.icon_change("pause")
            if self.playlist_table.currentRow() >= 0:
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
        self.player.audio_object.clearQueue()
        self.play_bttn.setChecked(False)
        self.stop_bttn.setEnabled(False)
        
    @pyqtSignature("")
    def on_next_bttn_pressed(self):
        """
        Go to next item in playlist(down)
        """
        track = self.playlist_table.next()
        if track:
            self.player.audio_object.stop() 
            self.player.audio_object.clear() 
            self.player.audio_object.load(track)
            self.player.audio_object.play()
        else:
            # TODO: some tidy up thing could go here
            return
     
    @pyqtSignature("int")
    def on_volume_sldr_valueChanged(self, value):
        """
        Self explanatory
        """
        if not self.mute_bttn.isChecked():
            self.mute_bttn.setIcon(self.__volume_icon(value))
        value /= 100.0
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

    
    def shutdown(self):
        self.parent.setOverrideCursor(QCursor(Qt.BusyCursor))
        if self.sets_db.get_interface_setting("remember") == "True":
            tracks = self.playlist_table.gen_file_list()
            self.media_db.save_last_playlist(tracks)
        self.media_db.shutdown()
        exit()
    
    @pyqtSignature("")
    def on_play_media_actn_triggered(self):
        """
        Extract music files and shove into current playlist.
        """        
        filts  = " ".join(self.format_filter)
        # TODO: use the below. Returns a StandardLocation that won't convert
        # to string so it's useless
        #QDesktopServices.MusicLocation
        mfiles = QFileDialog.getOpenFileNames(\
                        self, 
                        "Select Music Files",
                        "/home/", 
                        "Audio Files : %(filt)s (%(filt)s)" % {'filt': filts}
                        )       
                        
        for item in mfiles[0]:
            self.playlist_table.add_to_playlist(item[0])

    @pyqtSignature("bool")
    def on_minimise_tray_actn_toggled(self, checked):
        self.minimise_to_tray(checked)
    
    @pyqtSignature("")
    def on_actionClear_triggered(self):
        """
        Clear current playlist and if no music playing
        clear self.player.audio_object
        """
        self.playlist_table.clear_rows()
        self.playlist_table.tracks = []
        self.prev_trktbl_bttn.setEnabled(True)
        self.actionUndo.setEnabled(True)
        self.clear_trktbl_bttn.setEnabled(False)
        
    @pyqtSignature("")
    def on_actionSave_triggered(self):
        """
        Save current playlist
        """
        if self.playlist_table.rowCount() < 1:
            return
        
        play_name = QInputDialog.getText(None,
                                         "Save Playlist",
                                         "Enter a name for the playlist:",
                                         QLineEdit.Normal)
        if not play_name[1]:
            # User clicked cancel
            return
        
        if len(self.media_db.playlist_tracks(play_name[0])) > 1:        
            msg = QMessageBox.warning(None,
                "Overwrite Playlist?",
                """
                A playlist named '%s' already exists. 
                Do you want to overwrite it?
                """  
                            % play_name[0],
                            QMessageBox.StandardButtons(
                                QMessageBox.Cancel | 
                                QMessageBox.No | 
                                QMessageBox.Yes))
            
            if msg == QMessageBox.Cancel:
                return
            elif msg == QMessageBox.No:
                self.on_save_trktbl_bttn_clicked()
                
        tracks = self.playlist_table.gen_file_list()            
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
        now = self.playlist_table.current_row()
        if now:
            self.playlist_table.highlighted_track()
        
        # Checks if the search edit isn't empty
        #TODO: QString strip+length
        if len(str(srch_str).strip()) > 0:
            rows = []
            palette = self.playlist_table.palette()
            columns = self.playlist_table.columnCount()
            searched = self.playlist_table.findItems(srch_str, Qt.MatchContains)
            # TODO: make readable
            for search in searched:
                row = search.row()
                if row in rows:
                    continue
                rows.append(row)
                for col in range(columns):
                    item = self.playlist_table.item(row, col)
                    orig = palette.highlight().color().getRgb()
                    new_col = map(lambda x : 255-x, orig)
                    item.setBackground(QColor(new_col[0],new_col[1],new_col[2], 128))
                        
            for row in range(self.playlist_table.rowCount()):
                if row in rows:
                    continue
                for col in range(columns):
                    item = self.playlist_table.item(row, col)
                    if row % 2:
                        item.setBackground(palette.alternateBase().color())
                    else:
                        item.setBackground(palette.base().color())
                
    @pyqtSignature("bool")
    def on_mute_bttn_toggled(self, checked):
        """
        Mutes audio output and changes button icon accordingly
        """
        self.player.audio_object.mute(checked)
        icon = self.icons.icon("mute") if checked else self.__volume_icon()      
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
        self.collect_tree.time_filter = self.wdgt_manip.time_filter_value()
        self.collect_tree.populate()
        
        
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
        self.playlist_table.highlighted_track()
        
    @pyqtSignature("")
    def on_play_cd_actn_triggered(self):
        """
        add tracks from cd
        """
        acd = Cdrom.AudioCD()
        try:
            cd_tracks = acd.get_info()
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
        self.playlist_table.add_list_to_playlist(cd_tracks)                
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
            if path.splitext(tracks[0])[-1].lower() == ".cue":
                # sort out the cuesheet
                cue_now = CueSheet(tracks[0])
                for track in cue_now.tracks:
                    info =  {"Track":   track.number,  
                            "Title":    track.title,
                            "Artist":   track.performer, 
                            "Album":    cue_now.title,
                            "Year":     cue_now.year, 
                            "Genre":    cue_now.genre,
                            "Length":   "0", 
                            "Bitrate":  "0", 
                            "FileName": cue_now.path + track.file_name}
                    self.playlist_table.add_to_playlist(track.file_name, info)
            else:
                self.playlist_table.add_list_to_playlist(tracks)
            self.clear_trktbl_bttn.setEnabled(True)
            
        elif par == "Auto":
            if item.text(0) == "Top 10":
                tracks = self.media_db.top_tracks()
                self.playlist_table.add_list_to_playlist(tracks)
                self.clear_trktbl_bttn.setEnabled(True)
        else:
            new_par = item.parent().parent()            
            if new_par.text(0) == "Playlists":
                title, artist = item.text(0).split(" - ")
                track = self.media_db.search_by_titandart(title, artist)
                if len(track) > 0:
                    self.playlist_table.add_to_playlist(track[0])
                
            
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
            "Rename Playlist",
            "Rename the playlist to:",
            QLineEdit.Normal)
        # Checks if you entered a non-zero length name and that you clicked 'ok'
        if (not new_name[1]) or (len(new_name[0]) < 1):
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
        self.playlist_table.clear()

        if self.play_hist.position < len(self.play_hist.stack):
            self.next_trktbl_bttn.setEnabled(True)
            self.actionRedo.setEnabled(True)
            
        tracks, last = self.play_hist.last_list()
        self.playlist_table.add_list_to_playlist(tracks)
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
        self.playlist_table.clear()
        self.prev_trktbl_bttn.setEnabled(True)
        self.actionUndo.setEnabled(True)
        tracks, first = self.play_hist.next_list()
        self.playlist_table.add_list_to_playlist(tracks)
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
            self.playlist_table.add_list_to_playlist(tracks)
            self.clear_trktbl_bttn.setEnabled(True)
        else:
            fname = self.dir_model.filePath(index)
            self.playlist_table.add_to_playlist(fname)
            self.clear_trktbl_bttn.setEnabled(True)
            
    @pyqtSignature("QModelIndex")
    def on_filesystem_tree_expanded(self, index):
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
        self.build_db_thread.stop()

    def set_prog_sldr(self):
        """
        Linked to the current time of
        track being played
        """
        minu,sec = self.playlist_table.current_track().length.split(":")
        
        play_time = 1000 * ((int(minu) * 60) + int(sec))
#        self.progress_sldr.setPageStep(play_time/10)
#        self.progress_sldr.setSingleStep(play_time/25)
        self.t_length = QTime(0, (play_time / 60000) % 60, (play_time / 1000) % 60)
            
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
        if self.media_dir:
            self.stat_bttn.setEnabled(True)
            self.build_db_thread.set_values(self.media_dir, self.audio_formats,
                                            mode)
            self.stat_lbl.setText("Scanning Media")
            self.stat_prog.setValue(0)
            self.build_db_thread.start()
    
    # FIXME: this looks horrendously crap
    # FIXME: broken. only works for 1st track that is played
    def set_info(self):
        """
        The wikipedia page + album art to current artist playing
        Typically done on track-change
        """
        
        art_change = self.art_alb["nowart"] != self.art_alb["oldart"] 
        alb_change = self.art_alb["nowalb"] != self.art_alb["oldalb"]
        tit_change = self.art_alb["title"] != self.art_alb["oldtit"]

        # Artist change
        if art_change and self.art_alb["nowart"]:
            # Sort out wiki
            self.wiki_thread.artist = unicode(self.art_alb["nowart"])
            self.wiki_thread.start()
            
            self.infopage_thread.artist = self.art_alb["nowart"]
            self.infopage_thread.album = self.art_alb["nowalb"]
            self.infopage_thread.title = self.art_alb["title"]
            self.infopage_thread.albums =  self.media_db.get_albums(self.art_alb["nowart"])  
            self.infopage_thread.use_web = True
            self.infopage_thread.start()
            self.art_alb["oldart"] = self.art_alb["nowart"]

        # Album change
        elif alb_change and self.art_alb["nowalb"]:
            self.infopage_thread.artist = self.art_alb["nowart"]
            self.infopage_thread.album = self.art_alb["nowalb"]
            self.infopage_thread.title = self.art_alb["title"]
            self.infopage_thread.albums =  self.media_db.get_albums(self.art_alb["nowart"])  
            self.infopage_thread.use_web = True
            self.infopage_thread.start()
            self.art_alb["oldalb"] = self.art_alb["nowalb"]
        # track change only   
        elif tit_change and self.art_alb["title"]:
            self.infopage_thread.artist = self.art_alb["nowart"]
            self.infopage_thread.album = self.art_alb["nowalb"]
            self.infopage_thread.title = self.art_alb["title"]
            self.infopage_thread.albums =  self.media_db.get_albums(self.art_alb["nowart"])  
            self.infopage_thread.use_web = False
            self.infopage_thread.start()
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
            self.minimise_to_tray(self.isHidden())
        # Middle-click to pause/play
        elif event == 4:
            stopped =  (not self.player.audio_object.is_playing())
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
            
    def generate_info(self):
        f_now = self.player.audio_object.current_source()['source']
        if not f_now:
            # Not yet playing
            f_now = self.playlist_table.currentRow()
        self.playlist_table.colourise(f_now)
        trk = self.playlist_table.current_track() 
        
        self.msg_status = "Playing: %s by %s on %s" % (trk.title, trk.artist, trk.album)
        self.stat_lbl.setText(self.msg_status)
        
        self.art_alb["nowart"]  = trk.artist
        self.art_alb["nowalb"]  = trk.album
        self.art_alb["title"]   = trk.title

   
    @pyqtSignature("int")  
    def collection_sort(self, p0):
        if self.collect_tree.mode == 0:
            self.collect_tree.set_mode(1)
            self.collect_tree.headerItem().setText(0, "Album/Artist")            
        else:
            self.collect_tree.set_mode(0)
            self.collect_tree.headerItem().setText(0, "Artist/Album")
        self.collect_tree.populate()
