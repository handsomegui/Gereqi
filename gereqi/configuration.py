# -*- coding: utf-8 -*-

"""
Module implementing Configuration.
"""

from PyQt4.QtGui import QDialog, QDirModel
from PyQt4.QtCore import pyqtSignature, QDir, Qt, QAbstractItemModel, \
SIGNAL

from settings import Settings
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
                dir_now = self.filePath(index)
                # No point adding if it's root dir is already there
                checker = dir_now.split("/")
                there = False
                for val in range(len(checker)):
                    thing = checker[:val+1].join("/")
                    if thing in MyQDirModel.check_list[0]:
                        there = True
                        break
                        
                try:
                    tmp_list = []
                    for thing in MyQDirModel.check_list[1]:
                        if str(dir_now) in thing:
                            tmp_list.append(str(thing))
                    for thing in tmp_list:
                        MyQDirModel.check_list[1].remove(thing)   

                except ValueError:
                    # Doesn't exist yet
                    pass
                    
                if there is False:
                    MyQDirModel.check_list[0].append(str(self.filePath(index)))
                self.emit(SIGNAL("needsRefresh( QModelIndex )"), index)
                return True
                
            # Want to exclude dir
            else:
                dir_now = self.filePath(index)
                par_dir = dir_now.split("/")[:-1].join("/")                
                tmp_list = (list(MyQDirModel.check_list[0]), list(MyQDirModel.check_list[1]))
                
                for item in tmp_list[0]:
                    # removes if we've already checked it
                    if str(dir_now) in item:
                        MyQDirModel.check_list[0].remove(item)            
                 
                # Only add to unchecked if anything above is checked
                checker = dir_now.split("/")
                for val in range(len(checker)):
                    thing = checker[:val+1].join("/")
                    if thing in MyQDirModel.check_list[0]:
                        MyQDirModel.check_list[1].append(str(dir_now))
                
                self.emit(SIGNAL("needsRefresh( QModelIndex )"), index)
                return True
                
        else:
            return QDirModel.setData(self, index, value, role);
    

class Configuration(QDialog, Ui_settings_dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None, **args):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.dir_model = MyQDirModel()        
        self.connect(self.dir_model, SIGNAL("needsRefresh( QModelIndex )"), self.__refreshing)
        self.sets_db = Settings()
        self.__get_settings()

        self.__fileview_setup()
        
    def __get_settings(self):
        MyQDirModel.check_list = [self.sets_db.get_collection_setting("include"), 
                                                self.sets_db.get_collection_setting("exclude")]
        
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
        
    def __set_collections(self):
        self.sets_db.drop_collection()
        for incl in MyQDirModel.check_list [0]:
            self.sets_db.add_collection_setting("include", incl)
        for excl in MyQDirModel.check_list[1]:
            self.sets_db.add_collection_setting("exclude", excl)
            
    def __set_database(self):
        db_type = unicode(self.database_type.currentText())
        self.sets_db.drop_database()
        self.sets_db.add_database_setting("type", db_type)
        
        if db_type == "MYSQL":
            print("MYSQL selected")
            self.sets_db.add_database_setting("hostname", unicode(self.mysql_host.text()) )
            self.sets_db.add_database_setting("username", unicode(self.mysql_user.text()) )
            self.sets_db.add_database_setting("password", unicode(self.mysql_password.text()) )
            self.sets_db.add_database_setting("dbname", unicode(self.mysql_dbname.text()) )
            self.sets_db.add_database_setting("port", unicode(self.mysql_port.value()) )
            
        
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
        # TODO: create a dict of settings
        self.__set_collections()
        self.__set_database()
        QDialog.accept(self)
    
    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        QDialog.reject(self)
        

    
    @pyqtSignature("QString")
    def on_database_type_currentIndexChanged(self, val):
        """
        Prevent mysql info entry if sqlite dbtype is selected
        """
        if val == "SQLITE":
            self.mysql_config.setEnabled(False)
        else:
            self.mysql_config.setEnabled(True)
