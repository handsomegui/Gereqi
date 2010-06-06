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

from PyQt4.QtCore import QThread, QString, SIGNAL, Qt, QStringList
from PyQt4.QtGui import QImage, QPixmap
import os
import time
import pyinotify

from webinfo import Webinfo
from database import Media
from tagging import Tagging

build_lock = delete_lock = False

def cleanup_encodings(before):
    try:
        return before.decode("utf-8")
    except UnicodeDecodeError:
    #TODO: filename fixer
        print("WARNING!: Funny encoding for filename. Ignoring - ", repr(before))



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
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.ui_main = parent
        
    def stop_now(self):
        self.exiting = True
        
    def set_values(self, dirs, formats, tracks=None):
        """
        Required to put parameters into
        this thread from the outside
        """
        self.media_dir = dirs[0]
        self.a_formats = formats
        self.file_list = tracks
     
    def __track_list(self, dir):
        """
        Generates a list of compatible files
        """
        tracks = []
        # No point trying to speed this up. os.walk is a generator function
        for root, dirname, filenames in os.walk(dir):
            for name in filenames:
                now = os.path.join(root, name)
                file_now = cleanup_encodings(now)
                if file_now is None:
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
        self.ui_main.build_lock = True
        while self.ui_main.delete_lock is True:
            print("WAITING: creation")
            time.sleep(1)
            
        old_prog = 0    
        meta = Tagging(self.a_formats)
        media_db = Media()
        
        if self.file_list is None:
            tracks = []
            for dir in self.media_dir:
                tracks.extend(self.__track_list(dir))
        else:
            tracks = []
            for trk in self.file_list:
                tracks.append(unicode(trk))
            
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
                    # prepends the fileName as the DB function expects
                    # a certain order to the args passed
                    info.insert(0, trk) 
                    info.append(int(round(time.time())))
                    
                    # The playcount and rating
                    info.append(0)
                    info.append(0)
                    media_db.add_media(info)
                    cnt += 1
            else:
                print("User terminated scan.")
                self.emit(SIGNAL("finished( QString )"), QString("cancelled"))
                self.ui_main.build_lock = False
                self.exit()
                return
            
        print("%u of %u tracks scanned in: %0.1f seconds" % (cnt, tracks_total,  (time.time() - strt)))
        self.emit(SIGNAL("finished ( QString )"), QString("complete"))
        self.ui_main.build_lock = False
        self.exit()
        
        
class Watcher(QThread, pyinotify.ProcessEvent):
    """
    Watches a directory periodically for file changes
    """
    def __init__(self, parent):
        QThread.__init__(self)
        pyinotify.ProcessEvent.__init__(self)       
        self.ui_main = parent
        self.start_time = time.time()
        self.created = QStringList()
        self.deleted = QStringList()
        
    def __poller(self):
        """
        At every time interval, as specified by self.timer,
        if the deleted/created lists are non-empty and nothing else
        is happening (i.i. some other func/thread is already working on
        something sent previously from this func) the list SIGNALd to 
        be handled such as deleting/adding tracks from/to the DB.
        """
        if self.deleted.count() > 0:
            if self.ui_main.delete_lock is False:
                self.emit(SIGNAL("deletions ( QStringList )"), self.deleted)            
                self.deleted.clear()
            else:
                print("WAITING: deletion list")
                
        if self.created.count() > 0:
            if self.ui_main.build_lock is False:
                self.emit(SIGNAL("creations ( QStringList )"), self.created)
                self.created.clear()
            else:
                print("WAITING: creation list")
            
        self.start_time = time.time()
        
    def gen_exc_list(self, dirs):
        return 
    
    def process_IN_CREATE(self, event):
        file_name = cleanup_encodings(event.pathname)
        if file_name is not None:
            if file_name not in self.created:            
                self.created.append(file_name)

    def process_IN_DELETE(self, event):
        file_name = cleanup_encodings(event.pathname)
        if file_name is not None:
            if file_name not in self.deleted:            
                self.deleted.append(file_name)

    def set_values(self, dirs, timer):
        self.directory = dirs[0]
        self.timer = timer
        self.gogogo = True
        self.checkers = [False, False]
        
    def stopstop(self):
        """
        To stop the watcher. If it works it's
        just a crude bodge
        """
        self.gogogo = False               
        
    def run(self):
        self.setPriority(QThread.IdlePriority)
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE
        notifier = pyinotify.Notifier(wm, self,  read_freq=3, timeout=10)
        wdd = wm.add_watch(self.directory, mask, rec=True, auto_add=True)
        
        while self.gogogo is True:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
                
            if int(time.time() - self.start_time) > self.timer:
                self.__poller()         
        self.exit()


class DeleteFiles(QThread):
    def __init__(self, parent):
        self.ui_main = parent
        QThread.__init__(self)
        
    def set_values(self, deletions):
        self.file_list = deletions
        
    def run(self):        
        self.ui_main.delete_lock = True
        while self.ui_main.build_lock is True:
            print("WAITING: deletion")
            time.sleep(1)     
        
        media_db = Media()
        for trk in self.file_list:
            media_db.delete_track(unicode(trk))
            
        self.ui_main.wdgt_manip.setup_db_tree()  
        self.ui_main.delete_lock = False
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
            self.ui_main.stat_lbl.setText("Cancelled")
        else:
            self.ui_main.stat_lbl.setText("Finished")
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
            
