#!/usr/bin/env python
from time import localtime

class Extraneous:
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
