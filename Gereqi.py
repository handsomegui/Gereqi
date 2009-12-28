#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The main script to run the application
More things could be done in here but i've 
no idea what yet.
"""
from PySide.QtGui import QApplication
from PySide.QtCore import QString
from ui.interface import MainWindow
import sys
__version__= "master"  

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
