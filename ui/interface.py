#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow, QFileDialog,   \
QTableWidgetItem, QDesktopServices, QSystemTrayIcon, \
QIcon, QTreeWidgetItem, QPixmap, QMessageBox, QColor
from PyQt4.QtCore import QString, Qt, QTime, \
QStringList, SIGNAL, SLOT
from random import randrange

from settings import Setting_Dialog
from database import Media
from tagging import Tagging
from threads import Getcover, Getwiki, Builddb
from setups import Setups
from Ui_interface import Ui_MainWindow
from gstbe import Gstbe
from extraneous import Extraneous


class AudioBackend:
    def __init__(self, backend="gstreamer"):
        if backend == "gstreamer":
            self.gstreamer_init()
            
    def gstreamer_init(self):
        self.audio_object = Gstbe()
        self.connect(self.audio_object, SIGNAL("tick ( int )"), self.prog_tick)
        self.audio_object.pipe_line.connect("about-to-finish",  
                                            self.about_to_finish)
        self.connect(self.audio_object, SIGNAL("track_changed()"), 
                                               self.track_changed)
        self.connect(self.audio_object, SIGNAL("finished()"), 
                                               self.finished_playing)
        
# Not sure this is the correct place for this method
    def track_changed(self):
        """
        When the playing track changes certain
        Ui features may need to be updated.
        """
        print("TRACK CHANGED")
        self.generate_info()
        self.set_info()
        self.set_prog_sldr()
        MainWindow.old_pos = 0
        self.progSldr.setValue(0)
        
    def finished_playing(self):
        """
        Things to be performed when the playback finishes
        """
        print("FINISHED")
        self.contentTabs.setTabEnabled(1, False)
        self.contentTabs.setTabEnabled(2, False)
        self.playBttn.setChecked(False)
        self.stopBttn.setEnabled(False)
        self.progSldr.setValue(0)
        MainWindow.old_pos = 0
        self.stat_lbl.setText("Stopped")
        self.progLbl.setText("00:00 | 00:00")
        # clear things like wiki and reset cover art to default        
        self.wikiView.setHtml(QString(""))
        self.coverView.setPixmap(QPixmap(":/Icons/music.png"))
        self.trkNowBox.setTitle(QString("No Track Playing"))
        self.art_alb["oldart"] = self.art_alb["oldalb"] = None
        self.tray_icon.setToolTip("Stopped")
        
#TODO: increment the playcount in DB 
    def about_to_finish(self, pipeline):
        """
        Generates a track to go into queue
        before playback stops
        """
        print("ABOUT TO FINISH", pipeline)
        track = self.generate_track("next")
        #Not at end of  playlist
        if track:
            self.audio_object.enqueue(track)


class Playlist:
    # TODO: find out how to get colour-scheme
    colours = {
               "odd": QColor(220, 220, 220, 128), 
               "even": QColor(255, 255, 255), 
               "now": QColor(128, 184, 255, 128), 
               "search": QColor(255, 128, 128, 128)}
               
 # FIXME: For the love of god, de-uglify
    def add2playlist(self, file_name, info=None):
        """
        Called when adding tracks to the playlist either locally
        or from the database. Does not pull metadata from 
        the database and is passed into the function directly
        """
        # Not sure whether to pull in Tagging for each track
        
        info = self.meta.extract(file_name) 
        row = self.playlistTree.rowCount()
        hdr = self.header_search
        # Creates each cell for a track based on info
        track = QTableWidgetItem(QString("%02u" % info[0]))
        track.setFlags(track.flags() ^ Qt.ItemIsEditable)
        title = QTableWidgetItem(QString(info[1]))
        title.setFlags(title.flags() ^ Qt.ItemIsEditable)
        artist = QTableWidgetItem(QString(info[2]))
        artist.setFlags(artist.flags() ^ Qt.ItemIsEditable)
        album = QTableWidgetItem(QString(info[3]))
        album.setFlags(album.flags() ^ Qt.ItemIsEditable)
        year = QTableWidgetItem(str(info[4]))
        year.setFlags(year.flags() ^ Qt.ItemIsEditable)
        genre = QTableWidgetItem(QString(info[5]))
        genre.setFlags(genre.flags() ^ Qt.ItemIsEditable)
        length = QTableWidgetItem(QString(info[6]))
        bitrate = QTableWidgetItem(QString(str(info[7])))
        file = QTableWidgetItem(QString(file_name))
        self.playlistTree.insertRow(row)
        #TODO: These column assignments have to be dynamic at some point
        self.playlistTree.setItem(row, hdr("Track"), track)
        self.playlistTree.setItem(row, hdr("Title"), title)
        self.playlistTree.setItem(row, hdr("Artist"), artist)
        self.playlistTree.setItem(row, hdr("Album"), album)
        self.playlistTree.setItem(row, hdr("Year"), year)
        self.playlistTree.setItem(row, hdr("Genre"), genre)
        self.playlistTree.setItem(row, hdr("Length"), length)
        self.playlistTree.setItem(row, hdr("Bitrate"), bitrate)
        self.playlistTree.setItem(row, hdr("FileName") , file)
        self.playlistTree.resizeColumnsToContents()   
        
    def gen_file_list(self):
        """
        Creates a list of files in the playlist at its
        current sorting top to bottom
        """
        rows = self.playlistTree.rowCount() 
        column = self.header_search("FileName")
        file_list = [self.playlistTree.item(row, column).text() for row in range(rows)]
        return file_list   

    def del_track(self):
        """
        Deletes selected tracks from playlist
        """
        items = self.playlistTree.selectedItems()
        for item in items:
            try:
                row = item.row()
                self.playlistTree.removeRow(row)
            except RuntimeError:
                # likely deleted already i.e selected same row but multiple columns
                return  
                
        #TODO: use native/theme colours for odd/even colours
    def tracknow_colourise(self, now):
        """
        Instead of using QTableWidget's selectRow function, 
        set the background colour of each item in a row
        until track changes.
        """
        if now:
            self.playlistTree.selectRow(now)
            columns = self.playlistTree.columnCount()
            rows = self.playlistTree.rowCount()
            for row in range(rows):
                for col in range(columns):
                    item = self.playlistTree.item(row, col)
                    if row != now:
                        if row % 2:
                            item.setBackgroundColor(Playlist.colours["odd"])
                        else:
                            item.setBackgroundColor(Playlist.colours["even"])
                    else:
                        item.setBackgroundColor(Playlist.colours["now"])
                    
                    
    def header_search(self, val):
        """
        This will eventually allows the column order of the 
        playlist view to be changed         
        """
        cols = self.playlistTree.columnCount()
        headers = [self.playlistTree.horizontalHeaderItem(col).text() for col in range(cols)]
        return headers.index(val)
        
    def highlighted_track(self):
        """
        In the playlist
        """
        row = self.playlistTree.currentRow() # It's things like this I have no idea how to sort out
        column = self.header_search("FileName")
        track = None
        # -1 is the row value for None
        if row > -1:
            track = self.playlistTree.item(row, column).text()
        return track

# This needs to work with Ui_MainWindow somehow
class Track:

    def generate_track(self, mode, row=None):
        """
        As the playlist changes on sorting, the playlist (the immediately next/previous 
        tracks) has to be regenerated before the queing of the next track
        """
        # So that it can be dynamic later on when columns can be moved
        column = self.header_search("FileName")
        track = None
        if mode == "now":
            track = self.playlistTree.item(row, column).text()
        else:
            # If 0 then the playlist is empty
            rows = self.playlistTree.rowCount() 
            if rows > 0:
                row_now = self.current_row()
                if mode == "back":
                    if (row_now - 1) >= 0:
                        track = self.playlistTree.item(row_now - 1 , column)
                        track = track.text()
                elif mode == "next":
                    if self.play_type_bttn.isChecked():
                        # Here we need to randomly choose the next track
                        row = randrange(0, rows)
                        track = self.playlistTree.item(row, column)
                        track = track.text()
                    else:
                        if (row_now + 1) < rows:
                            track = self.playlistTree.item(row_now + 1, column)
                            track = track.text()
        if track:
            return str(track)
            
    def generate_info(self):
        """
         This retrieves data from the playlist table, not the database. 
        This is because the playlist may contain tracks added locally.        
        """
        row = self.current_row()
        title = self.playlistTree.item(row, 1).text()
        artist = self.playlistTree.item(row, 2).text()
        album = self.playlistTree.item(row, 3).text()
        
        # FIXME: Track total-time from playlist entry not playbin
        min, sec = self.playlistTree.item(row, 6).text().split(":")
        self.play_time = 1000 * ((int(min) * 60) + int(sec))
        
        msg1 = QString("Now Playing")
        msg2 = QString("%s by %s" % (title, artist))
        msg3 = QString("%s - %s\n%s" % (title, artist, album))
        # FIXME: Frankly this is crap. You cannot put any '\n' in the Qstring
        # which the title will understand. It's a single line only.
        self.trkNowBox.setTitle(msg3)
        if MainWindow.show_messages and self.playBttn.isChecked():
            self.tray_icon.showMessage(msg1, msg2, QSystemTrayIcon.NoIcon, 3000)
        self.tray_icon.setToolTip(msg2)
        message = "Playing: %s by %s on %s" % (title, artist, album)
        self.stat_lbl.setText(message)
        self.tracknow_colourise(row)
        MainWindow.art_alb["nowart"] = artist.toUtf8()
        MainWindow.art_alb["nowalb"] = album.toUtf8()
        

class MainWindow(Track, Playlist, AudioBackend,  Setups, Ui_MainWindow, QMainWindow): 
    """
    The main class of the app. There's loads of
    inherited Classes that may or may not have
    identical object/method names
    """    
    show_messages = True
    art_alb = {"oldart":None, "oldalb":None, "nowart":None, "nowalb":None} 
    old_pos = 0
    locale = ".com"
    audio_formats = ["flac","mp3","ogg"]
    
    def __init__(self, parent = None):
        """
        Initialisation of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
        QMainWindow.__init__(self, parent)
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        self.media_dir = None
        self.media_db = Media()
        self.cover_thread = Getcover()        
        self.html_thread = Getwiki()
        self.build_db_thread = Builddb()
        self.extras = Extraneous()
        self.meta = Tagging(MainWindow.audio_formats)
        self.init_setups()
        
        self.connect(self.build_db_thread, SIGNAL("finished ( QString ) "), self.__finish_build)
        self.connect(self.cover_thread, SIGNAL("got-image ( QImage ) "), self.__set_cover) 
        self.connect(self.html_thread, SIGNAL("got-wiki ( QString ) "), self.__set_wiki)
        self.connect(self.build_db_thread, SIGNAL("progress ( int ) "), self.stat_prog, SLOT("setValue(int)"))
        
        self.parentTabs.setTabEnabled(2, False)
        self.parentTabs.setTabEnabled(3, False)
        
    def on_srchCollectEdt_textChanged(self, p0):
        """
        This allows the filtering of the collection tree
        """
        srch = str(p0)
        self.setup_db_tree(filt=srch)       
        
    def on_collectTree_itemDoubleClicked(self, item, column):
        """
        When double click and abum in the collection browser
        add the album's tracks to the playlist.
        """
        now = item.text(0)
        par = item.parent()
        track = album = artist = None

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
        artist = self.extras.qstr2uni(artist)
        if track:
            album = self.extras.qstr2uni(album)     
            track = self.extras.qstr2uni(track)
            file_name = self.media_db.get_file(artist, album, track)
            self.add2playlist(file_name)
        elif album:
            album = self.extras.qstr2uni(album)
            tracks = self.media_db.get_files(artist, album)
            for track in tracks:
                # Retrieves metadata from database
                self.add2playlist(track)
    
    def on_prevBttn_pressed(self):
        """
        Skip to previous track in viewable playlist
        if possible
        """
        track = self.generate_track("back")
        if track:
            self.audio_object.stop()
            self.audio_object.load(track)
            # Checks to see if the playbutton is in play state
            if self.playBttn.isChecked():
                self.audio_object.play()
            # Just highlight the track we would play
            else:
                self.tracknow_colourise(self.current_row())

    #TODO: this can be called from 2 other actions. Needs tidy up.
    def on_playBttn_toggled(self, checked):
        """
        The play button either resumes or starts playback.
        Not possible to play a highlighted row.
        """
        #TODO: messy. Clean up.
        if checked:
            queued = self.audio_object.current_source()
            #FIXME: try and invert the result for less confusing varName
            stopped = self.stopBttn.isEnabled() is False
            highlighted = self.highlighted_track()
            if highlighted:      
                # Checks to see if highlighted track matches queued track
                # prevents loading whilst playing
                if (queued != highlighted) and stopped: 
                    queued = highlighted
                    self.audio_object.load(queued)
                # Nothing already loaded into playbin
                elif not queued:
                    selected = self.playlistTree.currentRow()
                    # A row is selected
                    if selected >= 0:
                        selected = self.generate_track("now", selected)           
                        self.audio_object.load(str(selected))
                    # Just reset the play button and stop here
                    else:
                        # This will call this function
                        self.playBttn.setChecked(False)
                self.audio_object.play()
                self.stopBttn.setEnabled(True)
                icon = QIcon(QPixmap(":/Icons/media-playback-pause.png"))
                tray = QIcon(QPixmap(":/Icons/app.png"))
                self.playBttn.setIcon(icon)
                self.tray_icon.setIcon(tray)
            else:
                self.playBttn.setChecked(False)
                return
        else:
            if self.audio_object.is_playing():
                self.audio_object.pause()
            icon = QIcon(QPixmap(":/Icons/media-playback-start.png"))
            tray = QIcon(QPixmap(":/Icons/app-paused.png"))
            self.playBttn.setIcon(icon)
            self.tray_icon.setIcon(tray)
            if self.playlistTree.currentRow() >= 0:
                self.stat_lbl.setText("Paused")
            else:
                self.stat_lbl.setText("Finished")
        self.play_action.setChecked(checked)
        self.actionPlay.setChecked(checked)
        
    def on_stopBttn_pressed(self):
        """
        To stop current track.
        """
        self.contentTabs.setTabEnabled(1, False)
        self.contentTabs.setTabEnabled(2, False)
        self.audio_object.stop()
        self.playBttn.setChecked(False)
        self.stopBttn.setEnabled(False)
        self.finished_playing()
        
    def on_nxtBttn_pressed(self):
        """
        Go to next item in playlist(down)
        """
        track = self.generate_track("next")
        if track:
            self.audio_object.stop() 
            self.audio_object.load(track)
            if self.playBttn.isChecked():
                self.audio_object.play()
            else:
                self.tracknow_colourise(self.current_row())
        else:
            # TODO: some tidy up thing could go here
            return
        
    def on_volSldr_valueChanged(self, value):
        """
        Self explanatory
        """        
        self.volLbl.setText("%s" % value)
        value = (value / 100.0) ** 2
        self.audio_object.set_volume(value)
    
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
            
    def on_actionRescan_Collection_triggered(self):
        """
        Scans through a directory and looks for supported media,
        extracts metadata and adds them to the database,hopefully.
        Really needs to be done in a separate thread as scan could
        take a while.
        """
        print "Rebuild: Ensure the db is ON CONFLICT REPLACE"
        self.create_collection()
    
    def on_actionQuit_triggered(self):
        """
        Closing Down. Maybe some database interaction.
        """
        exit()
    
    def on_actionPlay_Media_triggered(self):
        """
        Extract music files and shove into current playlist.
        """        
        mfiles = QFileDialog.getOpenFileNames(\
                        None, 
                        self.trUtf8("Select Music Files"),
                        QDesktopServices.storageLocation(QDesktopServices.MusicLocation), 
                        #TODO: do not hard-code this
                        self.trUtf8("*.flac *.mp3 *.ogg"), 
                        None)       
                        
        if mfiles:
            for item in mfiles:
                fname = self.extras.qstr2uni(item)
                ender = fname.split(".")[-1]
                if ender.lower() in MainWindow.audio_formats:
                    self.add2playlist(fname)

    def on_actionMinimise_to_Tray_triggered(self, checked):
        """
        Things to do when ui is minimised
        """
        self.minimise_to_tray(checked)
    
    def on_actionClear_triggered(self):
        """
        Clear current playlist and if no music playing
        clear self.audio_object
        """
        #TODO:incorporate playlists in to here.
        # When cleared save the playlist first to be
        # used with the playlist undo/redo buttons
        self.playlistTree.clearContents()
        rows = self.playlistTree.rowCount()
        # For some reason can only remove from bot to top
        for cnt in range(rows, -1, -1):
            self.playlistTree.removeRow(cnt)
    
    def on_clrplyBttn_clicked(self):
        """
        Clears current playlist
        """
        self.on_actionClear_triggered()
    
    def on_srchplyEdit_textChanged(self, p0):
        """
        Filters current playlist based on input.
        Not sure whether to highlight row or item
        """
        # Resets before searching again
        now = self.current_row()
        print now
        if now:
            self.tracknow_colourise(now)
        test = len(str(p0).strip())
        # Checks if the search edit isn't empty
        if test > 0:
            rows = []
            columns = self.playlistTree.columnCount()
            searched = self.playlistTree.findItems(p0, Qt.MatchContains)
            for search in searched:
                row = search.row()
                if not row in rows:
                    rows.append(row)
                    for col in range(columns):
                        item = self.playlistTree.item(row, col)
                        item.setBackgroundColor(Playlist.colours["search"])
                
    def on_muteBttn_toggled(self, checked):
        """
        Mutes audio output and changes button icon accordingly
        """
        self.audio_object.mute(checked)
        if checked:
            icon = QIcon(QPixmap(":/Icons/audio-volume-muted.png"))
            self.muteBttn.setIcon(icon)
        else:
            vol = (self.volSldr.value() / 100.0) ** 2
            icon = QIcon(QPixmap(":/Icons/audio-volume-high.png"))
            self.muteBttn.setIcon(icon)
            self.audio_object.set_volume(vol)
        
    def on_progSldr_sliderReleased(self):
        """
        Set's an internal seek value for tick() to use
        """
        val = self.progSldr.value()
        self.audio_object.seek(val)
        MainWindow.old_pos = val
    
    def on_actionUpdate_Collection_triggered(self):
        """
        Updates collection for new files. Ignore files already in database
        """
        # TODO: not completed yet. See self.create_collection
        print "Rebuild: Ensure the db is ON CONFLICT IGNORE"
        self.create_collection()

#FIXME: this causes a double-trigger of playbin.play() on app's
# first play.
    def on_playlistTree_cellDoubleClicked(self, row, column):
        """
        When item is doubleclicked. Play its row.
        """
        #This won't actualy stop. It'll pause instead.
        self.playBttn.setChecked(False)
        
        self.audio_object.stop()
        track = self.generate_track("now", row)
        self.audio_object.load(track)
        
        # Checking the button is the same
        #  as self.audio_object.play(), just cleaner overall
        self.playBttn.setChecked(True) 
        self.play_action.setChecked(True)
        
    def on_actionHelp_activated(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.information(None,
            self.trUtf8("Help"),
            self.trUtf8("""Boo!"""))

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
        artist = self.extras.qstr2uni(artist)
        #TODO: add tracks in trackNum order
        if album and (item.childCount() == 0):
            # Adding tracks to album
            album = self.extras.qstr2uni(album)
            tracks = self.media_db.get_titles(artist, album)
            for cnt in range(len(tracks)):
                track = tracks[cnt][0]
                track = QStringList(track)                
                track = QTreeWidgetItem(track)
                item.insertChild(cnt, track)
        elif item.childCount() == 0: 
            # Adding albums to the artist
            albums = self.media_db.get_albums(artist)
            for cnt in range(len(albums)):
                album = albums[cnt][0]
                album = QStringList(album)                
                album = QTreeWidgetItem(album)
                album.setChildIndicatorPolicy(0)
                item.insertChild(cnt, album)

    def on_clrCollectBttn_clicked(self):
        """
        Clears the collection search widget and in turn
        resets the collection tree
        """
        #TODO: expand the artist chosen before reset
        self.srchCollectEdt.clear()

    def on_collectTimeBox_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        filt = self.srchCollectEdt.text()
        filt = str(filt)
        self.setup_db_tree(filt)
        now = self.extras.date_now()
        print "Filter collectionTree WRT time.", now
        
    def on_actionAbout_Gereqi_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.aboutQt(None, 
            self.trUtf8(""))
            
    def on_clrsrchBttn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.srchplyEdit.clear()
        self.tracknow_colourise(self.current_row())
        #FIXME: need playbin.clearqueue()
        
        
#######################################
#######################################
        
    def quit_build(self):
        #TODO: confirm the below. May be old news.
        # ugly doesn't terminate cleanly
        # causes poor performance and errors on a rescan
        # locks up database
        print self.build_db_thread.stop_now() 

# This is needed as the higlighted row can be different
# than the currentRow method of Qtableview.
    def current_row(self):
        """
        Finds the playlist row of the
        currently playing track
        """
        file_list = self.gen_file_list()
        file_name = self.audio_object.current_source()
        if file_name:
            return file_list.index(file_name)
        
    def prog_tick(self, time):
        """
        Every second update time labels and progress slider
        """
        pos = self.progSldr.value()
        t_now = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        now = t_now.toString('mm:ss')
        maxtime = self.t_length.toString('mm:ss')
        msg = "%s | %s" % (now, maxtime)
        self.progLbl.setText(msg)            
        # This only goes(?) if  the user has not grabbed the slider
        # The 'or' stops issue where the slider doesn't move after track finishes
        if pos == MainWindow.old_pos: 
            self.progSldr.setValue(time)
        MainWindow.old_pos = time
 
    def set_prog_sldr(self):
        """
        Linked to the current time of
        track being played
        """
        self.progSldr.setRange(0, self.play_time)
        self.t_length = QTime(0, (self.play_time / 60000) % 60, (self.play_time / 1000) % 60)
            
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
    
    def create_collection(self):
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
            self.build_db_thread.set_values(self.media_dir, MainWindow.audio_formats)
            self.stat_prog.setToolTip("Scanning Media")
            self.stat_prog.setValue(0)
            self.build_db_thread.start()

    def set_info(self):
        """
        The wikipedia page + album art to current artist playing
        """
        # Wikipedia info
        if (self.art_alb["nowart"] != self.art_alb["oldart"] ) and self.art_alb["nowart"]:
            # passes the artist to the thread
            self.html_thread.set_values(self.art_alb["nowart"]) 
            # starts the thread
            self.html_thread.start() 
            self.art_alb["oldart"] = self.art_alb["nowart"]
        # Album art
        if (self.art_alb["nowalb"] != self.art_alb["oldalb"]) and self.art_alb["nowalb"]:
            self.cover_thread.set_values(self.art_alb["nowalb"], self.art_alb["nowart"], MainWindow.locale)
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
            stopped = self.audio_object.is_playing() is False
            self.playBttn.setChecked(stopped)

    def closeEvent(self, event):
        """
        When the 'X' button or alt-f4 is triggered
        """
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
            
    # I honestly could not figure out how to deal with Finishes.
    # Inheritance, attributes, etc is turning my brain to mush
            
    def __set_cover(self, img):
        if img.isNull():
            self.coverView.setPixmap(QPixmap(":/Icons/music.png"))
        else:
            cover = QPixmap()
            cover = cover.fromImage(img)
            cover = cover.scaledToWidth(200, Qt.SmoothTransformation)
            self.coverView.setPixmap(cover)        
        
    def __set_wiki(self, html):
        if html != "None":
            self.contentTabs.setTabEnabled(2, True)
            self.wikiView.setHtml(html)
        else:
            self.contentTabs.setTabEnabled(2, False)
            
    def __finish_build(self, status):
        """
        Things to perform when the media library
        has been built/cancelled
        """
        self.stat_bttn.setEnabled(False)
        if status == "cancelled":
            self.stat_prog.setToolTip("cancelled")
        else:
            self.stat_prog.setToolTip("Finished")
        self.stat_prog.setValue(100)
        self.collectTree.clear()
        self.setup_db_tree()

