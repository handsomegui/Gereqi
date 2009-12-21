#!/usr/bin/env python
# -*- coding: utf-8 -*-
import CDDB
import DiscID
import cdrom

class AudioCD:
    def __init__(self):
        return
            
    def __track_times(self):
        device = cdrom.open()
        first, last = cdrom.toc_header(device)
        tr_times = []
        for n in range(first, last+1):
            if n > 1:
                minu, sec = cdrom.toc_entry(device,n)[0:2]
                total = (minu * 60)+ sec
                old_m, old_s = cdrom.toc_entry(device,n-1)[0:2]
                old_t = (old_m * 60)+ old_s
                total -= old_t
                tr_times.append(total)
        return tr_times
            
            
    # ["title", "artist", "album", "date", "genre", "tracknumber" ]
    def get_info(self):
        cd_drive = DiscID.open()
        disc_id = DiscID.disc_id(cd_drive)
        
        query_status, query_info = CDDB.query(disc_id)
        read_status, read_info = CDDB.read(query_info[0]['category'], query_info[0]['disc_id'])
        
        art, alb = read_info['DTITLE'].split(" / ")
        yr = read_info['DYEAR']   
        
        timings = self.__track_times()
        items = []
        
        for trk in range(len(timings)):
            minu = timings [trk] // 60
            secs = timings [trk] % 60
            time_now = "%02d:%02d" % (minu, secs)
            f_name = "cdda://%s" % (trk+1)
            now = [read_info['TTITLE%d' % trk], art, alb, yr, \
                   read_info['DGENRE' ], trk+1, time_now, 44100, f_name ]
            items.append(now)
            
        return items
