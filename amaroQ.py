#!/usr/bin/env python
"""
The main script to run the application
More things could be done in here but i've 
no idea what yet.
"""
from PyQt4.QtGui import QApplication
from ui.amaroq import MainWindow

def main():
    import sys
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
