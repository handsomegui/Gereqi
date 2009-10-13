#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow, QFileDialog,   \
QTableWidgetItem, QDesktopServices, QSystemTrayIcon, \
QIcon, QPixmap, QTreeWidgetItem, QPixmap, QMessageBox
from PyQt4.QtCore import pyqtSignature, QString, Qt,  \
QTime, QStringList
from PyQt4.phonon import Phonon
from random import randrange

from settings import Setting_Dialog
from database import Media
from metadata import Metadata
from threads import Getcover, Getwiki, Builddb
from timing import Timing
from setups import Setups
from finishes import Finishes


# I don't  like this multiple class inheritance
class MainWindow(QMainWindow, Setups, Timing, Finishes):
    """
    The main class of the app
    """    
    def __init__(self, parent = None):
        """
        Initialisation of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
        QMainWindow.__init__(self, parent)
        Setups.__init__(self) # Guess what? A guess!
        Finishes.__init__(self)
        self.setupUi(self)
        self.media_db = Media()
        self.media_dir = None
        self.meta = Metadata()
        self.setup_db_tree()
        self.old_pos = 0
        self.cover_thread = Getcover()
        self.html_thread = Getwiki()
        self.build_db_thread = Builddb()     
        self.locale = ".com" # needs to be editable in Setting_Dialog
        # artist,album info. [0:1] is old. [2:3] is now
        self.art = [None, None, None, None] 
        self.setup_audio()
        self.setup_shortcuts()
        self.setup_extra()        
        self.create_actions()        
        self.playlist_add_menu()
        self.create_tray_menu()
        
    @pyqtSignature("QString")
    def on_srchCollectEdt_textChanged(self, p0):
        """
        This allows the filtering of the collection tree
        """
        srch = str(p0)
        self.setup_db_tree(filt=srch)       
        
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_collectTree_itemDoubleClicked(self, item, column):
        """
        When double click and abum in the collection browser
        add the album's tracks to the playlist.
        """
        now = item.text(0)
        par = item.parent()
        track = None
        album = None
        artist = None
        
        # When we haven't selected an artist
        if par:
            par_par = par.parent()
            # When we select an individual track
            if par_par:
                artist = par_par.text(0)
                album = par.text(0)
                track = now
                
            # When we've selected an album
            else:
                album = now
                artist = par.text(0)
        # In any case we'll have an artist
        artist = artist.toLocal8Bit()
        artist = str(artist)
        artist = artist.decode("utf-8")
        if track:
            album = album.toLocal8Bit()
            album = str(album)
            album = album.decode("utf-8")      
            track = track.toLocal8Bit()
            track = str(track)
            track = track.decode("utf-8")
            track = self.media_db.get_file(artist, album, track)[0][0]
            info = self.media_db.get_info(track)[0][1:] 
            self.add2playlist(str(track), info)
        elif album:
            album = album.toLocal8Bit()
            album = str(album)
            album = album.decode("utf-8")
            tracks = self.media_db.get_files(artist, album)
            for track in tracks:
                track = track[0]
                # Retrieves metadata from database
                info = self.media_db.get_info(track)[0][1:] 
                self.add2playlist(str(track), info)
    
    @pyqtSignature("")
    def on_prevBttn_pressed(self):
        """
        Skip to previous track in viewable playlist
        if possible
        """
        track = self.generate_track("back")
        if track:
            self.media_object.stop()
            self.media_object.clear()    
            self.media_object.setCurrentSource(track)
            if self.is_playing():
                self.media_object.play()            
            else:
                self.generate_info()

    # Because of the 2 signals that can trigger this, it's possible
    # this method is called twice when one or the other is called.
    @pyqtSignature("bool")
    def on_playBttn_toggled(self, checked):
        """
        The play button either resumes or starts playback.
        Not possible to play a highlighted row.
        """
        # Strange bug where if the playback was stopped by stopBttn
        # starting takes a while (varies). 
        if checked:
            # Need a check to see currentsource  matches higlighted track
            queued = self.media_object.currentSource().fileName()
            # Nothing already loaded into phonon
            if not queued:
                selected = self.playlistTree.currentRow()
                # A row is selected
                if selected >= 0:
                    selected = self.generate_track("now", selected)                
                    self.media_object.setCurrentSource(selected)
                # Just reset the play button and stop here
                else:
                    self.playBttn.setChecked(False)
                    return
            self.media_object.play()
            self.stopBttn.setEnabled(True)
            icon = QIcon(QPixmap(":/Icons/media-playback-pause.png"))
            self.playBttn.setIcon(icon)
            if not self.is_playing():
                self.generate_info()
        else:
            self.media_object.pause()
            icon = QIcon(QPixmap(":/Icons/media-playback-start.png"))
            self.playBttn.setIcon(icon)
            self.stat_lbl.setText("Paused")
        self.playBttn.setChecked(checked)    
        self.play_action.setChecked(checked)
        self.actionPlay.setChecked(checked)
        
    @pyqtSignature("")
    def on_stopBttn_pressed(self):
        """
        To stop current track.
        """
        self.tabWidget_2.setTabEnabled(1, False)
        self.tabWidget_2.setTabEnabled(2, False)
        self.media_object.stop()
        self.playBttn.setChecked(False)
        self.stopBttn.setEnabled(False)
        self.finished()
        
    @pyqtSignature("")
    def on_nxtBttn_pressed(self):
        """
        Go to next item in playlist(down)
        """
        track = self.generate_track("next")
        if track:
            self.media_object.stop() 
            self.media_object.clear()      
            self.media_object.setCurrentSource(track)
            if self.is_playing():
                self.media_object.play()
        
    @pyqtSignature("int")
    def on_volSldr_valueChanged(self, value):
        """
        Self explanatory
        """        
        self.volLbl.setText("%s" % value)
        value = (value / 100.0) ** 2
        self.audio_output.setVolume(value)
    
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
            print self.media_dir
            
    @pyqtSignature("")
    def on_actionRescan_Collection_triggered(self):
        """
        Scans through a directory and looks for supported media,
        extracts metadata and adds them to the database,hopefully.
        Really needs to be done in a separate thread as scan could
        take a while.
        """
        print "Rebuild: Ensure the db is ON CONFLICT REPLACE"
        self.collection()
    
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
        # kde4 dialogs are being used somehow so can't see if the filters work
        mfiles = QFileDialog.getOpenFileNames(\
                        None, 
                        self.trUtf8("Select Music Files"),
                        QDesktopServices.storageLocation(QDesktopServices.MusicLocation), 
                        self.trUtf8("*.flac;*.mp3;*.ogg"), 
                        None)       
        if mfiles:
            formats = ["ogg", "mp3", "flac"]
            for item in mfiles:
                item = str(item.toLocal8Bit())
                item = item.encode("utf-8")
                ender = item.split(".")[-1]
                ender = str(ender)
                ender = ender.lower()
                if ender in formats:
                    info = self.meta.extract(item) 
                    self.add2playlist(item, info)

    @pyqtSignature("bool")
    def on_actionMinimise_to_Tray_triggered(self, checked):
        """
        Things to do when ui is minimised
        """
        self.minimise_to_tray(checked)
    
    @pyqtSignature("")
    def on_actionClear_triggered(self):
        """
        Clear current playlist and if no music playing
        clear self.media_object
        """
        #TODO:incorporate playlists in to here.
        # When cleared save the playlist first to be
        # used with the playlist undo/redo buttons
        # Has to incorporate database
        self.playlistTree.clearContents()
        rows = self.playlistTree.rowCount()
        # For some reason can only remove from bot to top
        for cnt in range(rows, -1, -1):
            self.playlistTree.removeRow(cnt)
        self.media_object.clearQueue()
    
    @pyqtSignature("")
    def on_clrplyBttn_clicked(self):
        """
        Clears current playlist
        """
        self.on_actionClear_triggered()
    
    @pyqtSignature("")
    def on_srchplyEdit_returnPressed(self):
        """
        Filters current playlist based on input.
        Not sure whether to highlight row or item
        """
        srch_txt = self.srchplyEdit.text()
        rows = []
        searched = self.playlistTree.findItems(srch_txt, Qt.MatchContains)
        for search in searched:
            row = search.row()
            if not row in rows:
                rows.append(row)
        print rows
    
    @pyqtSignature("bool")
    def on_muteBttn_toggled(self, checked):
        """
        Mutes audio output and changes button icon accordingly
        """
        self.audio_output.setMuted(checked)
        if checked:
            icon = QIcon(QPixmap(":/Icons/audio-volume-muted.png"))
            self.muteBttn.setIcon(icon)
        else:
            icon = QIcon(QPixmap(":/Icons/audio-volume-high.png"))
            self.muteBttn.setIcon(icon)
    
    # A much cleaner solution. When you seek the volume is momentarily
    # set to 100% so it can really standout. 
    @pyqtSignature("")
    def on_progSldr_sliderReleased(self):
        """
        Slot documentation goes here.
        """
        val = self.progSldr.value()
        self.media_object.seek(val)
        self.old_pos = val
    
    @pyqtSignature("")
    def on_actionUpdate_Collection_triggered(self):
        """
        Updates collection for new files. Ignore files already in database
        """
        # TODO: not completed yet. See self.collection
        print "Rebuild: Ensure the db is ON CONFLICT IGNORE"
        self.collection()

    @pyqtSignature("int, int")
    def on_playlistTree_cellDoubleClicked(self, row, column):
        """
        When item is doubleclicked. Play its row.
        """
        self.media_object.stop()
        track = self.generate_track("now", row)
        self.media_object.setCurrentSource(track)
        self.media_object.play()
        self.playBttn.setChecked(True) 
        self.play_action.setChecked(True)
        
    @pyqtSignature("")
    def on_actionHelp_activated(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.information(None,
            self.trUtf8("Help"),
            self.trUtf8("""Just a note. If you have used amaroq-0.1.* and are now trying the dev branch you need to delete "~/.amaroq/amaroq.db" \n
The old database format is no longer compatible with the new implementation."""))

    @pyqtSignature("QTreeWidgetItem*")
    def on_collectTree_itemExpanded(self, item):
        """
        Generates the albums to go with the artists in
        the collection tree when expanded. Only if empty.
        """
        #TODO: make this aware of collectTimeBox widget
        par = item.parent()
        # If we've expanded an album
        if par:
            artist = par.text(0)
            album = item.text(0)
        else:
            artist = item.text(0)
            album = None
        # An artist in any case
        artist = artist.toLocal8Bit()
        artist = str(artist)
        artist = artist.decode("utf-8")
        #TODO: add tracks in trackNum order
        if album:
            # Adding tracks to album
            if item.childCount() == 0:
                album = album.toLocal8Bit()
                album = str(album)
                album = album.decode("utf-8")
                tracks = self.media_db.get_titles(artist, album)
                for cnt in range(len(tracks)):
                    track = tracks[cnt][0]
                    track = QStringList(track)                
                    track = QTreeWidgetItem(track)
                    item.insertChild(cnt, track)
        else:
            # Adding albums to the artist
            if item.childCount() == 0:
                albums = self.media_db.get_albums(artist)
                for cnt in range(len(albums)):
                    album = albums[cnt][0]
                    album = QStringList(album)                
                    album = QTreeWidgetItem(album)
                    album.setChildIndicatorPolicy(0)
                    item.insertChild(cnt, album)

    @pyqtSignature("")
    def on_clrCollectBttn_clicked(self):
        """
        Clears the collection search widget and in turn
        resets the collection tree
        """
        #TODO: expand the artist chosen before reset
        self.srchCollectEdt.clear()

    @pyqtSignature("int")
    def on_collectTimeBox_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        filt = self.srchCollectEdt.text()
        filt = str(filt)
        self.setup_db_tree(filt)
        now = self.date_now()
        print "Filter collectionTree WRT time.", now
        
    @pyqtSignature("")
    def on_actionAbout_Amaroq_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.aboutQt(None, 
            self.trUtf8(""))

#######################################
#######################################

    def tick(self, time):
        """
        Every second update time labels and progress slider
        """
        pos = self.progSldr.sliderPosition()
        t_now = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        if t_now == QTime(0, 0, 0):
            # Used because no Phonon.state when the mediaobject goes 
            # to next queued track 2,3 is the same sig as when next/prev
            # buttons are used
            self.state_changed(2, 3) 
        now = t_now.toString('mm:ss')
        maxtime = self.t_length.toString('mm:ss')
        msg = "%s | %s" % (now, maxtime)
        self.progLbl.setText(msg)            
        # This only goes(?) if  the user has not grabbed the slider
        # The 'or' stops issue where the slider doesn't move after track finishes
        if pos == self.old_pos or pos < 1: 
            self.progSldr.setValue(time)
        self.old_pos = time
            
    def about_to_finish(self):
        """
        Generates a track to go into queue
        before playback stops
        """
        track = self.generate_track("next")
        if track:
            self.media_object.clearQueue()
            self.media_object.enqueue(track)

    def set_prog_sldr(self):
        """
        Linked to the current time of
        track being played
        """
        length = self.media_object.totalTime()
        self.progSldr.setValue(0)
        self.progSldr.setRange(0, length)
        self.old_pos = 0
        self.t_length = QTime(0, (length / 60000) % 60, (length / 1000) % 60)
            
    def state_changed(self, new, old):
        """
        This is linked to phonon.State. A very unreliable feature.
        """
        print "debug: %s -> %s" % (new, old)
        # Prevents the slider being reset if playback is paused
        # or unpaused
        if self.is_playing():
            if not ((new == 2) and ( old == 4)):
                self.set_prog_sldr()
        # Track change state
        # This is really iffy as phonon.state appears
        # to be 'misfiring'. Perhaps use the functions in here
        # directly from the buttons
        if new == 2 and old == 3: 
            print "debug: track change\n"
            self.generate_info()
            self.set_info()
            self.media_object.clearQueue()
        # Stopped playing and at end of playlist
        elif new == 1 and old == 2 and self.is_last():
            print "debug: stopped\n"
            self.finished()
            
    def finished(self):
        """
        Things to be performed when the playlist finishes
        """
        self.tabWidget_2.setTabEnabled(1, False)
        self.tabWidget_2.setTabEnabled(2, False)
        self.playBttn.setChecked(False)
        self.stopBttn.setEnabled(False)
        self.progSldr.setValue(0)
        self.old_pos = 0
        self.stat_lbl.setText("Stopped")
        self.progLbl.setText("00:00 | 00:00")
        # clear things like wiki and reset cover art to default        
        self.wikiView.setHtml(QString(""))
        self.coverView.setPixmap(QPixmap(":/Icons/music.png"))
        self.trkNowBox.setTitle(QString("No Track Playing"))
        self.art[0] = None
        self.art[1] = None
        
    def minimise_to_tray(self, state):
        if state:
            self.show()
            self.setWindowState(Qt.WindowActive)
        else:
            self.hide()
        self.view_action.setChecked(state)
        self.actionMinimise_to_Tray.setChecked(state)
    
    def collection(self):
        """
        Either generates a new DB or adds new files to it
        Not finished
        """
        if not self.media_dir:
            self.media_dir = QFileDialog.getExistingDirectory(\
                None,
                self.trUtf8("Select Media Directory"),
                self.trUtf8("/home"),
                QFileDialog.Options(QFileDialog.ShowDirsOnly))
        # If the dialog is cancelled in last if statement the below is ignored
        if self.media_dir:
            self.stat_bttn.setEnabled(True)
            self.build_db_thread.set_values(self.media_dir)
            self.stat_prog.setToolTip("Scanning Media")
            self.stat_prog.setValue(0)
            self.build_db_thread.start()

    def set_info(self):
        """
        The wikipedia page + album art to current artist playing
        """        
        # Wikipedia info
        if self.art[2] != self.art[0] and self.art[2]: 
            # passes the artist to the thread
            self.html_thread.set_values(self.art[2]) 
            # starts the thread
            self.html_thread.start() 
            self.art[0] = self.art[2]  
        # Album art
        if self.art[3] != self.art[1] and self.art[3]:
            self.cover_thread.set_values(self.art[3], self.art[2], self.locale)
            self.cover_thread.start()
            self.art[1] = self.art[3]

    def tray_event(self, event):
        """
        Things to perform on user-interaction of the tray icon
        other than bringing up it's menu
        """
        # Left click
        if event == 3:
            if self.isVisible():
                self.minimise_to_tray(False)
            else:
                self.minimise_to_tray(True)            
        # Middle-click to pause/play
        elif event == 4:
            if self.is_playing():
                self.on_playBttn_toggled(False)
            else:
                self.on_playBttn_toggled(True)
                
    def del_track(self):
        """
        Deletes selected tracks from playlist
        """
        items = self.playlistTree.selectedItems()
        for item in items:
            try:
                row = item.row()
                self.playlistTree.removeRow(row)
            except:
                #FIXME:tidy up
                # likely deleted already i.e selected same row but multiple columns
                return  
      
# TODO: these could be pushed into their own class
    def generate_track(self, mode, row=None):
        """
        As the playlist changes on sorting, the playlist (the immediately next/previous 
        tracks) has to be regenerated before the queing of the next track
        """
        # So that it can be dynamic later on when columns can be moved
        column = 8 
        track = None
        if mode == "now":
            track = self.playlistTree.item(row, column).text()
        else:
            current = self.media_object.currentSource().fileName()
            # If 0 then the playlist is empty
            rows = self.playlistTree.rowCount() 
            if rows > 0:
                for row in range(rows):
                    file_name = self.playlistTree.item(row, column).text()
                    # Track, track, track.
                    if file_name == current:
                        if mode == "back":
                            if (row - 1) >= 0:
                                track = self.playlistTree.item(row - 1 , column)
                                track = track.text()
                        elif mode == "next":
                            if self.play_type_bttn.isChecked():
                                # Here we need to randomly choose the next track
                                row = randrange(0, rows)
                                track = self.playlistTree.item(row, column)
                                track = track.text()
                            else:
                                if (row + 1) < rows:
                                    track = self.playlistTree.item(row + 1, column)
                                    track = track.text()
        if track:
            print repr(track)
            track = Phonon.MediaSource(track)     
            return track

    def generate_info(self):
        # This retrieves data from the playlist table, not the database. 
        # This is because the playlist may contain tracks added locally.
        file_list = self.gen_file_list()
        file_name = self.media_object.currentSource().fileName()
        row = file_list.index(file_name)
        title = self.playlistTree.item(row, 1).text()
        artist = self.playlistTree.item(row, 2).text()
        album = self.playlistTree.item(row, 3).text()
        msg1 = QString("Now Playing")
        msg2 = QString("%s by %s" % (title, artist))
        msg3 = QString("%s - %s\n%s" % (title, artist, album))
        self.trkNowBox.setTitle(msg3)
        icon = QSystemTrayIcon.NoIcon        
        self.tray_icon.showMessage(msg1, msg2, icon, 3000)
        message = "Playing: %s by %s on %s" % (title, artist, album)
        self.stat_lbl.setText(message)
        self.playlistTree.selectRow(row) 
        self.art[2] = artist.toUtf8()
        self.art[3] = album.toUtf8()
        if row and self.wikiView.isVisible():
            self.set_info()

    def is_playing(self):
        """
        To find out if a file is being played
        """
        state = self.media_object.state()
        if state == 2:
            return True
        else:
            return False

    def is_last(self):
        """
        Checks whether the current track in self.media_object
        is the last in the viewable playlist
        """
        now = self.media_object.currentSource().fileName()                
        file_list = self.gen_file_list()
        file_cnt = len(file_list)
        try:
            pos = file_list.index(now)
        except:
            pos = None
        if  pos and  pos == file_cnt:
            return True        

    def gen_file_list(self):
        """
        Creates a list of files in the playlist at its
        current sorting top to bottom
        """
        column = 8
        rows = self.playlistTree.rowCount() 
        file_list = []
        for row in range(rows):
            item = self.playlistTree.item(row, column).text()
            file_list.append(item)  
        return file_list   
        
    def play_type(self, checked):
        if checked:
            self.play_type_bttn.setText("R")
        else:
            self.play_type_bttn.setText("N")

    def add2playlist(self, file_name, info):
        """
        Called when adding tracks to the playlist either locally
        or from the database. Does not pull metadata from 
        the database and is passed into the function directly
        """
        #TODO: prevent creation of empty rows
        file_col = 8
        current_row = self.playlistTree.rowCount()
        track = "%02u" % info[0]
        # Creates each cell for a track based on info
        track_item = QTableWidgetItem(QString(track))
        track_item.setFlags(track_item.flags() ^ Qt.ItemIsEditable)
        title_item = QTableWidgetItem(QString(info[1]))
        title_item.setFlags(title_item.flags() ^ Qt.ItemIsEditable)
        artist_item = QTableWidgetItem(QString(info[2]))
        artist_item.setFlags(artist_item.flags() ^ Qt.ItemIsEditable)
        album_item = QTableWidgetItem(QString(info[3]))
        album_item.setFlags(album_item.flags() ^ Qt.ItemIsEditable)
        year_item = QTableWidgetItem(str(info[4]))
        year_item.setFlags(year_item.flags() ^ Qt.ItemIsEditable)
        genre_item = QTableWidgetItem(QString(info[5]))
        genre_item.setFlags(genre_item.flags() ^ Qt.ItemIsEditable)
        length_item = QTableWidgetItem(QString(info[6]))
        bitrate_item = QTableWidgetItem(QString(str(info[7])))
        file_item = QTableWidgetItem(QString(file_name))
        self.playlistTree.insertRow(current_row)
        #TODO: These column assignments have to be dynamic at some point
        self.playlistTree.setItem(current_row, 0, track_item)
        self.playlistTree.setItem(current_row, 1, title_item)
        self.playlistTree.setItem(current_row, 2, artist_item)
        self.playlistTree.setItem(current_row, 3, album_item)
        self.playlistTree.setItem(current_row, 4, year_item)
        self.playlistTree.setItem(current_row, 5, genre_item)
        self.playlistTree.setItem(current_row, 6, length_item)
        self.playlistTree.setItem(current_row, 7, bitrate_item)
        self.playlistTree.setItem(current_row, file_col , file_item)
        self.playlistTree.resizeColumnsToContents()
        if self.playlistTree.columnWidth(0) > 300:
            self.playlistTree.setColumnWidth(0, 300)
