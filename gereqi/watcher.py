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
A lot of this was taken from a tutorial at
http://trac.dbzteam.org/pyinotify/wiki/Tutorial
"""

from PyQt4.QtCore import QThread

import pyinotify

wm = pyinotify.WatchManager()
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE
        
class Watcher(QThread, pyinotify.ProcessEvent):
    def __init__(self):
        QThread.__init__(self)
        pyinotify.ProcessEvent.__init__(self)
    
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname

    def set_values(self, directory):
        self.directory = directory
        
    def run(self):
        notifier = pyinotify.Notifier(wm, self,  timeout=5)
        wdd = wm.add_watch(self.directory, mask, rec=True)
        notifier.loop()
