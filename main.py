#!/usr/bin/env python

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString
from src.interface import MainWindow
import sys

def main():
    """
    dummy
    """
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
