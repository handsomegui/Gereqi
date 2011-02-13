# -*- coding: utf-8 -*-

"""
Module implementing Equaliser.
"""

from PySide.QtGui import QDialog, QColor, QDesktopServices
from PySide.QtCore import pyqtSignature

from Ui_about import Ui_About

class About(QDialog, Ui_About):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.textBrowser.anchorClicked.connect(self.__linker)
        

    
    def __linker(self, url):
        desk = QDesktopServices()
        desk.openUrl(url)