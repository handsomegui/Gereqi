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

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature, QDir, QString

from gereqi.storage.Settings import Settings
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
        self.__mysql_avail()
        self.sets_db = Settings()
        self.__fileview_setup()         
        self.__interface_setup()
        
    def __mysql_avail(self):
        """
        If mysql support was built into QSql then allow
        the backend to be used
        """
        from PyQt4.QtSql import QSqlDatabase
        avails = QSqlDatabase.drivers()
        if "QMYSQL" in avails:
            self.database_type.addItem("MYSQL")
        else:
            print("Mysql option not available")
        
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
        if include is not None:
            inc = [QString(dir) for dir in include.split(",")]
        if exclude is not None:
            exc = [QString(dir) for dir in exclude.split(",")]
        
        self.dir_model.check_list = [inc, exc]                                        
        filters = QDir.AllDirs|QDir.Readable|QDir.NoDotAndDotDot
        self.dir_model.setFilter(filters)
        self.dir_model.setReadOnly(True)
        self.collection_view.setModel(self.dir_model) 
        self.collection_view.setColumnHidden(1, True)
        self.collection_view.setColumnHidden(2, True)
        self.collection_view.setColumnHidden(3, True)
        self.collection_view.expandToDepth(0)
        
    def __database_setup(self):
        db_type = self.sets_db.get_database_setting("type")
        if db_type == "MYSQL":
            index = self.database_type.findText("MYSQL")
            self.database_type.setCurrentIndex(index)
            self.mysql_host.setText(self.sets_db.get_database_setting("hostname"))
            self.mysql_user.setText(self.sets_db.get_database_setting("username"))
            self.mysql_password.setText(self.sets_db.get_database_setting("password"))
            self.mysql_dbname.setText(self.sets_db.get_database_setting("dbname"))
            self.mysql_port.setValue(int(self.sets_db.get_database_setting("port")))
            
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
        self.__database_setup()
        
        
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
        
        incl = [ str(dir.toUtf8()) for dir in self.dir_model.check_list[0] ]
        excl = [ str(dir.toUtf8()) for dir in self.dir_model.check_list[1] ]
        incl = ",".join(incl)
        excl = ",".join(excl)
        self.sets_db.add_collection_setting("include",incl)
        self.sets_db.add_collection_setting("exclude",excl)
            
    def __set_database(self):
        db_type = unicode(self.database_type.currentText())
        self.sets_db.add_database_setting("type", db_type) 
        
        if db_type == "MYSQL":
            self.sets_db.add_database_setting("hostname", str(self.mysql_host.text().toUtf8()) )
            self.sets_db.add_database_setting("username", str(self.mysql_user.text().toUtf8()) )
            self.sets_db.add_database_setting("password", str(self.mysql_password.text().toUtf8()) )
            self.sets_db.add_database_setting("dbname", str(self.mysql_dbname.text().toUtf8()) )
            self.sets_db.add_database_setting("port", str(self.mysql_port.value()) )
            
    def __apply_settings(self):
        """
        Apply all the settings to the db
        """      
        self.__set_collections()
        self.__set_database()
        self.__save_settings()
            
    @pyqtSignature("QAbstractButton*")
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
            
