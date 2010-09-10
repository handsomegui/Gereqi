# -*- coding: utf-8 -*-

"""
Module implementing Equaliser.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

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
    

