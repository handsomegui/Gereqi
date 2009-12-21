#!/usr/bin/env python
# -*- coding: utf-8 -*-
import CDDB
import DiscID

class AudioCD:
    def __init__(self):
        cdrom = DiscID.open()
        disc_id = DiscID.disc_id(cdrom)
        
        query_status, query_info = CDDB.query(disc_id)
        read_status, read_info = CDDB.read(query_info[0]['category'], query_info[0]['disc_id'])
        
        
        cd_str = read_info['DTITLE'].split(" / ")
        art = cd_str[0].strip()
        yr,alb = cd_str[1].split(" - ")
        
        print art, yr, alb
        
        for i in range(disc_id[1]):
            print "Track %.02d: %s" % (i, read_info['TTITLE%d' % i])
