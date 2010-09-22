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

from PyQt4.QtCore import *

from urllib import pathname2url
from time import time, sleep

import os
import pyinotify

from webinfo import Webinfo
from tagging import Tagging
from infopage import InfoPage
from collection import CollectionDb
from settings import Settings

build_lock = delete_lock = False


class Getinfo(QThread):
    """
    Retrieves the cover for an album
    from Amazon
    """
    got_info = pyqtSignal(QString)
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.ui_main = parent
        
    def set_values(self, **params):
        self.info = params
    def run(self):
        html = InfoPage(self.ui_main).gen_info(**self.info)
        self.got_info.emit(html)
        
        
class Getwiki(QThread):
    """
    Retrieves the wiki info for an artist
    """
    got_wiki = pyqtSignal(QString)
    
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
        
        self.got_wiki.emit(result)
        
        
class Builddb(QThread):
    """
    Gets files from a directory and build's a 
    media database from the filtered files
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(QString)
    
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.ui_main = parent
        self.media_db = CollectionDb("builder")
        
    def __file_compat(self, dirpath, fname):
        now = os.path.join(dirpath, fname)
        ender = os.path.splitext(now)[-1].strip(".")
        ender = ender.lower() 
        # We only want to get tags for certain file formats
        if ender in self.a_formats: 
            return now  
        
    def stop_now(self):
        self.exiting = True
        
    def set_values(self, dirs, formats, mode, tracks=None):
        """
        Required to put parameters into
        this thread from the outside
        """
        self.media_dir = dirs
        self.file_list = tracks
        self.mode = mode
        self.meta = Tagging(formats)  
        self.a_formats = formats
     
    def __track_list(self, dir, excl):
        """
        Generates a list of compatible files
        """
        tracks = []
        not_need = [now for now in excl 
                        if dir in now]
        sets_db = Settings()
        # Recursively search                
        if sets_db.get_collection_setting("recursive") == "True":
        # No point trying to speed this up. os.walk is a generator function
            for dirpath, dirnames, filenames in os.walk(dir):
                # The exclusion part
                #FIXME: although this means you exclude the dirpath you don't exclude it's subdirs
                if dirpath not in not_need:
                    for fname in filenames:
                        trk = self.__file_compat(dirpath, fname)
                        if trk is not None:
                            tracks.append(trk)
                            
        else:
            # Cannot use the loop for both as one is the above is a generator
            # and os.listdir is a list-returning function
            for fname in os.listdir(dir):
                trk = self.__file_compat(dir, fname)
                if trk is not None:
                    tracks.append(trk)
                         
        return tracks
        
    def run(self):
        self.ui_main.build_lock = True
        while self.ui_main.delete_lock == True:
            print("WAITING: creation")
            sleep(1)
            
        old_prog = 0
        
        if self.mode == "redo":
            self.media_db.drop_media()
            print("FROM SCRATCH")
        elif self.mode == "update":
            print("UPDATE")
            self.__check_db()
        
        if self.file_list is None:
            tracks = []
            for dir in self.media_dir[0]:
                tracks.extend(self.__track_list(dir, self.media_dir[1]))
        else:
            tracks = []
            for trk in self.file_list:
                tracks.append(unicode(trk))
            
        tracks_total = len(tracks)
        print("%06d tracks to scan" % tracks_total)
        self.exiting = False
        
        #TODO:maybe put in a check to not bother getting tags for
        # an existing file and skipping anyway
        strt = time()
        cnt = 0
        #TODO: performance tuning
        for trk in tracks:
            if self.exiting == False: # Can't tell if this is causing slowdown
                ratio = float(cnt ) /  float(tracks_total)
                prog = int(round(100 * ratio))
                if prog > old_prog:
                    old_prog = prog
                    self.progress.emit(prog)

                info = self.meta.extract(trk)
                if info is not None:
                    # prepends the fileName as the DB function expects
                    # a certain order to the args passed
                    info.insert(0, trk) 
                    info.append(int(round(time())))
                    
                    # The playcount and rating
                    info.append(0)
                    info.append(0)
                    self.media_db.add_media(info)
                    cnt += 1
            else:
                print("User terminated scan.")
                self.finished.emit(QString("cancelled"))
                self.ui_main.build_lock = False
                return
            
        print("%u of %u tracks scanned in: %0.1f seconds" % (cnt, tracks_total,
                                                             (time() - strt)))
        self.finished.emit(QString("complete"))
        self.ui_main.build_lock = False
        
        
class Watcher(QThread, pyinotify.ProcessEvent):
    """
    Watches a directory periodically for file changes
    """
    deletions = pyqtSignal(QStringList)
    creations = pyqtSignal(QStringList)
    
    def __init__(self, parent):
        QThread.__init__(self)
        pyinotify.ProcessEvent.__init__(self)       
        self.ui_main = parent
        self.start_time = time()
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
            if self.ui_main.delete_lock == False:
                self.deletions.emit(self.deleted)
                self.deleted.clear()
            else:
                print("WAITING: deletion list")
                
        if self.created.count() > 0:
            if self.ui_main.build_lock == False:
                self.creations.emit(self.created)
                self.created.clear()
            else:
                print("WAITING: creation list")
            
        self.start_time = time()
        
    def __gen_exc_list(self, dirs):
        if dirs is not None:
            return ["^%s" % dir for dir in dirs]
        
    def __track_list(self, dir):
        tracks = []
        if self.recur:
            for dirpath, dirnames, filenames in os.walk(dir):
                for fname in filenames:
                    trk = os.path.join(dirpath, fname)
                    tracks.append(trk)                            
        else:
            for fname in os.listdir(dir):
                trk = os.path.join(dirpath, fname)
                tracks.append(trk)
                
        return tracks
        
    def process_IN_CREATE(self, event):
        file_name = event.pathname
        if (file_name is not None) and (file_name not in self.created):
            # pyinotify will only create just a single instance of
            # creation, the directory, not it's contained files
            if os.path.isdir(file_name):
                tracks = self.__track_list(file_name)
                for trk in tracks:
                    self.created.append(trk)
            else:
                self.created.append(file_name)

    def process_IN_DELETE(self, event):
        file_name = event.pathname
        print file_name
        if file_name is not None:
            if file_name not in self.deleted:            
                self.deleted.append(file_name)

    def set_values(self, dirs, timer, recursive):
        self.directory = dirs
        self.timer = timer
        self.gogogo = True
        self.checkers = [False, False]
        self.recur = recursive
        
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
        exclusions = self.__gen_exc_list(self.directory[1])
        excl = pyinotify.ExcludeFilter(exclusions)
        wdd = wm.add_watch(self.directory[0], mask, rec=self.recur, 
                           auto_add=True, exclude_filter=excl)
        
        while self.gogogo != False:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()           
           
            if int(time() - self.start_time) > self.timer:
                self.__poller()


class DeleteFiles(QThread):
    deleted = pyqtSignal()
    
    def __init__(self, parent):
        self.ui_main = parent
        QThread.__init__(self)
        
    def set_values(self, deletions):
        self.file_list = deletions
        
    def run(self):        
        self.ui_main.delete_lock = True
        while self.ui_main.build_lock == True:
            print("WAITING: deletion")
            sleep(1)     
        
        media_db = media_db = CollectionDb("deleter")
        for trk in self.file_list:
            media_db.delete_track(trk)
         
        # Signals to indicate that items based on
        # DB should probably update
        self.deleted.emit()
        self.ui_main.delete_lock = False       


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
            
            