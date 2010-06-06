# -*- coding: utf-8 -*-

"""
Module implementing Configuration.
"""

from PyQt4.QtGui import QDialog, QDirModel
from PyQt4.QtCore import pyqtSignature, QDir, Qt, QAbstractItemModel, \
SIGNAL

from Ui_configuration import Ui_settings_dialog

class MyQDirModel(QDirModel):
    check_list = [[], []]
        
    def data(self, index, role = Qt.DisplayRole):
        if index.isValid() and (index.column() == 0) and (role == Qt.CheckStateRole):
            dir_now = self.filePath(index)
            par_dir = dir_now.split("/")[:-1].join("/")
            # the item is checked only if we have stored its path
            if dir_now in MyQDirModel.check_list[1]:
                return Qt.Unchecked
            elif par_dir in MyQDirModel.check_list[1]:
                return Qt.Unchecked
                
            else:
                checker = dir_now.split("/")
                for val in range(len(checker)):
                    thing = checker[:val+1].join("/")
                    if thing in MyQDirModel.check_list[0]:
                        return Qt.Checked    
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
            # FIXME: no need to append if it's par_dir is there
            if (value == Qt.Checked):
                print self.filePath(index)
                MyQDirModel.check_list[0].append(self.filePath(index))
                try:
                    MyQDirModel.check_list[1].remove(self.filePath(index))
                except ValueError:
                    # Doesn't exist yet
                    pass
                self.emit(SIGNAL("needsRefresh( QModelIndex )"), index)
                return True
                
            # Want to exclude dir
            else:
                dir_now = self.filePath(index)
                par_dir = dir_now.split("/")[:-1].join("/")                
                tmp_list = (list(MyQDirModel.check_list[0]), list(MyQDirModel.check_list[1]))
                
                for item in tmp_list[0]:
                    # removes if we've already checked it
                    if dir_now in item:
                        MyQDirModel.check_list[0].remove(item)            
                 
                # Only add to unchecked if anything above is checked
                checker = dir_now.split("/")
                for val in range(len(checker)):
                    thing = checker[:val+1].join("/")
                    if thing in MyQDirModel.check_list[0]:
                        MyQDirModel.check_list[1].append(dir_now)                             
                
                self.emit(SIGNAL("needsRefresh( QModelIndex )"), index)
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
        self.dir_model = MyQDirModel()        
        self.connect(self.dir_model, SIGNAL("needsRefresh( QModelIndex )"), self.__refreshing)
        if parent.media_dir is not None:
            MyQDirModel.check_list = list(parent.media_dir)
        self.__fileview_setup()
        
    def __refreshing(self, index):
        if self.collection_view.isExpanded(index):
            self.collection_view.collapse(index)
            self.collection_view.expand(index)
        
        
    def __fileview_setup(self):
        """
        Make the fileview the correct type
        """
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
        
    def dir_list(self):
        checked = [unicode(chk) for chk in MyQDirModel.check_list[0] ]
        unchecked = [unicode(chk) for chk in MyQDirModel.check_list[1] ]
        return checked, unchecked
