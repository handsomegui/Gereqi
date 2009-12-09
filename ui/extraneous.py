#!/usr/bin/env python
from time import localtime
from os import path
from database import Media

class Extraneous:
    """
    Miscellaneous functions that have no real place to
    go but are used in various Classes.
    """
    def __init__(self):
        return
        
    def qstr2uni(self, qstr):
        """
        This is needed as you can't convert cleanly from qstring
        to unicode, which the database requires
        """
        now = str(qstr.toUtf8())
        return now.decode("utf-8")
        
    def date_now(self):
        date = localtime()
        year = str(date[0])[2:4]
        month = "%02d" % date[1]
        day = "%02d" % date[2]
        hour = "%02d" % date[3]
        minu = "%02d" % date[4]
        date = "%s%s%s%s%s" % (day, month, year, hour, minu)
        return date

    def check_source_exists(self, fname):
        """
        Checks whether if a track exists on drives.
        If not, it removes the track from the database.
        """
        if path.exists(fname):
            return True
        else:
            db = Media()
            print("WARNING: removed non-existing track, %s, from database" % fname)
            db.delete_track(fname)
