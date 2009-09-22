# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, \
QDesktopServices, QAction, QMenu, QSystemTrayIcon, qApp, QIcon, QPixmap, QLabel, \
QProgressBar, QToolButton, QSpacerItem, QSizePolicy, QTreeWidgetItem, QFont, QPixmap
from PyQt4.QtCore import pyqtSignature, QDir, QString, Qt, SIGNAL, QTime, SLOT, \
QSize,  QStringList, QByteArray, QBuffer, QIODevice
from PyQt4.phonon import Phonon
import os
#from cStringIO import StringIO

from settings import settingDlg
from Ui_amaroq import Ui_MainWindow
import resource_rc
from database import media
from metadata import metaData
from webinfo import webInfo

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    
    def __init__(self, parent = None):
        """
        Initialisation of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.mediaDB = media()
        self.info = webInfo()
        self.mediaDir = None
        self.meta = metaData()
        self.setupDBtree()
        self.windowShow = True
        self.playRandom = False
        self.oldPos = 0
        self.playLstEnd = False        

        self.art = [None, None] # The current playing artist
        self.old_art = [None, None] # The last playing artist
        
        self.setupAudio()
        self.setupExtra()
        self.createActions()
        self.createTrayIcon()
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
        
   
    def setupExtra(self):
        """
        Extra __init__ things to add to the UI
        """
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
        self.statPlyTypBttn.setText("N")
        self.statPlyTypBttn.setCheckable(True)
        self.statPlyTypBttn.setAutoRaise(True)

        self.statusBar.addPermanentWidget(self.statLbl)
        self.statusBar.addPermanentWidget(self.statProg)
        self.statusBar.addPermanentWidget(self.statBttn)
        self.statusBar.addPermanentWidget(self.statPlyTypBttn)

        headers = [self.tr("Track"), self.tr("Title"), self.tr("Artist"), self.tr("Album"), \
                   self.tr("Year"), self.tr("Genre"), self.tr("FileName")]
        
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

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        
        self.trayIconMenu.addAction(self.viewAction) 
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.playAction)
        self.trayIconMenu.addAction(self.nextAction)
        self.trayIconMenu.addAction(self.prevAction)
        self.trayIconMenu.addAction(self.stopAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        
        # No. This icon isn't final. Just filler.
        icon = QIcon(QPixmap(":/Icons/drawing.png"))
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(icon)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        
        self.connect(self.trayIcon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.trayEvent)
    
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
        tracks = self.mediaDB.filenames(artist, album)
        
        for track in tracks:
            track = track[0]
            info = self.mediaDB.trackInfo(track)[0][1:] # Retrieves metadata from database
            self.add2playlist(str(track), info)
    
    @pyqtSignature("")
    def on_prevBttn_pressed(self):
        """
        Slot documentation goes here.
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
            self.mediaObject.play()
            self.stopBttn.setEnabled(True)
            self.playBttn.setIcon(QIcon(QPixmap(":/Icons/media-playback-pause.png")))
            if not self.isPlaying():
                self.genInfo()
                
        else:
            self.mediaObject.pause()
            self.playBttn.setIcon(QIcon(QPixmap(":/Icons/media-playback-start.png")))
            self.statLbl.setText("Paused")
            
        self.playAction.setChecked(checked)
        
    @pyqtSignature("")
    def on_stopBttn_pressed(self):
        """
        To stop current track.
        """
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
        Slot documentation goes here.
        """
        self.volLbl.setText("%s" % value)
        self.audioOutput.setVolume(value/100.0)
    
    @pyqtSignature("")
    def on_actionEdit_triggered(self):
        """
       Brings up the settings Dialog
        """
        # TODO: not finished yet
        dialog = settingDlg(self)
        
        if dialog.exec_():
            self.mediaDir = dialog.dirVal()
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
        Closing Down
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
        # This shouldn't be called all the time as
        # it resets progSldr on a  pause/unpause
        self.setProgSldr() 
        if old == 2 and new == 3:            
            self.genInfo()
            
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
        # Case sensitive
        srch_txt = self.srchplyEdit.text()
        for x in range(self.playlistTree.rowCount()):
            for y in range(self.playlistTree.columnCount()):
                if srch_txt in self.playlistTree.item(x, y).text():
                    print "spam!: ", self.playlistTree.item(x, y).text()
    
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
    
    @pyqtSignature("int")
    def on_tabWidget_2_currentChanged(self, index):
        """
        When the wikiview becomes visible chances are
        it hasn't been viewed yet and needs to load
        """
        # TODO: not finished yet
        if index == 2:
            self.setWiki()

    def play_type(self, checked):
        if checked:
            self.statPlyTypBttn.setText("R")
            self.playRandom = True
        else:
            self.statPlyTypBttn.setText("N")
            self.playRandom = False
        
    def add2playlist(self, fileName, info):
        """
        Called when adding tracks tot he playlist either locally
        or from the database. Does not pull metadata from 
        the database and is passed into the function directly
        """
        
        track = "%02.u" % info[0]
        trackItem = QTableWidgetItem(track)
        trackItem.setFlags(trackItem.flags() ^ Qt.ItemIsEditable)
        
        titleItem = QTableWidgetItem(QString(info[1]))
        titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)

        artistItem = QTableWidgetItem(QString(info[2]))
        artistItem.setFlags(artistItem.flags() ^ Qt.ItemIsEditable)

        albumItem = QTableWidgetItem(QString(info[3]))
        albumItem.setFlags(albumItem.flags() ^ Qt.ItemIsEditable)
        
        yearItem = QTableWidgetItem(str(info[4]))
        yearItem.setFlags(yearItem.flags() ^ Qt.ItemIsEditable)

        genreItem = QTableWidgetItem(QString(info[5]))
        genreItem.setFlags(genreItem.flags() ^ Qt.ItemIsEditable)
        
        fileItem = QTableWidgetItem(QString(fileName))
        
        currentRow = self.playlistTree.rowCount()
        self.playlistTree.insertRow(currentRow)
        self.playlistTree.setItem(currentRow, 0, trackItem)
        self.playlistTree.setItem(currentRow, 1, titleItem)
        self.playlistTree.setItem(currentRow, 2, artistItem)
        self.playlistTree.setItem(currentRow, 3, albumItem)
        self.playlistTree.setItem(currentRow, 4, yearItem)
        self.playlistTree.setItem(currentRow, 5, genreItem)
        self.playlistTree.setItem(currentRow, 6, fileItem)
        
        # Figured out what the deleted section was supposed to do.
        # If the playlist was empty it would add2playlist tracks and enque 
        # the 1st track so playBttn would do something when 1st pressed.
        # It would also select the 1st row in the playlist. It did something else 
        # to do with appending the playlist but I've no idea. 

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
        Slot documentation goes here.
        """
        # TODO: not completed yet. See self.collection
        self.collection(False)


    def collection(self, rebuild):
        media = []
        
        if rebuild:
            # Here we change the PRIMARY KEY in the database to
            # ON CONFLICT REPLACE as we want to rebuild.
            print "Do something here"
        else:
            # Here we check that the PRIMARY KEY in the database is
            # ON CONFLICT IGNORE as we want to add new files.
            print "Do something here"
            
        if not self.mediaDir:
            self.on_actionEdit_triggered()         

        for root, dirname, filename in os.walk(str(self.mediaDir)):
            for x in filename:
                fileNow = os.path.join(root, x)                
                if fileNow.endswith(".ogg") or fileNow.endswith(".mp3") or fileNow.endswith(".flac"):
                    media.append(fileNow)
                    
        self.statProg.setValue(0)
        self.statProg.setToolTip("Scanning Media")
        
        medTotal = len(media)
        
        for track in range(medTotal):
            prog = int(100 * ( float(track) / float(medTotal ) ))
            track = media[track]
            tags = self.meta.extract(track)
            tags.insert(0, track)
            self.mediaDB.add_media(tags)
            self.statProg.setValue(prog)
        
        self.statProg.setToolTip("Finished")
        self.statProg.setValue(100)
        self.mediaDB.lenDB()
        self.collectTree.clear()
        self.setupDBtree()
        
    def setupDBtree(self):
        """
        The beginnings of viewing the media database in the QTreeView
        """
        artists = self.mediaDB.queryDB("artist") # This gives multiples of the same thing
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

#TODO: Thread me!
    def setWiki(self):
        """
        The wikipedia page to current artist playing
        """
        #TODO: thread me!!!! If internet is slow the ui locks up!
        if self.art[0] != self.old_art[0] and self.art[0]: # Not sure if 'and self.art' will do anything now
            print "Artist!"
            html = self.info.getInfo("info", str(self.art[0]))

            self.wikiView.setHtml(str(html))
            self.old_art[0] = self.art[0]
            
        elif self.art[1] != self.old_art[1] and self.art[1]:
            print "Album"
            result = self.info.getInfo("cover", self.art[0], self.art[1])
            
            cover = QPixmap()
            cover.loadFromData(result)
            bytes = QByteArray()
            buffer = QBuffer(bytes)
            buffer.open(QIODevice.WriteOnly)
            cover.save(buffer, "JPG")
            
            self.coverView.setPixmap(cover)
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
            
        elif event == 4:
            if self.isPlaying():
                self.on_playBttn_toggled(False)
            else:
                self.on_playBttn_toggled(True)
                
# TODO: these could be pushed into their own class
    def genTrack(self, mode, row=None):
        """
        As the playlist changes on sorting, the playlist (the immediately next/previous 
        tracks) has to be regenerated before the queing of the next track
        """
        column = 6 # So that it can be dynamic later on when columns can be moved
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
            self.setWiki()

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
        column = 6
        rows = self.playlistTree.rowCount() 
        fileList = []
        
        for row in range(rows):
            item = self.playlistTree.item(row, column).text()
            fileList.append(item)  
        
        return fileList    
