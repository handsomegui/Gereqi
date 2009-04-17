# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt4.QtCore import pyqtSignature, QDir, QString, Qt, SIGNAL, QTime
from PyQt4.phonon import Phonon
from settings import Dialog
from pysqlite2 import dbapi2 as sqlite
import os

from Ui_amaroq import Ui_MainWindow

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
        
        headers = [self.tr("Track"), self.tr("Title"), self.tr("Artist"), self.tr("Album"), self.tr("Year")]
        for val in range(5):
            self.playlistTree.insertColumn(val)
        self.playlistTree.setHorizontalHeaderLabels(headers)        

        self.connect(self.metaInformationResolver, SIGNAL('stateChanged(Phonon::State, Phonon::State)'),self.metaStateChanged)
        self.connect(self.mediaObject, SIGNAL('tick(qint64)'), self.tick)
    
    @pyqtSignature("")
    def on_clrBttn_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_srchEdt_editingFinished(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
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
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("bool")
    def on_playBttn_toggled(self, checked):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
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
        self.play.Bttn.setChecked(False)
    
    @pyqtSignature("")
    def on_nxtBttn_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("int")
    def on_volSldr_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("int")
    def on_progSldr_valueChanged(self, value):
        """
        To go back or forward in the current track.
        """
        # TODO: not implemented yet
    
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
    
    @pyqtSignature("")
    def on_actionExir_triggered(self):
        """
        Closing Down
        """
        exit()
    
    @pyqtSignature("")
    def on_actionPlay_Media_triggered(self):
        """
        Extract music files and shove into current playlist.
        """
        dir = QFileDialog.getExistingDirectory(\
            None,
            QString(),
            QDir.homePath(),
            QFileDialog.Options(QFileDialog.Option(0)))
            
        if dir:
            self.playlistTree.clearContents()
            for root, dirname, filename in os.walk(str(dir)):
                for x in filename:
                    fileNow = os.path.join(root, x)
                    for type in self.formats:
                        if fileNow.endswith(type):
                                    index = len(self.sources)
                                    self.sources.append(Phonon.MediaSource(fileNow))         
                 
            self.metaInformationResolver.setCurrentSource(self.sources[index])

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
            
            track = metaData.get(QString('TRACKNUMBER'), [QString()])[0]
            trackItem = QTableWidgetItem(track)
            trackItem.setFlags(trackItem.flags() ^ Qt.ItemIsEditable)
    
            title = metaData.get(QString('TITLE'), [QString()])[0]
            if title.isEmpty():
                title = self.metaInformationResolver.currentSource().fileName()
            
            print title
            titleItem = QTableWidgetItem(title)
            titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
    
            artist = metaData.get(QString('ARTIST'), [QString()])[0]
            artistItem = QTableWidgetItem(artist)
            artistItem.setFlags(artistItem.flags() ^ Qt.ItemIsEditable)
    
            album = metaData.get(QString('ALBUM'), [QString()])[0]
            albumItem = QTableWidgetItem(album)
            albumItem.setFlags(albumItem.flags() ^ Qt.ItemIsEditable)
    
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
        self.playBttn.setChecked(True) # Untested
        
    def tick(self, time):
        """
        Every second update time labels and progres slider
        """
        displayTime = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.progLbl.setText(displayTime.toString('mm:ss'))
    
    @pyqtSignature("int, int")
    def on_playlistTree_cellPressed(self, row, column):
        """
        Selects track
        """
        self.mediaObject.setCurrentSource(self.sources[row])
