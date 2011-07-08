#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
The main script to run the application
More things could be done in here but i've 
no idea what yet.
"""
from PyQt4.QtGui import QApplication
from gereqi.interface import MainWindow
from gereqi.threads import GetCovers
import sys
__version__ = "0.5.0" 

class Main:
    
    def __init__(self):
        """
        dummy
        """
        cover_thread = GetCovers()
        cover_thread.start()
        app = QApplication(sys.argv)
    
        app.setApplicationName("Gereqi")
        app.setApplicationVersion(__version__)
        self.wnd = MainWindow(app)
        
        self.setups()
        self.wnd.show()
        sys.exit(app.exec_())
    
    def setups(self):
	try:
	        self.wnd.search_trktbl_edit.setPlaceholderText("Playlist Search")
        	self.wnd.search_collect_edit.setPlaceholderText("Enter search terms here")
    	except:
		pass
    
if __name__ == '__main__':
    Main()
