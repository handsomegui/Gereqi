# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, \
QDesktopServices, QAction, QMenu, QSystemTrayIcon, qApp, QIcon, QPixmap, QLabel, \
QProgressBar, QToolButton, QSpacerItem, QSizePolicy
from PyQt4.QtCore import pyqtSignature, QDir, QString, Qt, SIGNAL, QTime, SLOT, QUrl, QSize
from PyQt4.phonon import Phonon
import os

from settings import settingDlg
from Ui_amaroq import Ui_MainWindow
import resource_rc
from database import media
from metadata import metaData

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    
    #FIXME: This is a mess. Fix
    def __init__(self, parent = None):
        """
        Initialistion of key items
        """
        self.dbase = "%s.amaroqdb" % QDir.homePath()
        try:
            self.dbase = sqlite.connect(self.dbase)
            self.cursor = self.dbase.cursor()
        except:
            print "Probably not made database yet"
        
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.mediaDB = media()
        self.mediaDir = None
        self.meta = metaData()
        
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        self.metaInformationResolver = Phonon.MediaObject(self)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        self.mediaObject.setTickInterval(1000)
        self.sources = []
        self.audioOutput.setVolume(1)
        self.viewable = True
        self.url = "about:blank"
        self.old_url = self.url
        self.playing = False # Had to as using mediaObject.state is fucking shit and useless
        self.track_changing = False
        
        self.statLbl = QLabel("Finished")
        self.statProg = QProgressBar()
        self.statBttn = QToolButton()
        self.statPlyTypBttn = QToolButton()
        icon = QIcon(QPixmap(":/Icons/application-exit.png"))
        
        self.statProg.setRange(0, 100)
        self.statProg.setValue(100)
        self.statProg.setMaximumSize(QSize(100, 32))
        self.statBttn.setIcon(icon)
        self.statBttn.setAutoRaise(True)
        self.statPlyTypBttn.setText("N")
        self.statPlyTypBttn.setCheckable(True)
        self.statPlyTypBttn.setAutoRaise(True)

        self.statusBar.addPermanentWidget(self.statLbl)
        self.statusBar.addPermanentWidget(self.statProg)
        self.statusBar.addPermanentWidget(self.statBttn)
        self.statusBar.addPermanentWidget(self.statPlyTypBttn)

        headers = [self.tr("Track"), self.tr("Title"), self.tr("Artist"), self.tr("Album"), self.tr("Year"), self.tr("Genre")]
        for val in range(len(headers)):
            self.playlistTree.insertColumn(val)
        self.playlistTree.setHorizontalHeaderLabels(headers)
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()      
    
    def createActions(self):
        self.quitAction = QAction(self.tr("&Quit"), self)
        self.playAction = QAction(self.tr("&Play"), self)
        self.playAction.setCheckable(True)
        self.viewAction = QAction(self.tr("&Visible"), self)
        self.viewAction.setCheckable(True)
        self.viewAction.setChecked(True)
        
        self.connect(self.quitAction, SIGNAL("triggered()"), qApp, SLOT("quit()"))
        self.connect(self.playAction, SIGNAL("toggled(bool)"), self.on_playBttn_toggled)
        self.connect(self.viewAction, SIGNAL("toggled(bool)"), self.minimiseTray)
#        self.connect(self.metaInformationResolver, SIGNAL('stateChanged(Phonon::State, Phonon::State)'),self.metaStateChanged)
        self.connect(self.mediaObject, SIGNAL('tick(qint64)'), self.tick)
        self.connect(self.mediaObject, SIGNAL('aboutToFinish()'),self.aboutToFinish)
        self.connect(self.mediaObject, SIGNAL('finished()'),self.finished)
        self.connect(self.mediaObject, SIGNAL('stateChanged(Phonon::State, Phonon::State)'),self.stateChanged)
        self.connect(self.statPlyTypBttn, SIGNAL('toggled(bool)'), self.play_type)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.playAction)
        self.trayIconMenu.addAction(self.viewAction)
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
        # TODO: not implemented yet
        raise NotImplementedError
    
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
        Slot documentation goes here.
        """
        # TODO: not implemented yet
#        raise NotImplementedError
#        dir = directory set in settings
        if not self.mediaDir:
            self.on_actionEdit_triggered()
            
#        if dir:
#            self.playlistTree.clearContents()
        # I'm going to have to break this loop into in order to utilise the
        # progressbar. I need to know how many files there are to be processed
        media = []
        
        for root, dirname, filename in os.walk(str(self.mediaDir)):
            for x in filename:
                fileNow = os.path.join(root, x)                
                if fileNow.endswith(".ogg") or fileNow.endswith(".mp3") or fileNow.endswith(".flac"):
                    media.append(fileNow)
                    
        medTotal = len(media)
        
        # extract tags and push into database
        self.statLbl.setText("Scanning Media")
        for track in range(medTotal):
            prog = int(100 * ( float(track) / float(medTotal ) ))
            track = media[track]
            tags = self.meta.extract(track)            
            self.statProg.setValue(prog)
        
        self.statLbl.setText("Finished")
        self.statProg.setValue(100)
    
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
#            self.metaInformationResolver.setCurrentSource(self.sources[index])
#            print self.metaInformationResolver.currentSource()
            for item in mfiles:
                if item.endsWith(".ogg") or item.endsWith(".mp3") or item.endsWith(".flac"):
                    self.sources.append(Phonon.MediaSource(item))
#                    self.metaInformationResolver.setCurrentSource(self.sources[index])
                    self.add2playlist(item)

                
#            self.metaInformationResolver.setCurrentSource(self.sources[index])

    @pyqtSignature("int, int")
    def on_playlistTree_cellDoubleClicked(self, row, column):
        """
        When item is doubleclicked. Play its row.
        """
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
        self.progLbl.setText("%s | %s" % (t_now.toString('mm:ss'), self.t_length.toString('mm:ss')))
        self.progSldr.setValue(time)
    
#    @pyqtSignature("int")
#    def on_progSldr_sliderMoved(self, position):
#        """
#        When the progress is moved by user input curent track seeks correspondingly
#        """
#        self.mediaObject.seek(position)
        
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
            
    def stateChanged(self):
        self.setProgSldr()
        row = self.playlistTree.currentRow()
        
        if self.track_changing:
            row += 1
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
#            self.statusBar.showMessage(QString(message), 0) # Turns out it's not permanent

        self.playlistTree.selectRow(row)

        self.url = "http://www.wikipedia.com/wiki/%s" % artist
        if row and self.wikiView.isVisible():
            if self.url != self.old_url:
                self.wikiView.setUrl(QUrl(self.url))
                self.old_url = self.url
        
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
        Slot documentation goes here.
        """
        # TODO: not implemented yet
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
        
        if self.mediaObject.state() == 0:
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
        # TODO: not implemented yet
        #<div id="bodyContent">
        if index == 2:
#            if self.url != self.old_url:
            self.wikiView.setUrl(QUrl(self.url))

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
        
    def add2playlist(self, fileName):
        info = self.meta.extract(fileName)
        
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
        
        currentRow = self.playlistTree.rowCount()
        self.playlistTree.insertRow(currentRow)
        self.playlistTree.setItem(currentRow, 0, trackItem)
        self.playlistTree.setItem(currentRow, 1, titleItem)
        self.playlistTree.setItem(currentRow, 2, artistItem)
        self.playlistTree.setItem(currentRow, 3, albumItem)
        self.playlistTree.setItem(currentRow, 4, yearItem)
        self.playlistTree.setItem(currentRow, 5, genreItem)

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
    
    
    # A much cleaner solution. If when you seek the volume is momentarily
    # set to 100% so it can really standout. 
    @pyqtSignature("")
    def on_progSldr_sliderReleased(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        val = self.progSldr.value()
        self.mediaObject.seek(val)
