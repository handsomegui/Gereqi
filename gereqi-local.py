#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


"""
The main script to run the application
More things could be done in here but i've 
no idea what yet.
"""
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString
from gereqi.interface import MainWindow
import sys
__version__= "0.3.9"  

def main():
    """
    dummy
    """
    app = QApplication(sys.argv)
    app.setApplicationName(QString("Gereqi"))
    app.setApplicationVersion(QString(__version__))
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
