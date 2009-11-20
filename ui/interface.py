#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow, QFileDialog,   \
QTableWidgetItem, QDesktopServices, QSystemTrayIcon, \
QIcon, QPixmap, QTreeWidgetItem, QPixmap, QMessageBox, \
QColor
from PyQt4.QtCore import pyqtSignature, QString, Qt,  \
QTime, QStringList, SIGNAL
from random import randrange

from settings import Setting_Dialog
from database import Media
from metadata import Metadata
from threads import Getcover, Getwiki, Builddb
from timing import Timing
from setups import Setups
from finishes import Finishes
from gstbe import Player


class MainWindow(Setups, Finishes, QMainWindow):
    """
    The main class of the app. There's loads of
    inherited Classes that may or may not have
    identical object/method names
    """    
    show_messages = False
    media_dir = None
    media_db = Media()
    meta = Metadata()
    cover_thread = Getcover()        
    html_thread = Getwiki()
    build_db_thread = Builddb()
    old_pos = 0
    locale = ".com"
    dating = Timing()
    playbin = Player()
    # artist,album info. [0:1] is old. [2:3] is now
    art = [None, None, None, None] 
    
    def __init__(self, parent = None):
        """
        Initialisation of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
#        super(MainWindow, self).__init__()
        QMainWindow.__init__(self, parent)
        # Do I really need these
        Setups.__init__(self) 
        Finishes.__init__(self)
        self.setupUi(self)
        self.setup_db_tree()
        self.setup_shortcuts()
        self.setup_extra()        
        self.create_actions()        
        self.playlist_add_menu()
        self.create_tray_menu()

        self.connect(self.playbin, SIGNAL("tick ( int )"), self.prog_tick)
        self.connect(self.playbin, SIGNAL("about_to_finish()"), self.about_to_finish)
        self.connect(self.playbin, SIGNAL("autoqueued()"), self.generate_info)
        self.connect(self.playbin, SIGNAL("finished()"), self.finished_playing)
        
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
        if not artist:
            artist = now
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
            self.playbin.stop()
            self.playbin.load(track)
            self.generate_info()
            # Checks to see if the playbutton is in play state
            if self.playBttn.isChecked():
                self.playbin.play()
            # Just highlight the track we would play
            else:
                self.tracknow_colourise(self.current_track())

    #TODO: this can be called from 2 other actions. Needs tidy up.
    @pyqtSignature("bool")
    def on_playBttn_toggled(self, checked):
        """
        The play button either resumes or starts playback.
        Not possible to play a highlighted row.
        """
        #TODO: messy. Clean up.
        if checked:
            queued = self.playbin.current_source()
            #FIXME: try and invert the result for less confusing varName
            not_stopped = self.stopBttn.isEnabled()
            highlighted = str(self.highlighted_track())
            
            if highlighted:
                # Checks to see if highlighted track matches queued track
                if queued != highlighted:
                    queued = highlighted
                    
                #FIXME:confusing as hell
                if queued and not not_stopped: 
                    self.playbin.load(queued)
                    self.generate_info()
                    
                # Nothing already loaded into playbin
                elif not queued:
                    selected = self.playlistTree.currentRow()
                    # A row is selected
                    if selected >= 0:
                        selected = self.generate_track("now", selected)           
                        self.playbin.load(str(selected))
                        self.generate_info()
                        
                    # Just reset the play button and stop here
                    else:
                        # This will call this function
                        self.playBttn.setChecked(False)
                        return
                self.playbin.play()
                self.stopBttn.setEnabled(True)
                icon = QIcon(QPixmap(":/Icons/media-playback-pause.png"))
                self.playBttn.setIcon(icon)
        else:
            self.playbin.pause()
            icon = QIcon(QPixmap(":/Icons/media-playback-start.png"))
            self.playBttn.setIcon(icon)
            if self.playlistTree.currentRow() >= 0:
                self.stat_lbl.setText("Paused")
            else:
                self.stat_lbl.setText("Finished")
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
        self.playbin.stop()
        self.playBttn.setChecked(False)
        self.stopBttn.setEnabled(False)
        self.finished_playing()
        
    @pyqtSignature("")
    def on_nxtBttn_pressed(self):
        """
        Go to next item in playlist(down)
        """
        track = self.generate_track("next")
        if track:
            self.playbin.stop() 
            self.playbin.load(track)
            self.generate_info()
            if self.playBttn.isChecked():
                self.playbin.play()
            else:
                self.tracknow_colourise(self.current_track())
        else:
            # TODO: some tidy up thing could go here
            return
        
    @pyqtSignature("int")
    def on_volSldr_valueChanged(self, value):
        """
        Self explanatory
        """        
        self.volLbl.setText("%s" % value)
        value = (value / 100.0) ** 2
        self.playbin.set_volume(value)
    
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
        clear self.playbin
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
#        self.media_object.clearQueue()
    
    @pyqtSignature("")
    def on_clrplyBttn_clicked(self):
        """
        Clears current playlist
        """
        self.on_actionClear_triggered()
    
    @pyqtSignature("QString")
    def on_srchplyEdit_textChanged(self, p0):
        """
        Filters current playlist based on input.
        Not sure whether to highlight row or item
        """
        # Resets before searching again
        self.tracknow_colourise(self.current_track)
        test = len(str(p0).strip())
        # Checks if the search edit isn't empty
        if test > 0:
            rows = []
            columns = self.playlistTree.columnCount()
            colour = QColor(255, 128, 128, 128)
            searched = self.playlistTree.findItems(p0, Qt.MatchContains)
            for search in searched:
                row = search.row()
                if not row in rows:
                    rows.append(row)
                    for col in range(columns):
                        item = self.playlistTree.item(row, col)
                        item.setBackgroundColor(colour)
                
    @pyqtSignature("bool")
    def on_muteBttn_toggled(self, checked):
        """
        Mutes audio output and changes button icon accordingly
        """
        self.playbin.mute(checked)
        if checked:
            icon = QIcon(QPixmap(":/Icons/audio-volume-muted.png"))
            self.muteBttn.setIcon(icon)
        else:
            vol = (self.volSldr.value() / 100.0) ** 2
            icon = QIcon(QPixmap(":/Icons/audio-volume-high.png"))
            self.muteBttn.setIcon(icon)
            self.playbin.set_volume(vol)
        
    @pyqtSignature("")
    def on_progSldr_sliderReleased(self):
        """
        Set's an internal seek value for tick() to use
        """
        val = self.progSldr.value()
        self.playbin.seek(val)
        self.old_pos = val
    
    @pyqtSignature("")
    def on_actionUpdate_Collection_triggered(self):
        """
        Updates collection for new files. Ignore files already in database
        """
        # TODO: not completed yet. See self.collection
        print "Rebuild: Ensure the db is ON CONFLICT IGNORE"
        self.collection()

#FIXME: this causes a double-trigger of playbin.play() on app's
# first play.
    @pyqtSignature("int, int")
    def on_playlistTree_cellDoubleClicked(self, row, column):
        """
        When item is doubleclicked. Play its row.
        """
        self.playbin.stop()
        track = self.generate_track("now", row)
        self.playbin.load(track)
        self.generate_info()
        
        # Checking the button is the same
        #  as self.playbin.play()
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
            self.trUtf8("""Boo!"""))

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
        now = self.dating.date_now()
        print "Filter collectionTree WRT time.", now
        
    @pyqtSignature("")
    def on_actionAbout_Gereqi_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.aboutQt(None, 
            self.trUtf8(""))
            
    @pyqtSignature("")
    def on_clrsrchBttn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.srchplyEdit.clear()
        self.tracknow_colourise(self.current_track)
        
        
#######################################
#######################################
        
    def quit_build(self):
        # ugly doesn't terminate cleanly
        # causes poor performance and errors on a rescan
        # locks up database
        print self.build_db_thread.stop_now() 

    def current_track(self):
        """
        Finds the row of the currently
        playing track
        """
        file_list = self.gen_file_list()
        file_name = self.playbin.current_source()
        return file_list.index(file_name)
        
    def prog_tick(self, time):
        """
        Every second update time labels and progress slider
        """
        if time < 1000:
            self.set_prog_sldr()
        pos = self.progSldr.sliderPosition()
        t_now = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        now = t_now.toString('mm:ss')
        maxtime = self.t_length.toString('mm:ss')
        msg = "%s | %s" % (now, maxtime)
        self.progLbl.setText(msg)            
        # This only goes(?) if  the user has not grabbed the slider
        # The 'or' stops issue where the slider doesn't move after track finishes
        if pos == self.old_pos or pos < 1: 
            self.progSldr.setValue(time)
        elif self.progSldr.value() == self.progSldr.maximum():
            self.progSldr.setValue(time)
        self.old_pos = time
 
#TODO: increment the playcount in DB 
    def about_to_finish(self):
        """
        Generates a track to go into queue
        before playback stops
        """
        track = self.generate_track("next")
        #Not at end of  playlist
        if track:
            self.playbin.enqueue(track)

    def set_prog_sldr(self):
        """
        Linked to the current time of
        track being played
        """
        self.progSldr.setRange(0, self.play_time)
        self.t_length = QTime(0, (self.play_time / 60000) % 60, (self.play_time / 1000) % 60)
            
    def state_changed(self, new, old):
        """
        This is linked to phonon.State. A very unreliable feature.
        """
        print "debug: Phonon.State: %s -> %s" % (new, old)

        # Prevents the slider being reset if playback is 
        # paused or unpaused
        if self.playbin.is_playing():
            if not ((new == 2) and ( old == 4)):
                self.set_prog_sldr()
        # Stopped playing and at end of playlist
        if new == 1 and old == 2 and self.is_last():
            print "debug: stopped\n"
            self.finished_playing()
            
    def finished_playing(self):
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
        """
        Does what it says.
        """
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
            if self.playbin.is_playing():
                self.playBttn.setChecked(False)
            else:
                self.playBttn.setChecked(True)
                
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
            current = self.playbin.current_source()
            # If 0 then the playlist is empty
            rows = self.playlistTree.rowCount() 
            if rows > 0:
                for row in range(rows):
                    file_name = str(self.playlistTree.item(row, column).text())
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
            return str(track)

    def generate_info(self):
        """
         This retrieves data from the playlist table, not the database. 
        This is because the playlist may contain tracks added locally.        
        """
        #TODO: need to check messages aren't too long
        row = self.current_track()
        title = self.playlistTree.item(row, 1).text()
        artist = self.playlistTree.item(row, 2).text()
        album = self.playlistTree.item(row, 3).text()
        
        min, sec = self.playlistTree.item(row, 6).text().split(":")
        self.play_time = 1000 * ((int(min) * 60) + int(sec))
        
        msg1 = QString("Now Playing")
        msg2 = QString("%s by %s" % (title, artist))
        msg3 = QString("%s - %s\n%s" % (title, artist, album))
        self.trkNowBox.setTitle(msg3)
        icon = QSystemTrayIcon.NoIcon
        if self.show_messages:
            self.tray_icon.showMessage(msg1, msg2, icon, 3000)
        message = "Playing: %s by %s on %s" % (title, artist, album)
        self.stat_lbl.setText(message)
        self.tracknow_colourise(row)
        self.art[2] = artist.toUtf8()
        self.art[3] = album.toUtf8()
        self.set_info()
        self.set_prog_sldr()
        self.old_pos = 0
        self.progSldr.setValue(0)

    def is_last(self):
        """
        Checks whether the current track in self.playbin
        is the last in the viewable playlist
        """
        now = self.playbin.current_source()
        file_list = self.gen_file_list()
        try:
            pos = file_list.index(QString(now))
        except:
            pos = None
        if  pos and  pos ==  len(file_list):
            return True        

    def gen_file_list(self):
        """
        Creates a list of files in the playlist at its
        current sorting top to bottom
        """
        column = 8
        rows = self.playlistTree.rowCount() 
        file_list = [self.playlistTree.item(row, column).text() for row in range(rows)]
        return file_list   
        
    def play_type(self, checked):
        if checked:
            self.play_type_bttn.setText("R")
        else:
            self.play_type_bttn.setText("N")

# FIXME: de-uglify
    def add2playlist(self, file_name, info):
        """
        Called when adding tracks to the playlist either locally
        or from the database. Does not pull metadata from 
        the database and is passed into the function directly
        """
        #TODO: prevent creation of empty rows.
        print(info)
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

#TODO: use native/theme colours for odd/even colours
    def tracknow_colourise(self, now):
        """
        Instead of using QTableWidget's selectRow function, 
        set the background colour of each item in a row
        until track changes.
        """
        self.playlistTree.selectRow(now)
        columns = self.playlistTree.columnCount()
        rows = self.playlistTree.rowCount()
        now_colour =  QColor(128, 184, 255, 128)
        odd_colour = QColor(220, 220, 220, 128)
        even_colour = QColor(255, 255, 255)
        for row in range(rows):
            for col in range(columns):
                item = self.playlistTree.item(row, col)
                if row != now:
                    if row % 2:
                        item.setBackgroundColor(odd_colour)
                    else:
                        item.setBackgroundColor(even_colour)
                else:
                    item.setBackgroundColor(now_colour)
    
    def highlighted_track(self):
        """
        In the playlist
        """
        column = 8
        row = self.playlistTree.currentRow()
        # -1 is the value for None
        if row > -1:
            track = self.playlistTree.item(row, column).text()
        else:
            track = None
        return track
        
