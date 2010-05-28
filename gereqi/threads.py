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
This file contains all the necessary threads for the app
to make it easier to manage
"""

from PyQt4.QtCore import QThread, QString, SIGNAL, Qt
from PyQt4.QtGui import QImage, QPixmap
import os
import time

from webinfo import Webinfo
from database import Media
from tagging import Tagging


class Getcover(QThread):
    """
    Retrives the cover for an album
    from Amazon
    """
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        
    def set_values(self, art, alb, loc=None):
        self.artist = art
        self.album = alb
        self.locale = loc
      
    def run(self):
        info = Webinfo()
        result = info.get_info("cover", self.artist, self.album)
        img = QImage()
        if result is not None:
            img.loadFromData(result, "JPG")
        self.emit(SIGNAL("got-image ( QImage )"), img) 
        self.exit()
        
        
class Getwiki(QThread):
    """
    Retrieves the wiki info for an artist
    """
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    
    def set_values(self, art):
        self.artist = art
        
    def run(self):
        info = Webinfo()
        result = info.get_info("info", self.artist)
        if result is not None:
            result = QString(result)
        else:
            result = QString("None")
        self.emit(SIGNAL("got-wiki ( QString )"), result)
        self.exit()
        
        
class Builddb(QThread):
    """
    Gets files from a directory and build's a 
    media database from the filtered files
    """
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        
    def stop_now(self):
        self.exiting = True
        
    def set_values(self, directory, formats, tracks=None):
        """
        Required to put parameters into
        this thread from the outside
        """
        self.media_dir = directory
        self.a_formats = formats
        self.file_list = tracks
     
    def __track_list(self):
        """
        Generates a list of compatible files
        """
        tracks = []
        # No point trying to speed this up. os.walk is a generator function
        for root, dirname, filenames in os.walk(str(self.media_dir)):
            for name in filenames:
                now = os.path.join(root, name)
                try:
                    file_now = now.decode("utf-8")
                except UnicodeDecodeError:
                    #TODO: filename fixer
                    print("WARNING!: Funny encoding for filename. Ignoring", repr(now))
                    continue
                ender = os.path.splitext(now)[-1].strip(".")
                ender = ender.lower()
                # We only want to get tags for certain file formats
                if ender in self.a_formats:
                    # No point doing DB interaction per item. We need to
                    # Need to know how many tracks for progress bar
                    tracks.append(file_now)
        return tracks
        
    def run(self):
        old_prog = 0    
        meta = Tagging(self.a_formats)
        media_db = Media()
        
        if self.file_list is None:
            tracks = self.__track_list()
        else:
            tracks = self.file_list
            
        tracks_total = len(tracks)
        self.exiting = False
        
        #TODO:maybe put in a check to not bother getting tags for
        # an existing file and skipping anyway
        strt = time.time()
        cnt = 0
        #TODO: performance tuning
        for trk in tracks:
            if not self.exiting: # Can't tell if this is causing slowdown
                ratio = float(cnt ) /  float(tracks_total)
                prog = int(round(100 * ratio))
                if prog > old_prog:
                    old_prog = prog
                    self.emit(SIGNAL("progress ( int )"), prog)
                
                info = meta.extract(trk.encode("utf-8"))
                if info is not None:
                    tags = info[0:3]
                    del info
                    # prepends the fileName as the DB function expects
                    # a certain order to the args passed
                    tags.insert(0, trk) 
                    tags.append(int(round(time.time())))
                    
                    # The playcount and rating
                    tags.append(0)
                    tags.append(0)
                    media_db.add_media(tags)
                    cnt += 1
            else:
                print("User terminated scan.")
                self.emit(SIGNAL("finished( QString )"), QString("cancelled"))
                self.exit()
                return
            
        print("%u of %u tracks scanned in: %0.1f seconds" % (cnt, tracks_total,  (time.time() - strt)))
        self.emit(SIGNAL("finished ( QString )"), QString("complete"))
        self.exit()

class Finishers:
    """
    Things to do when the threads finish
    """
    def __init__(self, parent):
        """
        parent being MainWindow in interface.py
        """
        self.ui_main = parent

    def db_build(self, status):
        """
        Things to perform when the media library
        has been built/cancelled
        """
        self.ui_main.stat_bttn.setEnabled(False)
        if status == "cancelled":
            self.ui_main.stat_prog.setToolTip("Cancelled")
        else:
            self.ui_main.stat_prog.setToolTip("Finished")
        self.ui_main.stat_prog.setValue(100)
        self.ui_main.wdgt_manip.setup_db_tree()
        self.ui_main.search_collect_edit.clear()
        
    def set_cover(self, img):
        """
        Takes the img and displays in info tab
        """
        if img.isNull() is True:
            self.ui_main.cover_view.setPixmap(QPixmap(":/Icons/music.png"))
        else:
            cover = QPixmap()
            cover = cover.fromImage(img, Qt.OrderedDither)
            cover = cover.scaledToWidth(200, Qt.SmoothTransformation)
            self.ui_main.cover_view.setPixmap(cover)        
        
    def set_wiki(self, html):
        """
        The printable wikipedia page (if found) is
        put into the wikipedia tab
        """
        if html != "None":
            self.ui_main.horizontal_tabs.setTabEnabled(2, True)
            self.ui_main.wiki_view.setHtml(html)
        else:
            self.ui_main.horizontal_tabs.setTabEnabled(2, False)
            
