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


from PyQt4.QtGui import QMainWindow, QFileDialog,   \
QTableWidgetItem, QDesktopServices, QSystemTrayIcon, \
QIcon, QTreeWidgetItem, QPixmap, QMessageBox, QColor, \
QSystemTrayIcon, QInputDialog, QLineEdit
from PyQt4.QtCore import QString, Qt, QTime, SIGNAL, \
SLOT, QDir, QObject, pyqtSignature

from random import randrange
import time

from settings import Setting_Dialog
from database import Media
from tagging import Tagging
from threads import Getcover, Getwiki, Builddb
from gstbe import Gstbe
from extraneous import Extraneous
from Ui_interface import Ui_MainWindow
from extrawidgets import SetupExtraWidgets, WidgetManips
from audiocd import AudioCD


class Finish:
    def __init__(self, parent):
        self.ui = parent

    def db_build(self, status):
        """
        Things to perform when the media library
        has been built/cancelled
        """
        self.ui.xtrawdgt.stat_bttn.setEnabled(False)
        if status == "cancelled":
            self.ui.xtrawdgt.stat_prog.setToolTip("Cancelled")
        else:
            self.ui.xtrawdgt.stat_prog.setToolTip("Finished")
        self.ui.xtrawdgt.stat_prog.setValue(100)
        self.ui.wdgt_manip.setup_db_tree()
        self.ui.srchCollectEdt.clear()
        
    def set_cover(self, img):
        if img.isNull() is True:
            self.ui.coverView.setPixmap(QPixmap(":/Icons/music.png"))
        else:
            cover = QPixmap()
            cover = cover.fromImage(img)
            cover = cover.scaledToWidth(200, Qt.SmoothTransformation)
            self.ui.coverView.setPixmap(cover)        
        
    def set_wiki(self, html):
        if html != "None":
            self.ui.contentTabs.setTabEnabled(2, True)
            self.ui.wikiView.setHtml(html)
        else:
            self.ui.contentTabs.setTabEnabled(2, False)
            
            
class AudioBackend:
    def __init__(self, parent,  backend="gstreamer"):
        self.ui = parent
        self.just_finished = False
        if backend == "gstreamer":
            self.__gstreamer_init()
            
    def __gstreamer_init(self):
        self.audio_object = Gstbe()
        QObject.connect(self.audio_object, SIGNAL("tick ( int )"), self.__prog_tick)
        self.audio_object.pipe_line.connect("about-to-finish", self.__about_to_finish)
        QObject.connect(self.audio_object, SIGNAL("track_changed()"), self.__track_changed)
        QObject.connect(self.audio_object, SIGNAL("finished()"), self.__finished_playing)
        QObject.connect(self.ui.stopBttn, SIGNAL("pressed()"), self.__finished_playing)
        
    def __about_to_finish(self, pipeline):
        """
        Generates a track to go into queue
        before playback stops
        """
        self.just_finished = True
        track = self.ui.tracking.generate_track("next")
        #Not at end of  playlist
        if track is not None:
            self.audio_object.enqueue(track)

    def __prog_tick(self, time):
        """
        Every second update time labels and progress slider
        """
        t_now = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        now = t_now.toString('mm:ss')
        max_time = self.ui.t_length.toString('mm:ss')
        self.ui.progLbl.setText("%s | %s" % (now, max_time))            
        # Allows normal playback whilst slider still grabbed
        if self.ui.progSldr.value() == self.ui.old_pos: 
            self.ui.progSldr.setValue(time)
        self.ui.old_pos = time
        
    def __track_changed(self):
        """
        When the playing track changes certain
        Ui features may need to be updated.
        """
        # Cannot do it in "about_to_finish" as it's in another thread
        if self.just_finished is True:
            self.just_finished = False
            self.__inc_playcount()
        
        self.ui.tracking.generate_info()
        self.ui.set_info()
        self.ui.set_prog_sldr()
        self.ui.old_pos = 0
        self.ui.progSldr.setValue(0)
        
    def __finished_playing(self):
        """
        Things to be performed when the playback finishes
        """
        self.just_finished = False
        self.ui.contentTabs.setTabEnabled(1, False)
        self.ui.contentTabs.setTabEnabled(2, False)
        self.ui.playBttn.setChecked(False)
        self.ui.stopBttn.setEnabled(False)
        self.ui.progSldr.setValue(0)
        self.ui.old_pos = 0
        self.ui.xtrawdgt.stat_lbl.setText("Stopped")
        self.ui.progLbl.setText("00:00 | 00:00")
        # clear things like wiki and reset cover art to default        
        self.ui.wikiView.setHtml(QString(""))
        self.ui.coverView.setPixmap(QPixmap(":/Icons/music.png"))
        self.ui.trkNowBox.setTitle(QString("No Track Playing"))
        self.ui.art_alb["oldart"] = self.ui.art_alb["oldalb"] = None
        self.ui.xtrawdgt.tray_icon.setToolTip("Stopped")
        
    def __inc_playcount(self):
        """
        Probably better to do this within the database.
        """
        now = self.ui.tracking.generate_track("back")
        playcount = int(self.ui.media_db.get_info(unicode(now))[0][5])
        playcount += 1
        self.ui.media_db.inc_count(playcount, unicode(now))
        


class Playlist:
    def __init__(self, parent):
        self.ui = parent
        
    def add_to_playlist(self, file_name, info=None):
        """
        Called when adding tracks to the playlist either locally
        or from the database. Does not pull metadata from 
        the database and is passed into the function directly
        """
        # This allows to manually put in info for things we know
        # mutagen cannot handle things like urls for podcasts
        if info is None:
            info = self.ui.meta.extract(file_name)
            if info is None:
                return
        row = self.ui.playlistTree.rowCount()
        self.ui.playlistTree.insertRow(row)
        #TODO: make the metadata come in as a dictionary
        tbl_items = [   ["Track", "%02u" % info[5]], ["Title", info[0]],  
                            ["Artist", info[1]], ["Album", info[2]], ["Year", info[3]], 
                            ["Genre", info[4]], ["Length", info[6]], ["Bitrate", str(info[7])], 
                            ["FileName", file_name]]
        # Creates each cell for a track based on info
        for header, thing in tbl_items:
            tbl_wdgt = QTableWidgetItem(QString(thing))
            column = self.header_search(header)
            self.ui.playlistTree.setItem(row, column, tbl_wdgt)
        self.ui.playlistTree.resizeColumnsToContents()   
        
    # This is needed as the higlighted row can be different
    # than the currentRow method of Qtableview.
    def current_row(self):
        """
        Finds the playlist row of the
        currently playing track
        """
        file_list = self.gen_file_list()
        current_file = self.ui.player.audio_object.current_source()
        
        if current_file is None:
            return self.ui.playlistTree.currentRow()
        else:
            return file_list.index(current_file)
        
        
    def gen_file_list(self):
        """
        Creates a list of files in the playlist at its
        current sorting top to bottom
        """
        rows = self.ui.playlistTree.rowCount() 
        column = self.header_search("FileName")
        file_list = [self.ui.playlistTree.item(row, column).text() for row in range(rows)]
        return file_list   
        
    def del_track(self):
        """
        Deletes selected tracks from playlist
        """
        items = self.ui.playlistTree.selectedItems()
        for item in items:
            try:
                row = item.row()
                self.ui.playlistTree.removeRow(row)
                self.tracknow_colourise()
            except RuntimeError:
                # likely deleted already i.e selected same row but multiple columns
                return 
        
    def header_search(self, val):
        """
        This will eventually allows the column order of the 
        playlist view to be changed         
        """
        cols = self.ui.playlistTree.columnCount()
        headers = [self.ui.playlistTree.horizontalHeaderItem(col).text() for col in range(cols)]
        return headers.index(val)
        
    #TODO: use native/theme colours for odd/even colours
    def tracknow_colourise(self, now=None):
        """
        Instead of using QTableWidget's selectRow function, 
        set the background colour of each item in a row
        until track changes.
        """
        columns = self.ui.playlistTree.columnCount()
        rows = self.ui.playlistTree.rowCount()
        for row in range(rows):
            for col in range(columns):
                item = self.ui.playlistTree.item(row, col)
                if row != now:
                    if row % 2:
                        item.setBackgroundColor(self.ui.colours["odd"])
                    else:
                        item.setBackgroundColor(self.ui.colours["even"])
                else:
                    item.setBackgroundColor(self.ui.colours["now"])
                    self.ui.playlistTree.selectRow(now)
                        
    def highlighted_track(self):
        """
        In the playlist
        """
        row = self.ui.playlistTree.currentRow()
        column = self.header_search("FileName")
        track = None
        # -1 is the row value for None
        if row > -1:
            track = self.ui.playlistTree.item(row, column).text()
        return track        

class Track:
    def __init__(self, parent):
        self.ui = parent
        
    def generate_track(self, mode, row=None):
        """
        As the playlist changes on sorting, the playlist (the immediately next/previous 
        tracks) has to be regenerated before the queing of the next track
        """
        # So that it can be dynamic later on when columns can be moved
        column = self.ui.playlisting.header_search("FileName")
        track = None
        if mode == "now":
            track = self.ui.playlistTree.item(row, column).text()
        else:
            # If 0 then the playlist is empty
            rows = self.ui.playlistTree.rowCount() 
            if rows > 0:
                row_now = self.ui.playlisting.current_row()
                if row_now is not None:
                    if mode == "back":
                        if (row_now - 1) >= 0:
                            track = self.ui.playlistTree.item(row_now - 1 , column)
                            track = track.text()
                    elif mode == "next":
                        if self.ui.xtrawdgt.play_type_bttn.isChecked() is True:
                            # Here we need to randomly choose the next track
                            row = randrange(0, rows)
                            track = self.ui.playlistTree.item(row, column)
                            track = track.text()
                        elif (row_now + 1) < rows:
                            track = self.ui.playlistTree.item(row_now + 1, column)
                            track = track.text()
        if track:
            return str(track)
            
    def generate_info(self):
        """
         This retrieves data from the playlist table, not the database. 
        This is because the playlist may contain tracks added locally.        
        """
        row = self.ui.playlisting.current_row()
        hdr = self.ui.playlisting.header_search
        title = self.ui.playlistTree.item(row, hdr("Title")).text()
        artist = self.ui.playlistTree.item(row, hdr("Artist")).text()
        album = self.ui.playlistTree.item(row, hdr("Album")).text()
        min, sec = self.ui.playlistTree.item(row, hdr("Length")).text().split(":")
        self.play_time = 1000 * ((int(min) * 60) + int(sec))
        
        msg_header = QString("Now Playing")
        msg_main = QString("%s by %s" % (title, artist))
        self.ui.trkNowBox.setTitle(msg_main)
        if self.ui.show_messages and self.ui.playBttn.isChecked():
            self.ui.xtrawdgt.tray_icon.showMessage(msg_header, msg_main, QSystemTrayIcon.NoIcon, 3000)
        self.ui.xtrawdgt.tray_icon.setToolTip(msg_main)
        self.msg_status = "Playing: %s by %s on %s" % (title, artist, album)
        self.ui.xtrawdgt.stat_lbl.setText(self.msg_status)
        self.ui.playlisting.tracknow_colourise(row)
        self.ui.art_alb["nowart"] = artist.toUtf8()
        self.ui.art_alb["nowalb"] = album.toUtf8()
        

class MainWindow(Ui_MainWindow, QMainWindow): 
    """
    Where everything starts from, mostly.
    """    

    
    def __init__(self, parent = None):
        """
        Initialisation of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
        
        self.show_messages = True
        self.art_alb = {"oldart":None, "oldalb":None, "nowart":None, "nowalb":None} 
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
        self.setupUi(self)
        
        self.media_dir = None
        self.media_db = Media()
        self.cover_thread = Getcover()        
        self.html_thread = Getwiki()
        self.build_db_thread = Builddb()
        self.extras = Extraneous()
        self.meta = Tagging(self.audio_formats)
        self.player = AudioBackend(self)
        self.playlisting = Playlist(self)
        self.xtrawdgt = SetupExtraWidgets(self)
        self.tracking = Track(self)
        self.wdgt_manip = WidgetManips(self)
        self.finishes = Finish(self)
        
        self.connect(self.build_db_thread, SIGNAL("finished ( QString ) "), self.finishes.db_build)
        self.connect(self.cover_thread, SIGNAL("got-image ( QImage ) "), self.finishes.set_cover) 
        self.connect(self.html_thread, SIGNAL("got-wiki ( QString ) "), self.finishes.set_wiki)
        self.connect(self.build_db_thread, SIGNAL("progress ( int ) "), self.xtrawdgt.stat_prog, SLOT("setValue(int)"))
        self.connect(self.fileView, SIGNAL("expanded (const QModelIndex&)"), self.__resize_fileview) 
        self.connect(self.fileView, SIGNAL("doubleClicked (const QModelIndex&)"), self.__fileview_item)
        self.connect(self.actionPlay, SIGNAL("toggled ( bool )"), self.playBttn, SLOT("setChecked(bool)"))
        self.connect(self.actionNext_Track, SIGNAL("triggered()"), self.nxtBttn, SLOT("click()"))
        self.connect(self.actionPrevious_Track, SIGNAL("triggered()"), self.prevBttn, SLOT("click()"))  
        self.connect(self.actionStop, SIGNAL("triggered()"), self.stopBttn, SLOT("click()"))
        self.connect(self.xtrawdgt.stat_bttn, SIGNAL("pressed()"), self.quit_build)
        self.connect(self.xtrawdgt.play_type_bttn, SIGNAL('toggled ( bool )'), self.wdgt_manip.set_play_type)

        
        #Make the collection search line-edit have the keyboard focus on startup.
        self.srchCollectEdt.setFocus()
        self.wdgt_manip.setup_db_tree()
        self.wdgt_manip.pop_playlist_view()
        
    @pyqtSignature("QString")  
    def on_srchCollectEdt_textChanged(self, p0):
        """
        This allows the filtering of the collection tree
        """
        srch = str(p0)
        time_filt = self.__time_filt_now()
        self.wdgt_manip.setup_db_tree(srch, time_filt)       
    
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_collectTree_itemDoubleClicked(self, item, column):
        """
        When double click and abum in the collection browser
        add the album's tracks to the playlist.
        """
        now = item.text(0)
        par = item.parent()
        track = album = artist = None

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
        if artist is None:
            artist = now
        if track is not None:
            file_name = self.media_db.get_file(unicode(artist), unicode(album), unicode(track))
            self.playlisting.add_to_playlist(file_name)
        elif album is not None:
            tracks = self.media_db.get_files(unicode(artist), unicode(album))
            for track in tracks:
                # Retrieves metadata from database
                self.playlisting.add_to_playlist(track)
    
    @pyqtSignature("")
    def on_prevBttn_pressed(self):
        """
        Skip to previous track in viewable playlist
        if possible
        """
        track = self.tracking.generate_track("back")
        if track is not None:
            self.player.audio_object.stop()
            self.player.audio_object.load(track)
            # Checks to see if the playbutton is in play state
            if self.playBttn.isChecked() is True:
                self.player.audio_object.play()
            else:
                self.playlisting.tracknow_colourise(self.playlisting.current_row())

    #TODO: this can be called from 2 other actions. Needs tidy up.
    @pyqtSignature("bool")
    def on_playBttn_toggled(self, checked):
        """
        The play button either resumes or starts playback.
        Not possible to play a highlighted row.
        """
        #TODO: messy. Clean up.
        if checked is True:
            queued = self.player.audio_object.current_source()
            stopped = self.stopBttn.isEnabled() is False
            highlighted = self.playlisting.highlighted_track()
            if highlighted is not None:      
                # Checks to see if highlighted track matches queued track
                # prevents loading whilst playing
                if (queued != highlighted) and (stopped is True): 
                    queued = highlighted
                    self.player.audio_object.load(queued)
                # Nothing already loaded into playbin
                elif queued is None:
                    selected = self.playlistTree.currentRow()
                    # A row is selected
                    if selected >= 0:
                        selected = self.tracking.generate_track("now", selected)           
                        self.player.audio_object.load(selected)
                    # Just reset the play button and stop here
                    else:
                        # This will call this function
                        self.playBttn.setChecked(False)
                # Makes sure the statusbar text changes from
                # paused back to the artist/album/track string
                elif self.player.audio_object.is_paused() is True:
                    self.xtrawdgt.stat_lbl.setText(self.tracking.msg_status)
                self.player.audio_object.play()
                self.stopBttn.setEnabled(True)
                icon = QIcon(QPixmap(":/Icons/media-playback-pause.png"))
                tray = QIcon(QPixmap(":/Icons/app.png"))
                self.playBttn.setIcon(icon)
                self.xtrawdgt.tray_icon.setIcon(tray)
            else:
                self.playBttn.setChecked(False)
                return
        else:
            if self.player.audio_object.is_playing() is True:
                self.player.audio_object.pause()
            icon = QIcon(QPixmap(":/Icons/media-playback-start.png"))
            tray = QIcon(QPixmap(":/Icons/app-paused.png"))
            self.playBttn.setIcon(icon)
            self.xtrawdgt.tray_icon.setIcon(tray)
            if self.playlistTree.currentRow() >= 0:
                self.xtrawdgt.stat_lbl.setText("Paused")
            else:
                self.xtrawdgt.stat_lbl.setText("Finished")
        self.xtrawdgt.play_action.setChecked(checked)
        self.actionPlay.setChecked(checked)
        
    @pyqtSignature("")    
    def on_stopBttn_pressed(self):
        """
        To stop current track.
        """
        self.contentTabs.setTabEnabled(1, False)
        self.contentTabs.setTabEnabled(2, False)
        self.player.audio_object.stop()
        self.playBttn.setChecked(False)
        self.stopBttn.setEnabled(False)
        
    @pyqtSignature("")
    def on_nxtBttn_pressed(self):
        """
        Go to next item in playlist(down)
        """
        track = self.tracking.generate_track("next")
        if track is not None:
            self.player.audio_object.stop() 
            self.player.audio_object.load(track)
            if self.playBttn.isChecked() is True:
                self.player.audio_object.play()
            else:
                self.playlisting.tracknow_colourise(self.playlisting.current_row())
        else:
            # TODO: some tidy up thing could go here
            return
     
    @pyqtSignature("int")
    def on_volSldr_valueChanged(self, value):
        """
        Self explanatory
        """        
        value = (value / 100.0) ** 2
        self.player.audio_object.set_volume(value)
    
    @pyqtSignature("")
    def on_actionConfigure_triggered(self):
        """
       Brings up the settings Dialog
        """
        # TODO: not finished yet. Need to learn
        # more about modal dialogs
        dialog = Setting_Dialog(self)
        if dialog.exec_():
            self.media_dir = dialog.dir_val()
            print(self.media_dir)
            
    @pyqtSignature("")
    def on_actionRescan_Collection_triggered(self):
        """
        Scans through a directory and looks for supported media,
        extracts metadata and adds them to the database,hopefully.
        Really needs to be done in a separate thread as scan could
        take a while.
        """
        print("Rebuild: Ensure the db is ON CONFLICT REPLACE")
        self.create_collection()
    
    @pyqtSignature("")
    def on_actionQuit_triggered(self):
        """
        Closing Down. Maybe some database interaction.
        """
        exit()
    
    @pyqtSignature("")
    def on_actionPlay_Media_triggered(self):
        """
        Extract music files and shove into current playlist.
        """        
        mfiles = QFileDialog.getOpenFileNames(\
                        None, 
                        QString("Select Music Files"),
                        QDesktopServices.storageLocation(QDesktopServices.MusicLocation), 
                        #TODO: do not hard-code this
                        QString(" ".join(self.format_filter)), 
                        None)       
                        
        if mfiles is not None:
            for item in mfiles:
                ender = unicode(item).split(".")[-1]
                if ender.lower() in self.audio_formats:
                    self.playlisting.add_to_playlist(unicode(item))

    @pyqtSignature("bool")
    def on_actionMinimise_to_Tray_toggled(self, checked):
        self.minimise_to_tray(checked)
    
    @pyqtSignature("")
    def on_actionClear_triggered(self):
        """
        Clear current playlist and if no music playing
        clear self.player.audio_object
        """
        #TODO:incorporate playlists in to here.
        # When cleared save the playlist first to be
        # used with the playlist undo/redo buttons
        self.playlistTree.clearContents()
        rows = self.playlistTree.rowCount()
        # For some reason can only remove from bot to top
        for cnt in range(rows, -1, -1):
            self.playlistTree.removeRow(cnt)
    
    @pyqtSignature("")
    def on_clrplyBttn_clicked(self):
        """
        Clears current playlist and sets focus
        on the search linedit
        """
        self.on_actionClear_triggered()
        self.srchplyEdit.setFocus()
    
    @pyqtSignature("QString")
    def on_srchplyEdit_textChanged(self, p0):
        """
        Filters current playlist based on input.
        Not sure whether to highlight row or item
        """
        # Resets before searching again
        now = self.playlisting.current_row()
        if now is not None:
            self.playlisting.highlighted_track()
        test = len(str(p0).strip())
        # Checks if the search edit isn't empty
        if test > 0:
            rows = []
            columns = self.playlistTree.columnCount()
            searched = self.playlistTree.findItems(p0, Qt.MatchContains)
            for search in searched:
                row = search.row()
                if row not in rows:
                    rows.append(row)
                    for col in range(columns):
                        item = self.playlistTree.item(row, col)
                        item.setBackgroundColor(self.colours["search"])
            for row in range(self.playlistTree.rowCount()):
                if row not in rows:
                    for col in range(columns):
                        item = self.playlistTree.item(row, col)
                        if row % 2:
                            item.setBackgroundColor(self.colours["odd"])
                        else:
                            item.setBackgroundColor(self.colours["even"])
        else:
            self.playlisting.tracknow_colourise()
                
    @pyqtSignature("bool")
    def on_muteBttn_toggled(self, checked):
        """
        Mutes audio output and changes button icon accordingly
        """
        self.player.audio_object.mute(checked)
        if checked is True:
            icon = QIcon(QPixmap(":/Icons/audio-volume-muted.png"))
            self.muteBttn.setIcon(icon)
        else:
            vol = (self.volSldr.value() / 100.0) ** 2
            icon = QIcon(QPixmap(":/Icons/audio-volume-high.png"))
            self.muteBttn.setIcon(icon)
            self.player.audio_object.set_volume(vol)
      
    @pyqtSignature("")  
    def on_progSldr_sliderReleased(self):
        """
        Set's an internal seek value for tick() to use
        """
        val = self.progSldr.value()
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
    def on_playlistTree_cellDoubleClicked(self, row, column):
        """
        When item is doubleclicked. Play its row.
        """
        #This won't actualy stop. It'll pause instead.
        self.playBttn.setChecked(False)
        
        self.player.audio_object.stop()
        track = self.tracking.generate_track("now", row)
        self.player.audio_object.load(track)
        # Checking the button is the same
        #  as self.player.audio_object.play(), just cleaner overall
        self.playBttn.setChecked(True) 
        self.xtrawdgt.play_action.setChecked(True)
        
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
    def on_collectTree_itemExpanded(self, item):
        """
        Generates the albums to go with the artists in
        the collection tree when expanded. Only if empty.
        """
        filt_time = self.__time_filt_now()
        par = item.parent()
        # If we've expanded an album
        if par is not None:
            artist = par.text(0)
            album = item.text(0)
        else:
            artist = item.text(0)
            album = None
        
        if (album is not None) and (item.childCount() == 0):
            # Adding tracks to album
            if filt_time is None:
                tracks = self.media_db.get_titles(unicode(artist), unicode(album))
            else:
                tracks = self.media_db.get_titles_timed(unicode(artist), unicode(album), filt_time)
            for cnt in range(len(tracks)):
                track = QTreeWidgetItem([tracks[cnt][0] ] )
                item.insertChild(cnt, track)
       
       # Adding albums to the artist 
       # i.e. the parent has no children    
        elif item.childCount() == 0: 
            if filt_time is None:
                albums = self.media_db.get_albums(unicode(artist))
            else:
                albums = self.media_db.get_albums_timed(unicode(artist), filt_time)                
            for cnt in range(len(albums)):      
                album = QTreeWidgetItem([albums[cnt][0]])
                album.setChildIndicatorPolicy(0)
                item.insertChild(cnt, album)

    @pyqtSignature("")
    def on_clrCollectBttn_clicked(self):
        """
        Clears the collection search widget and in turn
        resets the collection tree
        """
        self.srchCollectEdt.clear()
        self.srchCollectEdt.setFocus()

    @pyqtSignature("int")
    def on_collectTimeBox_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        filt = self.srchCollectEdt.text()
        filt_time = self.__time_filt_now()
        if filt_time is None:
            self.wdgt_manip.setup_db_tree(str(filt))
        else:
            self.wdgt_manip.setup_db_tree(str(filt), filt_time)
        
    @pyqtSignature("")
    def on_actionAbout_Gereqi_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.aboutQt(None, 
            QString(""))
            
    @pyqtSignature("")
    def on_clrsrchBttn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.srchplyEdit.clear()
        self.playlisting.highlighted_track()
        
    @pyqtSignature("")
    def on_actionPlay_Audio_CD_triggered(self):
        """
        Slot documentation goes here.
        """
        check = QMessageBox.question(None,
            QString("Play Audio-CD?"),
            QString("""Playback of CD's works up to a point at the moment. 
            Until Gstreamer-10.26 is released this situation will not change.  
            You can give it a try anyway."""),
            QMessageBox.StandardButtons(\
                QMessageBox.No | \
                QMessageBox.Yes))
        
        if check:
            acd = AudioCD()
            cd_tracks = acd.get_info()
            for trk in cd_tracks:
                self.playlisting.add_to_playlist(trk[-1],  trk)
                
    @pyqtSignature("")
    def on_svplyBttn_clicked(self):
        """
        Based on what is in the playlist and chosen name, it'll
        get put into the database
        """
        play_name = QInputDialog.getText(\
            None,
            self.trUtf8("Save Playlist"),
            self.trUtf8("Enter a name for the playlist:"),
            QLineEdit.Normal)
            
        if play_name[1] is True:
            check = self.media_db.playlist_tracks(unicode(play_name[0]))
            if len(check) > 0:
                msg = QMessageBox.warning(None,
                    self.trUtf8("Overwrite Playlist?"),
                    self.trUtf8("""A playlist named '%s' already exists. Do you want to overwrite it?"""  
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
                    self.on_svplyBttn_clicked()
                    
            tracks = self.playlisting.gen_file_list()            
            for track in tracks:
                self.media_db.playlist_add(unicode(play_name[0]), unicode(track))
            self.wdgt_manip.pop_playlist_view()
            
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_playlstView_itemDoubleClicked(self, item, column):
        """
        Slot documentation goes here.
        """
        try:
            par = unicode(item.parent().text(0))
        except  AttributeError:
            return
        
        if par =="Podcasts":
            return
            
        elif par == "Radio Streams":
            return
            
        elif par == "Playlists":
            playlist = item.text(column)
            tracks = self.media_db.playlist_tracks(unicode(playlist))
            for track in tracks:
                self.playlisting.add_to_playlist(track[0])
                
        else:
            new_par = item.parent().parent()
            print new_par.text(0), item.text(0)
            
            if new_par.text(0) == "Playlists":
                artist, title = unicode(item.text(0)).split(" - ")
                print self.media_db.search_by_titandart(artist, title)
                
            
    @pyqtSignature("bool")
    def on_delPlylstBttn_clicked(self, checked):
        """
        Delete a selected playlist from the DB
        """
        playlist = self.playlstView.selectedItems()
        if len(playlist) > 0:
            self.media_db.playlist_delete(unicode(playlist[0].text(0)))
            self.wdgt_manip.pop_playlist_view()
            
    
    @pyqtSignature("bool")
    def on_rnmPlylstBtnn_clicked(self, checked):
        """
        Rename the slected playlist
        """
        playlist = self.playlstView.selectedItems()
        try:
            par = unicode(playlist[0].parent().text(0))
        except  AttributeError:
            return        
            
        if (len(playlist) > 0) and (par in ["Podcasts", "Radio Streams",  "Playlists"]):
            new_name = QInputDialog.getText(\
                None,
                self.trUtf8("Rename Playlist"),
                self.trUtf8("Rename the playlist to:"),
                QLineEdit.Normal)
            
            # Checks if you entered a non-zero length name and that you clikced 'ok'
            if (new_name[1] is True) and (len(unicode(new_name[0])) > 0):
                #get all the tracks in the selected playlist
                tracks = self.media_db.playlist_tracks(unicode(playlist[0].text(0)))
                # delete the old playlist
                self.media_db.playlist_delete(unicode(playlist[0].text(0)))
                # add the tracks back in but with a new name, probably cleaner using an sql query
                for track in tracks:
                    self.media_db.playlist_add(unicode(new_name[0]), track[0])
                self.wdgt_manip.pop_playlist_view()
            
#######################################
#######################################
        
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
        self.progSldr.setRange(0, self.tracking.play_time)
        self.t_length = QTime(0, (self.tracking.play_time / 60000) % 60, (self.tracking.play_time / 1000) % 60)
            
    def minimise_to_tray(self, state):
        """
        Does what it says.
        """
        if state is True:
            self.show()
            self.setWindowState(Qt.WindowActive)
        else:
            self.hide()
        self.xtrawdgt.view_action.setChecked(state)
        self.actionMinimise_to_Tray.setChecked(state)
    
    def create_collection(self):
        """
        Either generates a new DB or adds new files to it
        Not finished
        """
        if self.media_dir is None:
            self.media_dir = QFileDialog.getExistingDirectory(\
                None,
                QString("Select Media Directory"),
                QDesktopServices.storageLocation(QDesktopServices.MusicLocation),
                QFileDialog.Options(QFileDialog.ShowDirsOnly))
        # If the dialog is cancelled in last if statement the below is ignored
        if self.media_dir is not None:
            self.xtrawdgt.stat_bttn.setEnabled(True)
            self.build_db_thread.set_values(self.media_dir, self.audio_formats)
            self.xtrawdgt.stat_prog.setToolTip("Scanning Media")
            self.xtrawdgt.stat_prog.setValue(0)
            self.build_db_thread.start()

    def set_info(self):
        """
        The wikipedia page + album art to current artist playing
        """
        art_change = self.art_alb["nowart"] != self.art_alb["oldart"] 
        # Wikipedia info
        if (art_change is True) and (self.art_alb["nowart"] is not None):
            # passes the artist to the thread
            self.html_thread.set_values(self.art_alb["nowart"]) 
            # starts the thread
            self.html_thread.start() 
            self.art_alb["oldart"] = self.art_alb["nowart"]
            
        alb_change = self.art_alb["nowalb"] != self.art_alb["oldalb"]
        # Album art
        if (alb_change is True) and (self.art_alb["nowalb"] is not None):
            album = self.art_alb["nowalb"]
            artist = self.art_alb["nowart"]
            self.cover_thread.set_values(album, artist, self.locale)
            self.cover_thread.start()
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
            self.playBttn.setChecked(stopped)

    def closeEvent(self, event):
        """
        When the 'X' button or alt-f4 is triggered
        """
        if self.xtrawdgt.tray_icon.isVisible() is True:
            self.hide()
            event.ignore()
            
    def __resize_fileview(self):
        """
        Resizes the fileView to it's contents.
        Because of the '0' this seperate method is needed
        """
        self.fileView.resizeColumnToContents(0)
        
    def __fileview_item(self, index):
        """
        This takes the fileview item and deduces whether
        it's a file or directory and populates playlist if possible
        """
        if self.xtrawdgt .dir_model.isDir(index) is True:
            fname = self.xtrawdgt .dir_model.filePath(index)
            searcher = QDir(fname)
            searcher.setFilter(QDir.Files)
            searcher.setFilter(QDir.Files)
            searcher.setNameFilters(self.format_filter)
            for item in searcher.entryInfoList():
                fname = item.absoluteFilePath()
                self.playlisting.add_to_playlist(unicode(fname))
        else:
            fname = self.xtrawdgt .dir_model.filePath(index)
            self.playlisting.add_to_playlist(unicode(fname))
            
    def __time_filt_now(self):
        index = self.collectTimeBox.currentIndex()
        if index == 0:
            #All
            filt_time = None
        elif index == 1:
            # Today
            now = time.localtime()
            filt_time = int(round(time.time() - ( (now[3] * now[4]) + now[5]) ))
        elif index == 2:
            # Week - 7 * 24 * 60 * 60
            filt_time  = int(round(time.time() - 604800))
        elif index == 3:
            # Month - 28 * 24 * 60 * 60
            filt_time  = int(round(time.time() - 2419200))
        elif index == 4:
            # 3 Months - 3 * 28 * 24 * 60 * 60
            filt_time  = int(round(time.time() - 7257600))
        elif index == 5:
            # Year 365.25 * 24 * 60 * 60
            filt_time  = int(round((time.time() - 31557600)))
    
        return filt_time

