#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Yes already. I know what this looks like. Absolutely awful so
stop telling me already. At least give me a few pointers. I'm
lost when it comes to Class aggregation.
"""
from PyQt4.QtGui import QMainWindow, QFileDialog,   \
QTableWidgetItem, QDesktopServices, QSystemTrayIcon, \
QIcon, QTreeWidgetItem, QPixmap, QMessageBox, QColor, \
QFont, QShortcut, QKeySequence, QLabel, QProgressBar, \
QToolButton, QAction, QSystemTrayIcon, \
qApp, QDirModel, QMenu
from PyQt4.QtCore import QString, Qt, QTime, SIGNAL, \
SLOT, QFile, QDir, QSize, QObject

from random import randrange

from settings import Setting_Dialog
from database import Media
from tagging import Tagging
from threads import Getcover, Getwiki, Builddb
from gstbe import Gstbe
from extraneous import Extraneous
from Ui_interface import Ui_MainWindow

class Finish:
    def __init__(self, BaseObject):
        self.ui = BaseObject

    def db_build(self, status):
        """
        Things to perform when the media library
        has been built/cancelled
        """
        self.ui.xtrawdgt.stat_bttn.setEnabled(False)
        if status == "cancelled":
            self.ui.xtrawdgt.stat_prog.setToolTip("cancelled")
        else:
            self.ui.xtrawdgt.stat_prog.setToolTip("Finished")
        self.ui.xtrawdgt.stat_prog.setValue(100)
        self.ui.collectTree.clear()
        self.ui.setup_db_tree()
        
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
    def __init__(self, BaseObject, backend="gstreamer"):
        self.ui = BaseObject
        if backend == "gstreamer":
            self.__gstreamer_init()
            
    def __gstreamer_init(self):
        self.audio_object = Gstbe()
        QObject.connect(self.audio_object, SIGNAL("tick ( int )"), self.__prog_tick)
        self.audio_object.pipe_line.connect("about-to-finish", self.__about_to_finish)
        QObject.connect(self.audio_object, SIGNAL("track_changed()"), self.__track_changed)
        QObject.connect(self.audio_object, SIGNAL("finished()"), self.__finished_playing)
        QObject.connect(self.ui.stopBttn, SIGNAL("clicked()"), self.__finished_playing)
        
    def __about_to_finish(self, pipeline):
        """
        Generates a track to go into queue
        before playback stops
        """
        print("ABOUT TO FINISH", pipeline)
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
        # FIXME: is generating maxtime each tick wasteful?
        maxtime = self.ui.t_length.toString('mm:ss')
        msg = "%s | %s" % (now, maxtime)
        self.ui.progLbl.setText(msg)            
        # Allows normal playback whilst slider still grabbed
        if self.ui.progSldr.value() == MainWindow.old_pos: 
            self.ui.progSldr.setValue(time)
        MainWindow.old_pos = time
        
    def __track_changed(self):
        """
        When the playing track changes certain
        Ui features may need to be updated.
        """
        print("TRACK CHANGED")
        self.ui.tracking.generate_info()
        self.ui.set_info()
        self.ui.set_prog_sldr()
        MainWindow.old_pos = 0
        self.ui.progSldr.setValue(0)
        
    def __finished_playing(self):
        """
        Things to be performed when the playback finishes
        """
        print("FINISHED")
        self.ui.contentTabs.setTabEnabled(1, False)
        self.ui.contentTabs.setTabEnabled(2, False)
        self.ui.playBttn.setChecked(False)
        self.ui.stopBttn.setEnabled(False)
        self.ui.progSldr.setValue(0)
        MainWindow.old_pos = 0
        self.ui.xtrawdgt.stat_lbl.setText("Stopped")
        self.ui.progLbl.setText("00:00 | 00:00")
        # clear things like wiki and reset cover art to default        
        self.ui.wikiView.setHtml(QString(""))
        # FIXME: seems to do nothing
        self.ui.coverView.setPixmap(QPixmap(":/Icons/music.png"))
        self.ui.trkNowBox.setTitle(QString("No Track Playing"))
        MainWindow.art_alb["oldart"] = MainWindow.art_alb["oldalb"] = None
        self.ui.xtrawdgt.tray_icon.setToolTip("Stopped")
        


class Playlist:
    def __init__(self, BaseObject):
        self.ui = BaseObject
        
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
        file_list = self.__gen_file_list()
        file_name = self.ui.player.audio_object.current_source()
        
        if file_name is not None:
            return file_list.index(file_name)
        
    def __gen_file_list(self):
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
                        item.setBackgroundColor(MainWindow.colours["odd"])
                    else:
                        item.setBackgroundColor(MainWindow.colours["even"])
                else:
                    item.setBackgroundColor(MainWindow.colours["now"])
                    self.ui.playlistTree.selectRow(now)
                        
    def highlighted_track(self):
        """
        In the playlist
        """
        row = self.ui.playlistTree.currentRow() # It's things like this I have no idea how to sort out
        column = self.header_search("FileName")
        track = None
        # -1 is the row value for None
        if row > -1:
            track = self.ui.playlistTree.item(row, column).text()
        return track        

class Track:
    def __init__(self, BaseObject):
        self.ui = BaseObject
        
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
        title = self.ui.playlistTree.item(row, 1).text()
        artist = self.ui.playlistTree.item(row, 2).text()
        album = self.ui.playlistTree.item(row, 3).text()
        
        # FIXME: Track total-time from playlist entry not playbin
        min, sec = self.ui.playlistTree.item(row, 6).text().split(":")
        self.play_time = 1000 * ((int(min) * 60) + int(sec))
        
        msg_header = QString("Now Playing")
        msg_main = QString("%s by %s" % (title, artist))
        self.ui.trkNowBox.setTitle(msg_main)
        if MainWindow.show_messages and self.ui.playBttn.isChecked():
            self.ui.xtrawdgt.tray_icon.showMessage(msg_header, msg_main, QSystemTrayIcon.NoIcon, 3000)
        self.ui.xtrawdgt.tray_icon.setToolTip(msg_main)
        self.msg_status = "Playing: %s by %s on %s" % (title, artist, album)
        self.ui.xtrawdgt.stat_lbl.setText(self.msg_status)
        self.ui.playlisting.tracknow_colourise(row)
        MainWindow.art_alb["nowart"] = artist.toUtf8()
        MainWindow.art_alb["nowalb"] = album.toUtf8()
        

class SetupExtraWidgets:
    def __init__(self, BaseObject):
        # Basically,the parent.
        self.ui = BaseObject
        self.__setup_fileview()
        self.__create_tray_menu()
        self.__playlist_add_menu()
        self.__disable_tabs()
        self.__setup_misc()
        self.__key_shortcuts()
        QObject.connect(self.play_type_bttn, SIGNAL('toggled ( bool )'), self.__play_type)

    def __setup_fileview(self):
        """
        A fileView browser where tracks can be (eventually)
        added to the playlist
        """
        self.dir_model = QDirModel()
        filters = QDir.Files | QDir.AllDirs | QDir.Readable | QDir.NoDotAndDotDot
        self.dir_model.setFilter(filters)
        self.dir_model.setReadOnly(True)
        self.dir_model.setNameFilters(["*.ogg","*.flac","*.mp3", "*.m4a"])
        self.ui.fileView.setModel(self.dir_model) 
        self.ui.fileView.setColumnHidden(1, True)
        self.ui.fileView.setColumnHidden(2, True)
        self.ui.fileView.setColumnHidden(3, True)
        self.ui.fileView.expandToDepth(0)
        
    def __create_tray_menu(self):
        """
        The tray menu contains shortcuts to features
        in the main UI
        """
        quit_action = QAction(QString("&Quit"), self.ui)
        self.play_action = QAction(QString("&Play"), self.ui)
        next_action = QAction(QString("&Next"), self.ui)
        prev_action = QAction(QString("&Previous"), self.ui)
        stop_action = QAction(QString("&Stop"), self.ui)
        self.play_action.setCheckable(True)
        self.view_action = QAction(QString("&Visible"), self.ui)
        self.view_action.setCheckable(True)
        self.view_action.setChecked(True)
        tray_icon_menu = QMenu(self.ui)
        icon = QIcon(QPixmap(":/Icons/app.png"))
        tray_icon_menu.addAction(icon, QString("Gereqi"))
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(prev_action)
        tray_icon_menu.addAction(self.play_action)
        tray_icon_menu.addAction(stop_action)
        tray_icon_menu.addAction(next_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(self.view_action)
        tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self.ui)
        icon2 = QIcon(QPixmap(":/Icons/app-paused.png"))
        self.tray_icon.setIcon(icon2)
        self.tray_icon.setContextMenu(tray_icon_menu)
        self.tray_icon.show()
        self.tray_icon.setToolTip("Stopped")    
        
        QObject.connect(self.play_action, SIGNAL("toggled(bool)"), self.ui.playBttn, SLOT("setChecked(bool)"))
        QObject.connect(next_action, SIGNAL("triggered()"), self.ui.nxtBttn, SLOT("click()"))
        QObject.connect(prev_action, SIGNAL("triggered()"), self.ui.prevBttn, SLOT("click()"))
        QObject.connect(stop_action, SIGNAL("triggered()"), self.ui.stopBttn, SLOT("click()"))
        QObject.connect(self.view_action, SIGNAL("toggled(bool)"), self.ui.minimise_to_tray)  
        QObject.connect(quit_action, SIGNAL("triggered()"), qApp, SLOT("quit()"))
        QObject.connect(self.tray_icon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.ui.tray_event)

     
    def __playlist_add_menu(self):
        """
        In the 'playlist' tab a menu is required for
        the 'add' button
        """
        menu = QMenu(self.ui)
        playlist_menu = QMenu(self.ui)
        playlist_menu.setTitle(QString("Playlist"))
        new = QAction(QString("New..."), self.ui)
        existing = QAction(QString("Import Existing..."), self.ui)
        playlist_menu.addAction(new)
        playlist_menu.addAction(existing)        
        menu.addMenu(playlist_menu)
        smart = QAction(QString("Smart Playlist..."), self.ui)
        dynamic = QAction(QString("Dynamic Playlist..."), self.ui)
        radio = QAction(QString("Radio Stream..."), self.ui)
        podcast = QAction(QString("Podcast..."), self.ui)
        menu.addAction(smart)
        menu.addAction(dynamic)
        menu.addAction(radio)
        menu.addAction(podcast)
        self.ui.addPlylstBttn.setMenu(menu)
        
    def __disable_tabs(self):
        self.ui.contentTabs.setTabEnabled(1, False)
        self.ui.contentTabs.setTabEnabled(2, False)
        self.ui.parentTabs.setTabEnabled(2, False)
        self.ui.parentTabs.setTabEnabled(3, False)
        
    def __setup_misc(self):
        """
        Extra __init__ things to add to the UI
        """        
        self.ui.progSldr.setPageStep(0)
        self.ui.progSldr.setSingleStep(0)
        self.stat_lbl = QLabel("Finished")
        self.stat_prog = QProgressBar()
        self.stat_bttn = QToolButton()
        self.play_type_bttn = QToolButton()
        icon = QIcon(QPixmap(":/Icons/application-exit.png"))
        self.stat_prog.setRange(0, 100)
        self.stat_prog.setValue(100)
        self.stat_prog.setMaximumSize(QSize(100, 18))
        self.stat_bttn.setIcon(icon)
        self.stat_bttn.setAutoRaise(True)
        self.stat_bttn.setEnabled(False)
        self.play_type_bttn.setText("N")
        self.play_type_bttn.setCheckable(True)
        self.play_type_bttn.setAutoRaise(True)
        self.ui.statusBar.addPermanentWidget(self.stat_lbl)
        self.ui.statusBar.addPermanentWidget(self.stat_prog)
        self.ui.statusBar.addPermanentWidget(self.stat_bttn)
        self.ui.statusBar.addPermanentWidget(self.play_type_bttn)
        # Headers for the Playlist widget
        # TODO: dynamic columns at some point
        headers = [QString("Track"), QString("Title"), QString("Artist"), \
                   QString("Album"), QString("Year"), QString("Genre"),   \
                   QString("Length"), QString("Bitrate"), QString("FileName")]
        for val in range(len(headers)):
            self.ui.playlistTree.insertColumn(val)
        self.ui.playlistTree.setHorizontalHeaderLabels(headers)

    def __play_type(self, checked):
        if checked is True:
            self.play_type_bttn.setText("R")
        else:
            self.play_type_bttn.setText("N")
            
    def __key_shortcuts(self):
        delete = QShortcut(QKeySequence(QString("Del")), self.ui)
        QObject.connect(delete, SIGNAL("activated()"), self.ui.playlisting.del_track)   
            

class MainWindow(Ui_MainWindow, QMainWindow): 
    """
    Where everything starts from, mostly.
    """    
    show_messages = True
    art_alb = {"oldart":None, "oldalb":None, "nowart":None, "nowalb":None} 
    old_pos = 0
    locale = ".com"
    audio_formats = ["flac","mp3","ogg", "m4a"]
    colours = {
           "odd": QColor(220, 220, 220, 128), 
           "even": QColor(255, 255, 255), 
           "now": QColor(128, 184, 255, 128), 
           "search": QColor(255, 128, 128, 128)}
    
    def __init__(self, parent = None):
        """
        Initialisation of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
        QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.media_dir = None
        self.media_db = Media()
        self.cover_thread = Getcover()        
        self.html_thread = Getwiki()
        self.build_db_thread = Builddb()
        self.extras = Extraneous()
        self.meta = Tagging(MainWindow.audio_formats)
        self.player = AudioBackend(self)
        self.playlisting = Playlist(self)
        self.xtrawdgt = SetupExtraWidgets(self)
        self.tracking = Track(self)
        
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

        
        #Make the collection search line-edit have the keyboard focus on startup.
        self.srchCollectEdt.setFocus()
        self.setup_db_tree()
        
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
        artist = self.extras.qstr2uni(artist)
        if track is not None:
            album = self.extras.qstr2uni(album)     
            track = self.extras.qstr2uni(track)
            file_name = self.media_db.get_file(artist, album, track)
            self.playlisting.add_to_playlist(file_name)
        elif album is not None:
            album = self.extras.qstr2uni(album)
            tracks = self.media_db.get_files(artist, album)
            for track in tracks:
                # Retrieves metadata from database
                self.playlisting.add_to_playlist(track)
    
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
                self.tracking.tracknow_colourise(self.playlisting.current_row())

    #TODO: this can be called from 2 other actions. Needs tidy up.
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
        
    def on_stopBttn_pressed(self):
        """
        To stop current track.
        """
        self.contentTabs.setTabEnabled(1, False)
        self.contentTabs.setTabEnabled(2, False)
        self.player.audio_object.stop()
        self.playBttn.setChecked(False)
        self.stopBttn.setEnabled(False)
        
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
                self.playlisting.highlighted_track(self.playlisting.current_row())
        else:
            # TODO: some tidy up thing could go here
            return
        
    def on_volSldr_valueChanged(self, value):
        """
        Self explanatory
        """        
        value = (value / 100.0) ** 2
        self.player.audio_object.set_volume(value)
    
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
        print("Rebuild: Ensure the db is ON CONFLICT REPLACE")
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
                        self.trUtf8("*.flac *.mp3 *.ogg *.m4a"), 
                        None)       
                        
        if mfiles is not None:
            for item in mfiles:
                fname = self.extras.qstr2uni(item)
                ender = fname.split(".")[-1]
                if ender.lower() in MainWindow.audio_formats:
                    self.playlisting.add_to_playlist(fname)

    def on_actionMinimise_to_Tray_toggled(self, checked):
        self.minimise_to_tray(checked)
    
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
    
    def on_clrplyBttn_clicked(self):
        """
        Clears current playlist and sets focus
        on the search linedit
        """
        self.on_actionClear_triggered()
        self.srchplyEdit.setFocus()
    
    def on_srchplyEdit_textChanged(self, p0):
        """
        Filters current playlist based on input.
        Not sure whether to highlight row or item
        """
        # Resets before searching again
        now = self.playlisting.current_row()
        if now is not None:
            self.playlisting.highlighted_track(now)
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
                        item.setBackgroundColor(MainWindow.colours["search"])
                
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
        
    def on_progSldr_sliderReleased(self):
        """
        Set's an internal seek value for tick() to use
        """
        val = self.progSldr.value()
        self.player.audio_object.seek(val)
        MainWindow.old_pos = val
    
    def on_actionUpdate_Collection_triggered(self):
        """
        Updates collection for new files. Ignore files already in database
        """
        # TODO: not completed yet. See self.create_collection
        print("Rebuild: Ensure the db is ON CONFLICT IGNORE")
        self.create_collection()

#FIXME: this causes a double-trigger of playbin.play() on app's
# first play.
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
        if par is not None:
            artist = par.text(0)
            album = item.text(0)
        else:
            artist = item.text(0)
            album = None
        # An artist in any case
        artist = self.extras.qstr2uni(artist)
        #TODO: add tracks in trackNum order
        if (album is not None) and (item.childCount() == 0):
            # Adding tracks to album
            album = self.extras.qstr2uni(album)
            tracks = self.media_db.get_titles(artist, album)
            for cnt in range(len(tracks)):
                track = QTreeWidgetItem([ tracks[cnt][0] ] )
                item.insertChild(cnt, track)
        elif item.childCount() == 0: 
            # Adding albums to the artist
            albums = self.media_db.get_albums(artist)
            for cnt in range(len(albums)):      
                album = QTreeWidgetItem([ albums[cnt][0] ])
                album.setChildIndicatorPolicy(0)
                item.insertChild(cnt, album)

    def on_clrCollectBttn_clicked(self):
        """
        Clears the collection search widget and in turn
        resets the collection tree
        """
        #TODO: expand the artist chosen before reset
        self.srchCollectEdt.clear()
        self.srchCollectEdt.setFocus()

    def on_collectTimeBox_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        filt = self.srchCollectEdt.text()
        filt = str(filt)
        self.setup_db_tree(filt)
        now = self.extras.date_now()
        print("Filter collectionTree WRT time.", now)
        
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
        self.playlisting.highlighted_track(self.playlisting.current_row())
        #FIXME: need playbin.clearqueue()
        
        
#######################################
#######################################
        
    def quit_build(self):
        #TODO: confirm the below. May be old news.
        # ugly doesn't terminate cleanly
        # causes poor performance and errors on a rescan
        # locks up database
        print(self.build_db_thread.stop_now() )


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
                self.trUtf8("Select Media Directory"),
                self.trUtf8("/home"),
                QFileDialog.Options(QFileDialog.ShowDirsOnly))
        # If the dialog is cancelled in last if statement the below is ignored
        if self.media_dir is not None:
            self.xtrawdgt.stat_bttn.setEnabled(True)
            self.build_db_thread.set_values(self.media_dir, MainWindow.audio_formats)
            self.xtrawdgt.stat_prog.setToolTip("Scanning Media")
            self.xtrawdgt.stat_prog.setValue(0)
            self.build_db_thread.start()

# FIXME: Holy shit. What a mess. Fix
    def set_info(self):
        """
        The wikipedia page + album art to current artist playing
        """
        # Wikipedia info
        if (self.art_alb["nowart"] != self.art_alb["oldart"] ) and (self.art_alb["nowart"] is not None):
            # passes the artist to the thread
            self.html_thread.set_values(self.art_alb["nowart"]) 
            # starts the thread
            self.html_thread.start() 
            self.art_alb["oldart"] = self.art_alb["nowart"]
        # Album art
        if (self.art_alb["nowalb"] != self.art_alb["oldalb"]) and (self.art_alb["nowalb"] is not None):
            self.cover_thread.set_values(self.art_alb["nowalb"], 
                                         self.art_alb["nowart"], MainWindow.locale)
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
            # FIXME: do not hard code formats
            searcher.setNameFilters(["*.ogg","*.flac","*.mp3", "*.m4a"])
            for item in searcher.entryInfoList():
                fname = item.absoluteFilePath()
                self.playlisting.add_to_playlist(self.extras.qstr2uni(fname))
        else:
            fname = self.xtrawdgt .dir_model.filePath(index)
            self.playlisting.add_to_playlist(self.extras.qstr2uni(fname))
        

    def setup_db_tree(self, filt=None):
        """
        viewing the media database in the QTreeView
        """
        #TODO: make the creation aware of the collectTimeBox widget
        time_filter = self.collectTimeBox.currentIndex()
        self.collectTree.clear()
        # This gives multiples of the same thing i.e albums
        artists = self.media_db.get_artists()
        artists = sorted(artists)
        old_char = None
        char = None
        font = QFont()
        font.setBold(True)
        for cnt in range(len(artists)):
            artist = artists[cnt][0]
            # When creating collection tree only 
            #  allow certain artists based on the filter.
            # FIXME: not sure filt is not None is needed
            if (filt is not None) and (filt.lower() not in artist.lower()):
                continue
            char = artist[0]   
            if char != old_char:
                old_char = char  
                char = QTreeWidgetItem(["== %s ==" % char])
                char.setFont(0, font)
                self.collectTree.addTopLevelItem(char)
            artist = QTreeWidgetItem([QString(artist)])
            artist.setChildIndicatorPolicy(0)
            self.collectTree.addTopLevelItem(artist)
