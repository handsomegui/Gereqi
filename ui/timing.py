#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import localtime

class Timing:
    def __init__(self):
        return
        
    def date_now(self):
        date = localtime()
        year = str(date[0])[2:4]
        month = "%02d" % date[1]
        day = "%02d" % date[2]
        hour = "%02d" % date[3]
        minu = "%02d" % date[4]
        date = "%s%s%s%s%s" % (day, month, year, hour, minu)
        return date
