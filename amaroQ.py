#!/usr/bin/env python

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString
from ui.amaroq import MainWindow

VERSION = "0.1.3"

def main():
    import sys
    app =QApplication(sys.argv)
    app.setApplicationName(QString("Amaroq"))
    app.setApplicationVersion(QString(VERSION))
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
