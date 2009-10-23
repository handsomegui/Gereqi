#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains all the necessary threads for the app
to make it easier to manage
"""

from PyQt4.QtCore import QThread, QString, SIGNAL
from PyQt4.QtGui import QImage
import os
from time import time

from webinfo import Webinfo
from database import Media
from metadata import Metadata
from timing import Timing

class Getcover(QThread):
    """
    Retrives the cover for an album
    from Amazon
    """
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        
    def set_values(self, art, alb, loc=None):
        self.artist = art
        self.album = alb
        self.locale = loc
      
    def run(self):
        info = Webinfo()
        result = info.get_info("cover", self.locale, self.artist, self.album)
        if result:
            img = QImage()
            img.loadFromData(result, "JPG")
            self.emit(SIGNAL("Activated( QImage )"), img) 
        
        
class Getwiki(QThread):
    """
    Retrieves the wiki info for an artist
    """
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
    
    def set_values(self, art):
        self.artist = art
        
    def run(self):
        info = Webinfo()
        result = info.get_info("info",None,  self.artist)
        result = QString(result)        
        self.emit(SIGNAL("Activated( QString )"), result)
        
        
class Builddb(QThread):
    """
    Gets files from a directory and build's a 
    media database from the filtered files
    """
    def __init__(self,parent=None):
        QThread.__init__(self, parent)
#        super(Builddb, self).__init__()
        
    def set_values(self, dir):
        """
        Required to put parameters into
        this thread from the outside
        """
        self.media_dir = dir
     
    def __track_list(self):
        formats = [".ogg", ".mp3", ".flac"]
        tracks = []
        # No point trying to speed this up. os.walk is a generator function
        for root, dirname, filenames in os.walk(str(self.media_dir)):
            for name in filenames:
                file_now = os.path.join(root, name)
                try:
                    file_now = file_now.decode("utf-8")
                except UnicodeDecodeError:
                    print "Warning!: latin1 encoded filename. Ignoring", repr(file_now)
                    continue
                ender = os.path.splitext(file_now)[-1]
                ender = ender.lower()
                # We only want to get tags for certain file formats as
                # tagpy can only work with certain types
                if ender in formats:
                    tracks.append(file_now)
        return tracks
        
    def run(self):
        old_prog = 0    
        meta = Metadata()
        media_db = Media()
        dating = Timing()
        tracks = self.__track_list()
        tracks_total = len(tracks)
        
        #TODO:maybe put in a check to not bother getting tags for
        # an existing file and skipping anyway
        strt = time()
        cnt = 0
        for trk in tracks:
            prog = float(cnt ) /  float(tracks_total)
            prog = int(round(100 * prog))
            if prog > old_prog:
                old_prog = prog
                self.emit(SIGNAL("Activated ( int )"), prog)
            tags = meta.extract(trk)
            date = dating.date_now()
            # prepends the fileName as the DB function expects
            # a certain order to the args passed
            tags.insert(0, trk) 
            tags.append(date)
            media_db.add_media(tags)
            cnt += 1
            
        print("%u tracks scanned in: %0.1f seconds" % (cnt, (time() - strt)))
        status = QString("finished")
        self.emit(SIGNAL("Activated ( QString )"), status)
