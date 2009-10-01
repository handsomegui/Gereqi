# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, \
QDesktopServices, QAction, QMenu, QSystemTrayIcon, qApp, QIcon, QPixmap, QLabel, \
QProgressBar, QToolButton, QSpacerItem, QSizePolicy, QTreeWidgetItem, QFont, QPixmap,  \
QShortcut, QKeySequence
from PyQt4.QtCore import pyqtSignature, QDir, QString, Qt, SIGNAL, QTime, SLOT, \
QSize,  QStringList
from PyQt4.phonon import Phonon
from random import randrange

from settings import SETTINGDLG
from Ui_amaroq import Ui_MainWindow
import resource_rc
from database import MEDIA
from metadata import METADATA
from threads import GETCOVER, GETWIKI, BUILDDB

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    The main class of the app
    """    
    def __init__(self, parent = None):
        """
        Initialisation of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.mediaDB = MEDIA()
        self.mediaDir = None
        self.meta = METADATA()
        self.setupDBtree()
        self.windowShow = True
        self.playRandom = False
        self.oldPos = 0
        self.playLstEnd = False 
        self.coverThread = GETCOVER()
        self.htmlThread = GETWIKI()
        self.buildThread = BUILDDB()     
        self.localisation = ".co.uk" # this needs to be editable in the settings Dialog

        self.art = [None, None] # The current playing artist
        self.old_art = [None, None] # The last playing artist
        
        self.setupAudio()
        self.setupShortcuts()
        self.setupExtra()        
        self.createActions()        
        self.trayIcon.show()
        
        
    def setupAudio(self):
        """
        Audio backend stuff
        """
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        self.mediaObject.setTickInterval(1000)
        self.audioOutput.setVolume(1)
        
    def setupShortcuts(self):
        delete = QShortcut(QKeySequence(self.tr("Del")), self)
        
        self.connect(delete, SIGNAL("activated()"), self.delTrack) 
        
    def setupExtra(self):
        """
        Extra __init__ things to add to the UI
        """
        self.progSldr.setPageStep(0)
        self.progSldr.setSingleStep(0)
        self.statLbl = QLabel("Finished")
        self.statProg = QProgressBar()
        self.statBttn = QToolButton()
        self.statPlyTypBttn = QToolButton()
        icon = QIcon(QPixmap(":/Icons/application-exit.png"))
        
        self.statProg.setRange(0, 100)
        self.statProg.setValue(100)
        self.statProg.setMaximumSize(QSize(100,18))
        
        self.statBttn.setIcon(icon)
        self.statBttn.setAutoRaise(True)
        self.statBttn.setEnabled(False)
        
        self.statPlyTypBttn.setText("N")
        self.statPlyTypBttn.setCheckable(True)
        self.statPlyTypBttn.setAutoRaise(True)

        self.statusBar.addPermanentWidget(self.statLbl)
        self.statusBar.addPermanentWidget(self.statProg)
        self.statusBar.addPermanentWidget(self.statBttn)
        self.statusBar.addPermanentWidget(self.statPlyTypBttn)

        headers = [self.tr("Track"), self.tr("Title"), self.tr("Artist"), self.tr("Album"), \
                   self.tr("Year"), self.tr("Genre"),   self.tr("Length"), self.tr("Bitrate"), self.tr("FileName")]
        
        for val in range(len(headers)):
            self.playlistTree.insertColumn(val)
        self.playlistTree.setHorizontalHeaderLabels(headers)
    
    def createActions(self):
        self.quitAction = QAction(self.tr("&Quit"), self)
        self.playAction = QAction(self.tr("&Play"), self)
        self.nextAction = QAction(self.tr("&Next"), self)
        self.prevAction = QAction(self.tr("&Previous"), self)
        self.stopAction = QAction(self.tr("&Stop"), self)
        self.playAction.setCheckable(True)
        self.viewAction = QAction(self.tr("&Visible"), self)
        self.viewAction.setCheckable(True)
        self.viewAction.setChecked(True)
        
        self.createTrayIcon()
        
        self.connect(self.quitAction, SIGNAL("triggered()"), qApp, SLOT("quit()"))
        self.connect(self.playAction, SIGNAL("toggled(bool)"), self.on_playBttn_toggled)
        self.connect(self.nextAction, SIGNAL("triggered()"), self.on_nxtBttn_pressed)
        self.connect(self.prevAction, SIGNAL("triggered()"), self.on_prevBttn_pressed)
        self.connect(self.stopAction, SIGNAL("triggered()"), self.on_stopBttn_pressed)
        self.connect(self.viewAction, SIGNAL("toggled(bool)"), self.minimiseTray)
        self.connect(self.mediaObject, SIGNAL('tick(qint64)'), self.tick)
        self.connect(self.mediaObject, SIGNAL('aboutToFinish()'),self.aboutToFinish)
        self.connect(self.mediaObject, SIGNAL('finished()'),self.finished)
        self.connect(self.mediaObject, SIGNAL('stateChanged(Phonon::State, Phonon::State)'),self.stateChanged)
        self.connect(self.statPlyTypBttn, SIGNAL('toggled(bool)'), self.play_type)
        self.connect(self.coverThread, SIGNAL("Activated ( QImage ) "), self.setCover) # Linked to QThread
        self.connect(self.htmlThread, SIGNAL("Activated ( QString ) "), self.setWiki)
        self.connect(self.buildThread, SIGNAL("Activated ( int ) "), self.statProg.setValue)
        self.connect(self.buildThread, SIGNAL("Activated ( QString ) "), self.finBuild)
        self.connect(self.trayIcon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.trayEvent)
        self.connect(self.statBttn, SIGNAL("triggered()"), self.buildThread.exit)
        
    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        icon = QIcon(QPixmap(":/Icons/drawing.png"))
        
        self.trayIconMenu.addAction(icon, QString("Amaroq"))
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.prevAction)
        self.trayIconMenu.addAction(self.playAction)
        self.trayIconMenu.addAction(self.stopAction)
        self.trayIconMenu.addAction(self.nextAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.viewAction)
        self.trayIconMenu.addAction(self.quitAction)
        
        # No. This icon isn't final. Just filler.
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(icon)
        self.trayIcon.setContextMenu(self.trayIconMenu)       
        
    
    @pyqtSignature("")
    def on_clrBttn_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not finished
        self.srchEdt.clear()
    
    @pyqtSignature("")
    def on_srchEdt_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not finished
        print self.srchEdt.text()
    
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_collectTree_itemDoubleClicked(self, item, column):
        """
        When double click and abum in the collection browser
        add the album's tracks to the playlist.
        """
        album = item.text(column)
        
        try:
            artist = item.parent().text(0)
        except:
            # Should go here if the artist item is double-clicked as it has no parent
            return
        tracks = self.mediaDB.file_names(artist, album)
        
        for track in tracks:
            track = track[0]
            info = self.mediaDB.track_info(track)[0][1:] # Retrieves metadata from database
            self.add2playlist(str(track), info)
    
    @pyqtSignature("")
    def on_prevBttn_pressed(self):
        """
        Skip to previous track in viewable playlist
        if possible
        """
        
        track = self.genTrack("back")
        if track:
            self.mediaObject.stop()
            self.mediaObject.setCurrentSource(track)
            
            if self.isPlaying():
                self.mediaObject.play()            
            else:
                self.genInfo()


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
            queued = self.mediaObject.currentSource().fileName()
            
            if not queued:
                selected = self.playlistTree.currentRow()
                if selected >= 0:
                    selected = self.genTrack("now", selected)                
                    self.mediaObject.setCurrentSource(selected)
                else:
                    self.playBttn.setChecked(False)
                    return
                
            self.mediaObject.play()
            self.stopBttn.setEnabled(True)
            self.playBttn.setIcon(QIcon(QPixmap(":/Icons/media-playback-pause.png")))
            if not self.isPlaying():
                self.genInfo()
                
        else:
            self.mediaObject.pause()
            self.playBttn.setIcon(QIcon(QPixmap(":/Icons/media-playback-start.png")))
            self.statLbl.setText("Paused")
            
        self.playBttn.setChecked(checked)    
        self.playAction.setChecked(checked)
        
    @pyqtSignature("")
    def on_stopBttn_pressed(self):
        """
        To stop current track.
        """
        #TODO: disable the lyrics and wiki tabs
        self.mediaObject.stop()
        self.playBttn.setChecked(False)
        
        self.stopBttn.setEnabled(False)
        self.finished()
        
        
    
    @pyqtSignature("")
    def on_nxtBttn_pressed(self):
        """
        Go to next item in playlist(down)
        """
        track = self.genTrack("next")
        if track:
            self.mediaObject.stop()       
            self.mediaObject.setCurrentSource(track)
            if self.isPlaying():
                self.mediaObject.play()
        
    @pyqtSignature("int")
    def on_volSldr_valueChanged(self, value):
        """
        Self explanatory
        """        
        self.volLbl.setText("%s" % value)
        value = (value / 100.0) ** 2
        self.audioOutput.setVolume(value)
    
    @pyqtSignature("")
    def on_actionEdit_triggered(self):
        """
       Brings up the settings Dialog
        """
        # TODO: not finished yet
        dialog = SETTINGDLG(self)
        
        if dialog.exec_():
            self.mediaDir = dialog.dir_val()
            print self.mediaDir
            
    @pyqtSignature("")
    def on_actionRescan_Collection_triggered(self):
        """
        Scans through a directory and looks for supported media,
        extracts metadata and adds them to the database,hopefully.
        Really needs to be done in a separate thread as scan could
        take a while.
        """
        self.collection(True)
    
    @pyqtSignature("")
    def on_actionExit_triggered(self):
        """
        Closing Down. Maybe some database interaction.
        """
        exit()
    
    @pyqtSignature("")
    def on_actionPlay_Media_triggered(self):
        """
        Extract music files and shove into current playlist.
        """        
        # As the kde4 dialogs are being used (somehow) I can't see if the filters work
        mfiles = QFileDialog.getOpenFileNames(\
                        None, 
                        self.tr("Select Music Files"),
                        QDesktopServices.storageLocation(QDesktopServices.MusicLocation), 
                        self.trUtf8("*.flac;;*.mp3;;*.ogg"))       
           
        if mfiles:
            for item in mfiles:
                if item.endsWith(".ogg") or item.endsWith(".mp3") or item.endsWith(".flac"):
                    
                    info = self.meta.extract(item) # Added this so add2playlist can have data added from mediaDB
                    self.add2playlist(item, info)

    @pyqtSignature("int, int")
    def on_playlistTree_cellDoubleClicked(self, row, column):
        """
        When item is doubleclicked. Play its row.
        """
        self.mediaObject.stop()

        track = self.genTrack("now", row)
        self.mediaObject.setCurrentSource(track)
        self.mediaObject.play()
        self.playBttn.setChecked(True) 
        self.playAction.setChecked(True)
        
    def tick(self, time):
        """
        Every second update time labels and progress slider
        """
        pos = self.progSldr.sliderPosition()
        t_now = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        if t_now == QTime(0, 0, 0):
                # Used because no Phonon.state when the mediaobject goes to next queued track
                # 2,3 is the same sig as when next/prev buttons are used
            self.stateChanged(2, 3) 
        self.progLbl.setText("%s | %s" % (t_now.toString('mm:ss'), self.t_length.toString('mm:ss')))            
            
        # This only goes(?) if  the user has not grabbed the slider
        if pos == self.oldPos or pos < 1: # This or stops a problem where the slider doesn't move after the track finishes
            self.progSldr.setValue(time)
        
        
        self.oldPos = time
            
    def aboutToFinish(self):    
        track = self.genTrack("next")
        if track:
            self.mediaObject.enqueue(track)

    def setProgSldr(self):
        length = self.mediaObject.totalTime()
        self.progSldr.setValue(0)
        self.progSldr.setRange(0, length)
        self.oldPos = 0
        self.t_length = QTime(0, (length / 60000) % 60, (length / 1000) % 60)
            
    def stateChanged(self, old, new):      
        # Prevents the slider being reset if playback is paused
        # or unpaused
        if self.isPlaying():
            if not ((old == 2) and ( new == 4)):
                self.setProgSldr()
            
        if old == 2 and new == 3:         
            self.genInfo()
            self.setInfo()
            
        # Stopped playing and at end of playlist
        elif old == 1 and new == 2 and self.isLast():
            self.finished()
            
    def finished(self):
        self.playBttn.setChecked(False)
        self.stopBttn.setEnabled(False)
        
        self.progSldr.setValue(0)
        self.oldPos = 0
        self.statLbl.setText("Stopped")
        self.progLbl.setText("00:00 | 00:00")
        
        # clear things like wiki and reset cover art to default        
        self.wikiView.setHtml(QString(""))
        self.coverView.setPixmap(QPixmap(":/Icons/music.png"))
        self.old_art = [None, None]
        
    def minimiseTray(self, state):
        if state:
            self.show()            
        else:
            self.hide()
            
        self.windowShow = state #FIXME:Try and replace with a PyQt4 function
        self.viewAction.setChecked(state)
        self.actionMinimise_to_Tray.setChecked(state)
        
    @pyqtSignature("bool")
    def on_actionMinimise_to_Tray_triggered(self, checked):
        """
        Things to do when ui is minimised
        """
        self.minimiseTray(checked)
    
    @pyqtSignature("")
    def on_actionClear_triggered(self):
        """
        Clear current playlist and if no music playing
        clear self.mediaObject
        """
        self.playlistTree.clearContents()
        rows = self.playlistTree.rowCount()
        
        # For some reason can only remove from bot to top
        for x in range(rows, -1, -1):
            self.playlistTree.removeRow(x)
        
        self.mediaObject.clearQueue()
    
    @pyqtSignature("")
    def on_clrplyBttn_clicked(self):
        """
        Clears current playlist
        """
        self.on_actionClear_triggered()
    
    @pyqtSignature("")
    def on_srchplyEdit_returnPressed(self):
        """
        Filters current playlist based on input
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
        self.audioOutput.setMuted(checked)
        if checked:
            self.muteBttn.setIcon(QIcon(QPixmap(":/Icons/audio-volume-muted.png")))
        else:
            self.muteBttn.setIcon(QIcon(QPixmap(":/Icons/audio-volume-high.png")))
    
    def play_type(self, checked):
        if checked:
            self.statPlyTypBttn.setText("R")
        else:
            self.statPlyTypBttn.setText("N")

    def add2playlist(self, fileName, info):
        """
        Called when adding tracks to the playlist either locally
        or from the database. Does not pull metadata from 
        the database and is passed into the function directly
        """
        #TODO: prevent creation of empty rows
        meta = ["track", "title", "artist", "album", "year", "genre", "length", "bitrate", "file"]
        vals = len(meta)
        
        for n in range(vals):
            if meta[n] == "track":
                itemInfo = '''"%02u"''' % info[0]
            elif meta[n] == "file":
                itemInfo = '''"%s"''' % fileName
            else:
                itemInfo = "info[%d]" % n
                
            itemName = "%sItem" % meta[n]
            func1 = "QTableWidgetItem(QString(str(%s)))" % itemInfo
            func2 = "%s.setFlags(%s.flags() ^ Qt.ItemIsEditable)" % (itemName, itemName)
            
            exec "%s = %s" % (itemName, func1)
            exec func2
            
    
        currentRow = self.playlistTree.rowCount()
        self.playlistTree.insertRow(currentRow)
        
        fileCol = 8
        #TODO: These column assignments have to be dynamic at some point
        self.playlistTree.setItem(currentRow, 0, trackItem)
        self.playlistTree.setItem(currentRow, 1, titleItem)
        self.playlistTree.setItem(currentRow, 2, artistItem)
        self.playlistTree.setItem(currentRow, 3, albumItem)
        self.playlistTree.setItem(currentRow, 4, yearItem)
        self.playlistTree.setItem(currentRow, 5, genreItem)
        self.playlistTree.setItem(currentRow, 6, lengthItem)
        self.playlistTree.setItem(currentRow, 7, bitrateItem)
        self.playlistTree.setItem(currentRow, fileCol , fileItem)
        
        self.playlistTree.resizeColumnsToContents()
        if self.playlistTree.columnWidth(0) > 300:
                self.playlistTree.setColumnWidth(0, 300)
    
    
    # A much cleaner solution. When you seek the volume is momentarily
    # set to 100% so it can really standout. 
    @pyqtSignature("")
    def on_progSldr_sliderReleased(self):
        """
        Slot documentation goes here.
        """
        
        val = self.progSldr.value()
        self.mediaObject.seek(val)
        self.oldPos = val
    
    @pyqtSignature("")
    def on_actionUpdate_Collection_triggered(self):
        """
        Updates collection for new files. Ignore files already in database
        """
        # TODO: not completed yet. See self.collection
        self.collection(False)


    def collection(self, rebuild):
        """
        Either generates a new DB or adds new files to it
        Not finished
        """
        #TODO: finish the DB interaction
        
        if rebuild:
            # Here we change the PRIMARY KEY in the database to
            # ON CONFLICT REPLACE as we want to rebuild.
            print "Do something here:rebuild"
        else:
            # Here we check that the PRIMARY KEY in the database is
            # ON CONFLICT IGNORE as we want to add new files.
            print "Do something here:rescan"
            
        if not self.mediaDir:
            self.on_actionEdit_triggered()
   
        # If the dialog is cancelled in last if statement the below is ignored
        if self.mediaDir:
            self.statBttn.setEnabled(True)
            self.buildThread.set_values(self.mediaDir)
            self.statProg.setToolTip("Scanning Media")
            self.statProg.setValue(0)
            self.buildThread.start()

    def setupDBtree(self):
        """
        The beginnings of viewing the media database in the QTreeView
        """
        artists = self.mediaDB.query_db("artist") # This gives multiples of the same thing
        artists = sorted(artists)
        oldChar= None
        char = None
        font = QFont()
        font.setBold(True)
        
        #TODO: at the start of new letter in alphabet create a header/separator
        for n in range(len(artists)):
            artist = artists[n][0]
            try:char = str(artist)[0]
            except:char = ""            
            
            if char != oldChar:
                oldChar = char  
                char = "== %s ==" % char
                char = QStringList(char)
                char = QTreeWidgetItem(char)
                char.setFont(0, font)
                self.collectTree.addTopLevelItem(char)
               
            albums = self.mediaDB.searching("album", "artist", artist)
            artist = QStringList(artist)
            artist = QTreeWidgetItem(artist)
            self.collectTree.addTopLevelItem(artist)

            for album in albums:           
                album = album[0]
                album = QStringList(album)                
                album = QTreeWidgetItem(album)
                artist.addChild(album)

    def setInfo(self):
        """
        The wikipedia page + album art to current artist playing
        """        
        # Wikipedia info
        if self.art[0] != self.old_art[0] and self.art[0]: 
            self.htmlThread.set_values(self.art[0]) # passes the artist to the thread
            self.htmlThread.start() # starts the thread
            self.old_art[0] = self.art[0]         
        # Album art
        if self.art[1] != self.old_art[1] and self.art[1]:
            self.coverThread.set_values(self.art[0], self.art[1], self.localisation)
            self.coverThread.start()
            self.old_art[1] = self.art[1]

    def trayEvent(self, event):
        """
        Things to perform on user-interaction of the tray icon
        other than bringing up it's menu
        """
        winState = self.windowState()
        # hex val is supposed to indicate minimised
        # no idea how to extract it from windowState
#        print winState == 0x00000001 
        if event == 3:
            if self.windowShow:
                self.minimiseTray(False)
            else:
                self.minimiseTray(True)            
            
        # Middle-click to pause/play
        elif event == 4:
            if self.isPlaying():
                self.on_playBttn_toggled(False)
            else:
                self.on_playBttn_toggled(True)
                
    def delTrack(self):
        """
        Deletes selected tracks from playlist
        """
        items = self.playlistTree.selectedItems()
        for item in items:
            try:
                row = item.row()
                self.playlistTree.removeRow(row)
            except:
                return # it's probably deleted already i.e we selected the same row but multiple columns FIXME:tidy up
      
# TODO: these could be pushed into their own class
    def genTrack(self, mode, row=None):
        """
        As the playlist changes on sorting, the playlist (the immediately next/previous 
        tracks) has to be regenerated before the queing of the next track
        """
        column = 8 # So that it can be dynamic later on when columns can be moved
        if mode == "now":
            track = self.playlistTree.item(row, column).text()
            
        else:
            current = self.mediaObject.currentSource().fileName()
            rows = self.playlistTree.rowCount() # If 0 then the playlist is empty
            
            #FIXME: the elses encased in the 1st if are probably now pointless
            if rows > 0:
                for row in range(rows):
                    fileName = self.playlistTree.item(row, column).text()
                    
                    # Track, track, track.
                    if fileName == current:
                        if mode == "back":
                            if (row - 1) >= 0:
                                track = self.playlistTree.item(row - 1 , column).text()
                            else:
                                track = None
                            break
                            
                        elif mode == "next":
                            if self.statPlyTypBttn.isChecked():
                                # Here we need to randomly choose the next track
                                row = randrange(0, rows)
                                track = self.playlistTree.item(row, column).text()
                            else:
                                if (row + 1) < rows:
                                    track = self.playlistTree.item(row + 1, column).text()
                                else:
                                    track = None                            
                                break
                            
            else:
                track = None
                 
        if track:
            track = Phonon.MediaSource(track)      
            
        return track

    def genInfo(self):
        # This retrieves data from the playlist table, not the database. This is because
        # the playlist may contain tracks added locally.
        fileList = self.genFilelist()
        fileName = self.mediaObject.currentSource().fileName()
        row = fileList.index(fileName)
        
        title = self.playlistTree.item(row, 1).text()
        artist = self.playlistTree.item(row, 2).text()
        album = self.playlistTree.item(row, 3).text()
        message = "%s by %s" % (title, artist)
        self.trayIcon.showMessage(QString("Now Playing"), QString(message), QSystemTrayIcon.NoIcon, 3000)
        
        message = "Playing: %s by %s on %s" % (title, artist, album)
        self.statLbl.setText(message)
        self.playlistTree.selectRow(row) 
        self.art[0] = str(artist)
        self.art[1] = str(album)
        if row and self.wikiView.isVisible():
            self.setInfo()

    def isPlaying(self):
        state = self.mediaObject.state()
        if state == 2:
            return True
        else:
            return False

    def isLast(self):
        """
        Checks whether the current track in self.mediaObject
        is the last in the viewable playlist
        """
        now = self.mediaObject.currentSource().fileName()                
        fileList = self.genFilelist()
        fileCnt = len(fileList)
        try:
            pos = fileList.index(now)
        except:
            pos = None
        if  pos and  pos == fileCnt:
            return True        

    def genFilelist(self):
        column = 8
        rows = self.playlistTree.rowCount() 
        fileList = []
        
        for row in range(rows):
            item = self.playlistTree.item(row, column).text()
            fileList.append(item)  
        
        return fileList   
 
#FIXME: this is getting ridiculous. We need new classes. .

# These are linked to the threads emitting signals
    def setCover(self, img):
        cover = QPixmap()
        cover = cover.fromImage(img)
        cover = cover.scaledToWidth(200, Qt.SmoothTransformation)
        self.coverView.setPixmap(cover)        
        self.coverThread.exit() # Can't  hurt
        
    def setWiki(self, html):
        self.wikiView.setHtml(str(html))
        self.htmlThread.exit()
        

    def finBuild(self, status):
        print str(status)
        if str(status) == "finished":
            self.buildThread.exit()
            print "Scanned directory."
            self.statBttn.setEnabled(False)
            self.statProg.setToolTip("Finished")
            self.statProg.setValue(100)
            self.collectTree.clear()
            self.setupDBtree()

