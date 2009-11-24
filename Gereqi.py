#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The main script to run the application
More things could be done in here but i've 
no idea what yet.
"""
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString
from ui.interface import MainWindow

VERSION = "master"  

def main():
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName(QString("Gereqi"))
    app.setApplicationVersion(QString(VERSION))
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
