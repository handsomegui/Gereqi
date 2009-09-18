# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, \
QDesktopServices, QAction, QMenu, QSystemTrayIcon, qApp, QIcon, QPixmap, QLabel, \
QProgressBar, QToolButton, QSpacerItem, QSizePolicy, QTreeWidgetItem
from PyQt4.QtCore import pyqtSignature, QDir, QString, Qt, SIGNAL, QTime, SLOT, QUrl, \
QSize,  QStringList
from PyQt4.phonon import Phonon
import os

from settings import settingDlg
from Ui_amaroq import Ui_MainWindow
import resource_rc
from database import media
from metadata import metaData
from wiki import Wiki

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    
    #FIXME: This is a mess. Fix
    def __init__(self, parent = None):
        """
        Initialistion of key items. Some may be pulled
        from other files as this file is getting messy
        """ 
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.mediaDB = media()
        self.mediaDir = None
        self.meta = metaData()
        self.setupDBtree()
        self.wikipedia = Wiki()
        
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        self.metaInformationResolver = Phonon.MediaObject(self)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        self.mediaObject.setTickInterval(1000)
        self.sources = []
        self.audioOutput.setVolume(1)
#        self.tabViewable = True
        self.url = "about:blank"
        self.old_url = self.url
        self.playing = False # Had to as using mediaObject.state is fucking shit and useless
        self.track_changing = False
        
        self.setupExtra()
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show() 
   
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

        headers = [self.tr("Track"), self.tr("Title"), self.tr("Artist"), self.tr("Album"), self.tr("Year"), self.tr("Genre"), self.tr("FileName")]
        
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
#        self.connect(self.metaInformationResolver, SIGNAL('stateChanged(Phonon::State, Phonon::State)'),self.metaStateChanged)
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
        # TODO: not ifinished
        print self.srchEdt.text()
    
    @pyqtSignature("QTreeWidgetItem*, int")
    def on_collectTree_itemDoubleClicked(self, item, column):
        """
        Slot documentation goes here.
        """
        # TODO: not completed yet
        album = item.text(column)
        
        try:
            artist= item.parent().text(0)
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
        row = self.playlistTree.currentRow() - 1
        if row >= 0:
            self.playlistTree.selectRow(row)
            self.mediaObject.stop()
            self.mediaObject.setCurrentSource(self.sources[row])
            if self.playing:
                self.mediaObject.play()

    # Because of the 2 signals that can trigger this, it's possible
    # this method is called twice when one or the other is called.
    @pyqtSignature("bool")
    def on_playBttn_toggled(self, checked):
        """
        Slot documentation goes here.
        """
        self.stopBttn.setEnabled(True)
        if checked:
            self.mediaObject.play()
            self.playBttn.setIcon(QIcon(QPixmap(":/Icons/media-playback-pause.png")))
        else:
            self.mediaObject.pause()
            self.playBttn.setIcon(QIcon(QPixmap(":/Icons/media-playback-start.png")))
            
        self.playing = checked    
        self.playAction.setChecked(checked)
        self.playBttn.setChecked(checked)

        
    @pyqtSignature("")
    def on_stopBttn_pressed(self):
        """
        To stop current track.
        """
        self.mediaObject.stop()
        self.playBttn.setChecked(False)
        self.progSldr.setValue(0)
        self.playing = False
        self.stopBttn.setEnabled(False)
    
    @pyqtSignature("")
    def on_nxtBttn_pressed(self):
        """
        Go to next item in playlist(down)
        """
        row = self.playlistTree.currentRow() + 1
        if row < len(self.sources):
            self.playlistTree.selectRow(row)
            self.mediaObject.stop()
            self.mediaObject.setCurrentSource(self.sources[row])
            if self.playing:
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
        Slot documentation goes here.
        """
        # TODO: not implemented yet
#        raise NotImplementedError
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
            index = len(self.sources)
            for item in mfiles:
                if item.endsWith(".ogg") or item.endsWith(".mp3") or item.endsWith(".flac"):
                    
                    info = self.meta.extract(item) # Added this so add2playlist can have data added from mediaDB
                    self.add2playlist(item, info)

    @pyqtSignature("int, int")
    def on_playlistTree_cellDoubleClicked(self, row, column):
        """
        When item is doubleclicked. Play its row.
        """
        print row, column
        self.mediaObject.stop()
        self.mediaObject.setCurrentSource(self.sources[row])
        self.mediaObject.play()
        self.playBttn.setChecked(True) 
        self.playAction.setChecked(True)
        self.playing = True
        
    def tick(self, time):
        """
        Every second update time labels and progres slider
        """
        t_now = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        if t_now == QTime(0, 0, 0):
            self.track_changing = True
            self.stateChanged(None, None) #FIXME: use proper states here
        self.progLbl.setText("%s | %s" % (t_now.toString('mm:ss'), self.t_length.toString('mm:ss')))
        self.progSldr.setValue(time)
    
    def aboutToFinish(self):
        # Needs to select next track in playlist
        index = self.sources.index(self.mediaObject.currentSource()) + 1
        if len(self.sources) > index:
            self.mediaObject.enqueue(self.sources[index])
            self.track_changing = True
            
    def setProgSldr(self):
        length = self.mediaObject.totalTime()
        self.progSldr.setRange(0, length)
        self.t_length = QTime(0, (length / 60000) % 60, (length / 1000) % 60)
            
#FIXME: this seems to be called 3 times on every track change
    def stateChanged(self, old, new):
        print "State Changed", old, new
        self.setProgSldr()
        
        # If there is any files in the playlist i.e. len(self.sources) > 0
        if self.sources:
            row = self.sources.index(self.mediaObject.currentSource())
        
            if self.track_changing:
                self.track_changing = False
                
            title = self.playlistTree.item(row, 1).text()
            artist = self.playlistTree.item(row, 2).text()
            
            if self.playing:
                message = "%s by %s" % (title, artist)
                self.trayIcon.showMessage(QString("Now Playing"), QString(message), QSystemTrayIcon.NoIcon, 3000)
                title = self.playlistTree.item(row, 1).text()
                artist = self.playlistTree.item(row, 2).text()
                album = self.playlistTree.item(row, 3).text()
                time =  self.t_length.toString('mm:ss')
                message = "Playing: %s by %s on %s (%s)" % (title, artist, album, time)
                self.statLbl.setText(message)
    
            self.playlistTree.selectRow(row) # Yeah. This isn't right
    
            self.url = "http://www.en.wikipedia.org/wiki/%s" % artist
            if row and self.wikiView.isVisible():
                self.setWiki()
        
    def finished(self):
        self.progSldr.setValue(0)
        self.progLbl.setText("00:00")
        self.playing = False
        
    def minimiseTray(self, state):
        if state:
            self.show()
        else:
            self.hide()
            
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
        self.sources = []
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

    def calc_playlist(self):
        """
        Bunch of arse.
        """
        time = 0
        media_obj = Phonon.MediaObject()
        for n in range(len(self.sources)):
            obj = media_obj.setCurrentSource(self.sources[n])
            t1 = obj.totalTime()
            print t1
            time += t1
            
        total_time = QTime(0, (time / 60000) % 60, (ltime / 1000) % 60)
        total_time = total_time.toString('mm:ss')
        print total_time
        
    def play_type(self, checked):
        if checked:
            self.statPlyTypBttn.setText("R")
            self.play_norm = False
        else:
            self.statPlyTypBttn.setText("N")
            self.play_norm = True
        
    def add2playlist(self, fileName, info):
        
        self.sources.append(Phonon.MediaSource(fileName))
        
        trackItem = QTableWidgetItem(str(info[0]))
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

#TODO: figure out the below
        # I honestly cannot remember what this commented section does
#        source = self.metaInformationResolver.currentSource() # This seems to be looking up something I don't think it is
#        if not self.playlistTree.selectedItems():
#            print "Spam"
#            self.playlistTree.selectRow(0)
#            self.mediaObject.setCurrentSource(source)
#
#
#        print source, self.sources[0]
#        val = self.sources.index(source)+ 1
#
#        if len(self.sources) > val:
#            self.metaInformationResolver.setCurrentSource(self.sources[val])
#        else:
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
        
        #TODO: at the start of new letter in alphabet create a header/separator
        for artist in artists:            
            artist = artist[0]
            albums = self.mediaDB.searching("album", "artist", artist)
            artist = QStringList(artist)
            artist = QTreeWidgetItem(artist)
            self.collectTree.addTopLevelItem(artist)
            
# There's a way of adding albums all in one command but it requires a list
# which I would still have to loop to create
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
        if self.url != self.old_url:
            html = self.wikipedia.fetch(str(self.url))
            self.wikiView.setHtml(str(html))
            self.old_url = self.url
