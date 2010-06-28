#Copyright 2009 Jonathan.W.Noble <jonnobleuk@gmail.com>


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

from PyQt4.QtCore import *
from PyQt4.QtSql import *
import os

class CollectionDb:
    def __init__(self, mode="SQLITE", args=None):
        """
        Experimental. As sqlite and mysql are barely different trying to
        account for the differences
        """
        self.db_type = mode
        if mode == "SQLITE":
            
            app_dir = "%s/.gereqi/" % os.getenv("HOME")
            db_loc = "%smedia.db" % app_dir
            if QDir(app_dir).exists is False:
                QDir().mkdir(app_dir)
                
            self.media_db = QSqlDatabase.addDatabase("QSQLITE");
            self.media_db.setDatabaseName(db_loc)
        
        elif mode == "MYSQL":
            self.media_db = QSqlDatabase.addDatabase("QMYSQL");
            self.media_db.setHostName(args["hostname"])
            self.media_db.setDatabaseName(args["dbname"])
            self.media_db.setUserName(args["username"])
            self.media_db.setPassword(args["password"])
            ok = self.media_db.open()
            
            if ok is True:
                print "MYSQL OK"
            else:
                print "MYSQL ERROR"
                return
                
            self.query = QSqlQuery(self.media_db)
            
        
#        self.__setup_tables()
