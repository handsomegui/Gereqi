#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The main script to run the application
More things could be done in here but i've 
no idea what yet.
"""
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString
from ui.amaroq import MainWindow
import gobject

VERSION = "pygst"  

def main():
    import sys
    gobject.threads_init()
    app = QApplication(sys.argv)
    app.setApplicationName(QString("Amaroq"))
    app.setApplicationVersion(QString(VERSION))
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
