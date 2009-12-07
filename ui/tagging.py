#!/usr/bin/env python
#TODO: Import based on gstreamer capabilities
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.easyid3 import EasyID3
from os import stat

class Tagging:
    def __init__(self, formats):
        # Formats have to be file extensions without
        # the '.' and in lower-case
        self.a_formats = formats
        
    def __treat_tracknum(self, track):
        print track, type(track)
        if "/" in track:
            now = track.split("/")[0]
        else:
            now = track
        return int(now)
        
    def __dict_to_list(self, item):
        return [self.__treat_tracknum(item["tracknumber"][0]), 
                                           item["title"][0], 
                                           item["artist"][0], 
                                           item["album"][0], 
                                           item["date"][0], 
                                           item["genre"][0]]
        
        
    def __sec_to_time(self, seconds):
        minim = seconds // 60
        rem = seconds % 60
        length = "%02d:%02d" % (minim, rem)
        
    def __mp3_extract(self, fname):
        audio = EasyID3(fname)
        other = MP3(fname)
        length = self.__sec_to_time(round(other.info.length))
        bitrate = round(other.info.bitrate / 1024)
        
        tags = self.__dict_to_list(audio)
        tags.append(length)
        tags.append(bitrate)
        return tags
        
    def __flac_extract(self, fname):
        audio = FLAC(fname)
        length = self.__sec_to_time(rnd(other.info.length))
        f_size = stat(fname).st_size * 8
        bitrate = rnd(f_size / other.info.length / 1024)
        
    def extract(self, fname):
        """
        Based on the file-format extract info
        """
        ext = fname.split(".")[-1].lower()
        if ext in self.a_formats:
            if ext == "flac":
                tags = self.__flac_extract(fname)
            elif ext == "mp3":
                tags = self.__mp3_extract(fname)
            elif ext == "ogg":
                tags = self.__ogg_extract(fname)
                
            return tags
            return [track, title, artist, album, year, genre, length, bitrate]
