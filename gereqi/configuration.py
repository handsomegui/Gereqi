# -*- coding: utf-8 -*-

"""
Module implementing Configuration.
"""

from PyQt4.QtGui import QDialog, QDirModel
from PyQt4.QtCore import pyqtSignature, QDir, Qt, QAbstractItemModel

from Ui_configuration import Ui_settings_dialog

class MyQDirModel(QDirModel):
    checked = []
    unchecked = []
        
    def data(self, index, role = Qt.DisplayRole):
        if index.isValid() and (index.column() == 0) and (role == Qt.CheckStateRole):
            dir_now = self.filePath(index)
            par_dir = dir_now.split("/")[:-1].join("/")
            # the item is checked only if we have stored its path
            if dir_now in MyQDirModel.unchecked:
                return Qt.Unchecked
            elif par_dir in MyQDirModel.unchecked:
                return Qt.Unchecked
                
            else:
                if dir_now in MyQDirModel.checked:
                    return Qt.Checked
                elif par_dir in MyQDirModel.checked:
                    MyQDirModel.checked.append(dir_now)
                    return Qt.Checked
                else:
                    return Qt.Unchecked
                
        return QDirModel.data(self, index, role)        
        
    def flags(self, index):
        if index.column() == 0: # make the first column checkable
           return QDirModel.flags(self, index) | Qt.ItemIsUserCheckable
        else:
            return QDirModel.flags(self, index)            
        
    def setData(self, index, value, role = Qt.EditRole):
        if index.isValid() and (index.column() == 0) and role == Qt.CheckStateRole:
            # store checked paths, remove unchecked paths
            if (value == Qt.Checked):
                MyQDirModel.checked.append(self.filePath(index))
                try:
                    MyQDirModel.unchecked.remove(self.filePath(index))
                except ValueError:
                    # Doesn't exist yet
                    return True
                return True
            else:
                MyQDirModel.checked.remove(self.filePath(index))
                MyQDirModel.unchecked.append(self.filePath(index))
                return True
                
        else:
            return QDirModel.setData(self, index, value, role);
    

class Configuration(QDialog, Ui_settings_dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.__fileview_setup()
        
    def __fileview_setup(self):
        """
        Make the fileview the correct type
        """
        self.dir_model = MyQDirModel()
        filters = QDir.AllDirs|QDir.Readable|QDir.NoDotAndDotDot
        self.dir_model.setFilter(filters)
        self.dir_model.setReadOnly(True)
        self.collection_view.setModel(self.dir_model) 
        self.collection_view.setColumnHidden(1, True)
        self.collection_view.setColumnHidden(2, True)
        self.collection_view.setColumnHidden(3, True)
        self.collection_view.expandToDepth(0)
    
    @pyqtSignature("QAbstractButton*")
    def on_buttonBox_clicked(self, button):
        """
        Slot documentation goes here.
        """
        if button.text() == "Apply":
            print "APPLY"
    
    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print "ACCEPT"
        QDialog.accept(self)
    
    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print "REJECTED"
        QDialog.reject(self)
