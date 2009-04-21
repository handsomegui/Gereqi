# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QDesktopServices, QAction, QMenu, QSystemTrayIcon, qApp, QIcon, QPixmap
from PyQt4.QtCore import pyqtSignature, QDir, QString, Qt, SIGNAL, QTime, SLOT, QUrl
from PyQt4.phonon import Phonon
from settings import Dialog
from pysqlite2 import dbapi2 as sqlite
import os

from Ui_amaroq import Ui_MainWindow
import resource_rc

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Initialistion of key items
        """
        self.formats = [".ogg", ".mp3"]
        self.dbase = "%s.amaroqdb" % QDir.homePath()
        try:
            self.dbase = sqlite.connect(self.dbase)
            self.cursor = self.dbase.cursor()
        except:
            print "Probably not made database yet"
        
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        self.metaInformationResolver = Phonon.MediaObject(self)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        self.mediaObject.setTickInterval(1000)
        self.sources = []
        self.audioOutput.setVolume(1)
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()
        self.viewable = True
        self.url = "about:blank"
        self.old_url = self.url
        
        headers = [self.tr("Track"), self.tr("Title"), self.tr("Artist"), self.tr("Album"), self.tr("Year")]
        for val in range(5):
            self.playlistTree.insertColumn(val)
        self.playlistTree.setHorizontalHeaderLabels(headers)        

        self.connect(self.metaInformationResolver, SIGNAL('stateChanged(Phonon::State, Phonon::State)'),self.metaStateChanged)
        self.connect(self.mediaObject, SIGNAL('tick(qint64)'), self.tick)
        self.connect(self.mediaObject, SIGNAL('aboutToFinish()'),self.aboutToFinish)
        self.connect(self.mediaObject, SIGNAL('finished()'),self.finished)
        self.connect(self.mediaObject, SIGNAL('stateChanged(Phonon::State, Phonon::State)'),self.stateChanged)
    
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
        if row > 0:
            self.playlistTree.setCurrentCell(row, 1)
            self.mediaObject.stop()
            self.mediaObject.setCurrentSource(self.sources[row])
            self.mediaObject.play()
    
    @pyqtSignature("bool")
    def on_playBttn_toggled(self, checked):
        """
        Slot documentation goes here.
        """
        if checked:
            self.mediaObject.play()
        else:
            self.mediaObject.pause()
        
    @pyqtSignature("")
    def on_stopBttn_pressed(self):
        """
        To stop current track.
        """
        self.mediaObject.stop()
        self.playBttn.setChecked(False)
        self.progSldr.setValue(0)
    
    @pyqtSignature("")
    def on_nxtBttn_pressed(self):
        """
        Go to next item in playlist(down)
        """
        row = self.playlistTree.currentRow() + 1
        if row < len(self.sources):
            self.playlistTree.setCurrentCell(row, 1)
            self.mediaObject.stop()
            self.mediaObject.setCurrentSource(self.sources[row])
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
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_actionRescan_Collection_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
#        dir = directory set in settings
#        if dir:
#            self.playlistTree.clearContents()
#            for root, dirname, filename in os.walk(str(dir)):
#                for x in filename:
#                    fileNow = os.path.join(root, x)
#                    for type in self.formats:
#                        if fileNow.endswith(type):
#                                    index = len(self.sources)
#                                    self.sources.append(Phonon.MediaSource(fileNow))   
    
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
        mfiles = QFileDialog.getOpenFileNames(self,
                self.tr("Select Music Files"),
                QDesktopServices.storageLocation(QDesktopServices.MusicLocation))            

        if mfiles:
            index = len(self.sources)
            for item in mfiles:   
               self.sources.append(Phonon.MediaSource(item))   
    
            self.metaInformationResolver.setCurrentSource(self.sources[index])

# Pretty much a copy and paste of Trolltech's example
    def metaStateChanged(self, newState, oldState):
            if newState == Phonon.ErrorState:
                QMessageBox.warning(self, self.tr("Error opening files"),
                        self.metaInformationResolver.errorString())
    
                while self.sources and self.sources.pop() != self.metaInformationResolver.currentSource():
                    pass
    
                return
    
            if newState != Phonon.StoppedState and newState != Phonon.PausedState:
                return
    
            if self.metaInformationResolver.currentSource().type() == Phonon.MediaSource.Invalid:
                return
    
            metaData = self.metaInformationResolver.metaData()
            
            # No worky
            track = metaData.get(QString('TRACKNUMBER'), [QString()])[0]
            trackItem = QTableWidgetItem(track)
            trackItem.setFlags(trackItem.flags() ^ Qt.ItemIsEditable)
    
            title = metaData.get(QString('TITLE'), [QString()])[0]
            if title.isEmpty():
                title = self.metaInformationResolver.currentSource().fileName()
            
            titleItem = QTableWidgetItem(title)
            titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
    
            artist = metaData.get(QString('ARTIST'), [QString()])[0]
            artistItem = QTableWidgetItem(artist)
            artistItem.setFlags(artistItem.flags() ^ Qt.ItemIsEditable)
    
            album = metaData.get(QString('ALBUM'), [QString()])[0]
            albumItem = QTableWidgetItem(album)
            albumItem.setFlags(albumItem.flags() ^ Qt.ItemIsEditable)
            
            # No worky
            year = metaData.get(QString('DATE'), [QString()])[0]
            yearItem = QTableWidgetItem(year)
            yearItem.setFlags(yearItem.flags() ^ Qt.ItemIsEditable)
    
            currentRow = self.playlistTree.rowCount()
            self.playlistTree.insertRow(currentRow)
            self.playlistTree.setItem(currentRow, 0, trackItem)
            self.playlistTree.setItem(currentRow, 1, titleItem)
            self.playlistTree.setItem(currentRow, 2, artistItem)
            self.playlistTree.setItem(currentRow, 3, albumItem)
            self.playlistTree.setItem(currentRow, 4, yearItem)
    
            if not self.playlistTree.selectedItems():
                self.playlistTree.selectRow(0)
                self.mediaObject.setCurrentSource(self.metaInformationResolver.currentSource())
    
            source = self.metaInformationResolver.currentSource()
            index = self.sources.index(self.metaInformationResolver.currentSource()) + 1
    
            if len(self.sources) > index:
                self.metaInformationResolver.setCurrentSource(self.sources[index])
            else:
                self.playlistTree.resizeColumnsToContents()
                if self.playlistTree.columnWidth(0) > 300:
                    self.playlistTree.setColumnWidth(0, 300)
    
    @pyqtSignature("int, int")
    def on_playlistTree_cellDoubleClicked(self, row, column):
        """
        When item doubleclicked. Play it.
        """
        self.mediaObject.stop()
        self.mediaObject.setCurrentSource(self.sources[row])
        self.mediaObject.play()
        self.playBttn.setChecked(True) 
        
    def tick(self, time):
        """
        Every second update time labels and progres slider
        """
        displayTime = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.progLbl.setText(displayTime.toString('mm:ss'))
        self.progSldr.setValue(time)
    
    @pyqtSignature("int, int")
    def on_playlistTree_cellPressed(self, row, column):
        """
        Selects track
        """
#        if Phonon.StoppedState:
#            self.mediaObject.setCurrentSource(self.sources[row])
#        else:
#            print "playing"
    
    @pyqtSignature("int")
    def on_progSldr_sliderMoved(self, position):
        """
        When the progress is moved by user input curent track seeks correspondingly
        """
        self.mediaObject.seek(position)
        
    def aboutToFinish(self):
        # Needs to select next track in playlist
        index = self.sources.index(self.mediaObject.currentSource()) + 1
        if len(self.sources) > index:
            self.mediaObject.enqueue(self.sources[index])
            
    def setProgSldr(self):
        length = self.mediaObject.totalTime()
        self.progSldr.setRange(0, length)
            
    def stateChanged(self):
        self.setProgSldr()
        row = self.playlistTree.currentRow()
        
        # May want to only do this if self.wikiView is visible
        if row:
            artist = self.playlistTree.item(row, 2).text()
            self.url = QUrl("http://www.wikipedia.com/wiki/%s" % artist)
            if self.url != self.old_url:
                self.wikiView.setUrl(self.url)
                self.old_url = self.url
        
    def finished(self):
        self.progSldr.setValue(0)
        self.progLbl.setText("00:00")
        
    def createActions(self):
        self.quitAction = QAction(self.tr("&Quit"), self)
        self.playAction = QAction(self.tr("&Play"), self)
        self.viewAction = QAction(self.tr("&Restore"), self)
        self.connect(self.quitAction, SIGNAL("triggered()"), qApp, SLOT("quit()"))
        self.connect(self.playAction, SIGNAL("triggered()"), self.mediaObject.play)
        self.connect(self.viewAction, SIGNAL("triggered()"), self.minimiseTray)
        

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.playAction)
        self.trayIconMenu.addAction(self.viewAction)
        self.trayIconMenu.addAction(self.quitAction)
        
        # No. This icon isn't final. Just filler.
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Icons/drawing.png"), QIcon.Normal, QIcon.Off)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(icon)
        
    def minimiseTray(self):
        if self.viewable:
            self.hide()
            self.viewable = False
        else:
            self.show()
            self.viewable = True
    
    @pyqtSignature("")
    def on_actionMinimise_to_Tray_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.minimiseTray()
    
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
