#!/usr/bin/env python
#TODO: Import based on gstreamer capabilities
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.easyid3 import EasyID3
from os import stat

class Manipulations:
    def treat_tracknum(self, track):
        """
        Turns the track tag into an integer
        """
        if "/" in track:
            now = track.split("/")[0]
        else:
            now = track
        return int(now)
        
    def dict_to_list(self, item):
        """
        Takes the mutagen dictionary and converts into
        a list. Catches missing values and inserts suitable
        None-values
        """
        headers = ["tracknumber", "title", "artist", "album", "date", "genre"]
        values = []
        for hdr in headers:
            try:
                if hdr == "tracknumber":
                    val = self.treat_tracknum(item[hdr][0])
                else:
                    val = item[hdr][0]
            # Used to use KeyError exception but got very odd  list-index error about 'val'
            except:
                val = None
            if not val:
                if (hdr == "tracknumber") or (hdr == "date"):
                    val = 0
                else:
                    val = "Unknown"
            values.append(val)
            
        return values
        
    def sec_to_time(self, seconds):
        """
        Converts seconds into min:sec 
        time format
        """
        minim = seconds // 60
        rem = seconds % 60
        length = "%02d:%02d" % (minim, rem)
        return length
        
    def manual_bitrate(self, fname,  item):
        f_size = stat(fname).st_size * 8
        bitrate = int(round(f_size / item.info.length / 1024))
        return bitrate
        
class Tagging:
    def __init__(self, formats):
        # Formats have to be file extensions without
        # the '.' and in lower-case
        self.a_formats = formats
        self.manip = Manipulations()
        
    def __mp3_extract(self, fname):
        """
        mp3s require 2 instances as EasyIDE
        lacks length and bitrate tags
        """
        try:
            audio = EasyID3(fname)
        # ID3NoHeaderError
        except:
            print "mp3 file does not start with ID3 tag:", fname
            return
        try:
            other = MP3(fname)
        #HeaderNotFoundError
        except: 
            print "Headers not found. Can't sync to an MPEG frame", fname
            return
        length = self.manip.sec_to_time(round(other.info.length))
        bitrate = int(round(other.info.bitrate / 1024))
        tags = self.manip.dict_to_list(audio)
        tags.append(length)
        tags.append(bitrate)
        return tags
        
    def __oggflac_extract(self, fname, mode):
        """
        Flacs lack bitrate tag so requires
        a simple file-size/playtime calculation.
        The values for oggs are unbelievably 
        massive
        """
        if mode == "flac":
            audio = FLAC(fname)
        elif mode == "ogg":
            audio = OggVorbis(fname)
        length = self.manip.sec_to_time(round(audio.info.length))
        bitrate = self.manip.manual_bitrate(fname, audio)
        tags = self.manip.dict_to_list(audio)
        tags.append(length)
        tags.append(bitrate)
        return tags
        
        
    def extract(self, fname):
        """
        Based on the file-format extract info
        """
        ext = fname.split(".")[-1].lower()
        if ext in self.a_formats:
            if ext == "flac":
                tags = self.__oggflac_extract(fname, ext)
            elif ext == "mp3":
                tags = self.__mp3_extract(fname)
            elif ext == "ogg":
                tags = self.__oggflac_extract(fname, ext)
                
            return tags
