# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow, QFileDialog
from PyQt4.QtCore import pyqtSignature, QDir, QString
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
        
        headers = [self.tr("Track"), self.tr("Title"), self.tr("Artist"), self.tr("Album"), self.tr("Year")]
        for val in range(5):
            self.playlistTree.insertColumn(val)
        self.playlistTree.setHorizontalHeaderLabels(headers)
    
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
    
    @pyqtSignature("QTableWidgetItem*")
    def on_playlistTree_itemDoubleClicked(self, item):
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
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_stopBttn_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
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
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
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
        # TODO: not implemented yet
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
#                            print "%s\nExtract tags and create a new entry in self.playlistTree" % fileNow
                            self.metaInformationResolver.setCurrentSource(Phonon.MediaSource(fileNow))
                            metaData = self.metaInformationResolver.metaData()
                            title = metaData.get(QString('TITLE'), [QString()])[0]
                            
