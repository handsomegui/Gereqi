#!/usr/bin/env python

import re
import os

class CueSheet:
    path = None
    title = None
    performer = None
    genre = None
    year = None
    tracks = None
    def __init__(self,cue_file):
        self.tracks = []
        self.path = "%s/" % os.path.dirname(cue_file)
        with open(cue_file,'r') as fnow:
            self.__setup(fnow) 
        return
    
    def __between_quotes(self, value):
        return re.findall('"([^"]*)"', value)[0]
        
    def __setup(self,cue_sheet):
        title_found = False
        file_found = False
        cue = cue_sheet.read().split('\r\n')
        trk = None
        for item in cue:
            # Work through the tracks
            if file_found:
                if (("TRACK" in item) and ("AUDIO" in item)):
                    trk = Track(self.file_name)
                    number = item.split()[1]
                    trk.set_number(int(number))
                elif ("TITLE" in item):
                    trk.set_title(self.__between_quotes(item))
                elif ("PERFORMER" in item):                    
                    trk.set_performer(self.__between_quotes(item))
                elif ("INDEX 01" in item):
                    trk.set_index(item.split()[-1])
                    self.tracks.append(trk)
                
            
            # Find album/disc info
            if ("GENRE" in item):
                self.genre = item.split("GENRE")[-1].strip()
            elif ("DATE" in item):
                self.year = item.split("DATE")[-1].strip()
            elif ("PERFORMER" in item):
                self.performer = self.__between_quotes(item)
            elif ("TITLE" in item) and not title_found:
                self.title = self.__between_quotes(item)
                title_found = True
            elif ("FILE" in item):
                self.file_name = self.__between_quotes(item)
                file_found = True
        
    def __repr__(self):
        return "Album(%s,%s,%s,%s,%s)" % \
            (self.title, self.performer, self.genre,
             self.year,self.tracks)
        
    
class Track:
    title = None
    performer = None
    number = None
    index = None
    file_name = None
    
    def __init__(self,file_name=None):
        # This is allows a cuefile with 1 file but many tracks and vice-versa
        self.file_name = file_name
    
    def __repr__(self):
        return "Track(%s,%s,%s,%s,%s)" % \
            (self.index,self.number,self.title,self.performer,self.file_name)
        
    def set_title(self,title):
        self.title = title
    def set_performer(self,performer):
        self.performer = performer
    def set_number(self,number):
        self.number = number
    def set_index(self,index):
        self.index = index

