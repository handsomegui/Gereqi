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

from PyQt4.QtCore import QString

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
        for trk in range(first, last+1):
            if trk > 1:
                minu, sec = cdrom.toc_entry(device, trk)[0:2]
                total = (minu * 60) + sec
                old_m, old_s = cdrom.toc_entry(device, trk-1)[0:2]
                old_t = (old_m * 60) + old_s
                total -= old_t
                tr_times.append(total)
        return tr_times
            
            
    # ["title", "artist", "album", "date", "genre", "tracknumber" ]
    def get_info(self):
        cd_drive = DiscID.open()
        try:
            disc_id = DiscID.disc_id(cd_drive)
        except cdrom.error,err:
            msg = err[1]
            raise StandardError(str(msg))
            
        
        #query_status, query_info = CDDB.query(disc_id)
        query_info = CDDB.query(disc_id)[1]
        #read_status, read_info = CDDB.read(
        read_info = CDDB.read(query_info[0]['category'], 
                              query_info[0]['disc_id'])[1]
        
        art, alb = read_info['DTITLE'].split(" / ")
        year = read_info['DYEAR']   
        
        timings = self.__track_times()
        items = []
        
        for trk in range(len(timings)):
            minu = timings [trk] // 60
            secs = timings [trk] % 60
            time_now = "%02d:%02d" % (minu, secs)
            f_name = "cdda://%s" % (trk+1)

            now = {"Title":read_info['TTITLE%d' % trk], "Artist": art, 
                   "Album": alb, "Year": year, "Genre": read_info['DGENRE'], 
                   "Track": QString("%02u" % (trk+1)), "Length": time_now, 
                   "Bitrate": QString("%02u" % 44100), "FileName": f_name}
            
            items.append((f_name, now))

        return items
