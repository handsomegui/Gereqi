#!/usr/bin/env  python

import pyudev as udev
import pyudev.pyqt4 as qudev
from PySide.QtCore import QThread


class Tester(QThread):
    def __init__(self):
        QThread.__init__(self)
      
    def eventer(self, spam):
        print spam
    
    def run(self):
        context = udev.Context()
        monitor = udev.Monitor.from_netlink(context)
        observer = qudev.QUDevMonitorObserver(monitor)
        #monitor.filter_by(subsystem='input')
        observer.deviceAdded.connect(self.eventer)
        monitor.start()
        print "AHH"