# This file is part of Gereqi.
#
# Gereqi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gereqi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gereqi.  If not, see <http://www.gnu.org/licenses/>.

"""
Module implementing Configuration.
"""

from PyQt4.QtGui import QDialog,QAbstractButton
from PyQt4.QtCore import QDir, pyqtSignature

from storage.Settings import Settings
from Ui_configuration import Ui_settings_dialog
from myqdirmodel import MyQDirModel


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
        self.sets_db = Settings()
        self.__fileview_setup()         
        self.__interface_setup()
        
    def __refreshing(self, index):
        if self.collection_view.isExpanded(index):
            self.collection_view.collapse(index)
            self.collection_view.expand(index)
        
    def __fileview_setup(self):
        """
        Make the fileview the correct type
        """
        self.dir_model = MyQDirModel()        
        self.dir_model.needsRefresh.connect(self.__refreshing)
        
        # DO NOT DO 'inc=exc=[]' they all point to the same thing 
        inc = []
        exc = []
        include = self.sets_db.get_collection_setting("include")
        exclude = self.sets_db.get_collection_setting("exclude")
        
        # TODO: are these needed?
        if include is not None:
            inc = [dir for dir in include.split(",")]
        if exclude is not None:
            exc = [dir for dir in exclude.split(",")]
        
        self.dir_model.check_list = {'includes':inc,
                                     'excludes':exc}                                        
        filters = QDir.AllDirs|QDir.Readable|QDir.NoDotAndDotDot
        self.dir_model.setFilter(filters)
        self.dir_model.setReadOnly(True)
        self.collection_view.setModel(self.dir_model) 
        self.collection_view.setColumnHidden(1, True)
        self.collection_view.setColumnHidden(2, True)
        self.collection_view.setColumnHidden(3, True)
        self.collection_view.expandToDepth(0)
            
    def __interface_setup(self):
        # General
        func = lambda x : self.sets_db.get_interface_setting(x) == "True"
        coversize = self.sets_db.get_interface_setting("coversize")
        self.tray_icon.setChecked(func("trayicon"))
        self.remember_current.setChecked(func("remember"))
        self.context_browser_change.setChecked(func("context-change"))
        if coversize is not None:
            self.cover_size.setValue(int(coversize))
        
        #  Collection
        func = lambda x : self.sets_db.get_collection_setting(x) == "True"
        self.scan_recursively.setChecked(func("recursive"))
        self.watch_folders.setChecked(func("watch"))
        
        
    def __save_settings(self):
        true_false = lambda x : x == True and "True" or "False"
        # Interface
        cover_size = self.cover_size.value()
        show_tray = true_false(self.tray_icon.isChecked())
        remember = true_false(self.remember_current.isChecked())
        context = true_false(self.context_browser_change.isChecked())
        self.sets_db.add_interface_setting("trayicon", show_tray)
        self.sets_db.add_interface_setting("coversize", cover_size)
        self.sets_db.add_interface_setting("remember", remember)
        self.sets_db.add_interface_setting("context-change", context)

        # Collection
        recursive_dirs = true_false(self.scan_recursively.isChecked())
        watch_dirs = true_false(self.watch_folders.isChecked())
        
        self.sets_db.add_collection_setting("watch", watch_dirs)
        self.sets_db.add_collection_setting("recursive", recursive_dirs)
        
    def __set_collections(self):        
        incl = ','.join(self.dir_model.check_list['includes'])
        excl = ','.join(self.dir_model.check_list['excludes'])
        self.sets_db.add_collection_setting("include",incl)
        self.sets_db.add_collection_setting("exclude",excl)
            
    def __apply_settings(self):
        """
        Apply all the settings to the db
        """      
        self.__set_collections()
        self.__save_settings()
            
    @pyqtSignature("QAbstractButton")
    def on_buttonBox_clicked(self, button):
        """
        Slot documentation goes here.
        """
        if button.text() == "Apply":
            self.__apply_settings()
    
    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.__apply_settings()
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
        elif val == "MYSQL":
            self.mysql_config.setEnabled(True)
            
    @pyqtSignature("bool")
    def on_scan_recursively_toggled(self, check):
        """
        sets the myqdirmodel in a certain mode
        """
        self.dir_model.recursive = check
            
