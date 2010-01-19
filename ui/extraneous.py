#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        
    def check_source_exists(self, fname):
        """
        Checks whether if a track exists on drives.
        If not, it removes the track from the database.
        """
        if path.exists(fname) is True:
            return True
        else:
            db = Media()
            print("WARNING: removed non-existing track, %s, from database" % fname)
            db.delete_track(fname)
