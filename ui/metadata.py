#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import tagpy

class Metadata:
    def __init__(self):
        return
        
    def extract(self, file_name):
        """
        Gets the file's metadata and outputs to
        whatever needs it. tagpy doesn't return 
        safe 'empty' values so i'ev had to bodge 
        it a little with a load of try and excepts
        """
        
        tags = tagpy.FileRef(str(file_name))
        
        try:
            track = tags.tag().track
            track = str(track)
            if len(track.strip()) < 1:
                track = "Unknown"
        except:
            track = "0"
        try:
            title = tags.tag().title
            title = title.replace('''"''',"")
            title = title.encode("iso-8859-15")  
            
            if not title:
                title = file_name.split("/")[-1]
                title = title.split(".")[0]
        except:
            title = file_name.split("/")[-1]
            title = title.split(".")[0]
        
        try:
            artist = tags.tag().artist
            artist = artist.replace('''"''',"")
            artist = artist.encode("iso-8859-15")
            if len(artist.strip()) < 1:
                artist = "Unknown Artist"
                
        except:
            artist = "Unknown Artist"
            
        try:
            album = tags.tag().album
            album = album.replace('''"''',"")
            album = album.encode("iso-8859-15")
            if len(album.strip()) < 1:
                album = "Unknown Album"
        except:
            album = "Unknown Album"

        try: 
            genre = tags.tag().genre
            genre = genre.replace('''"''',"")
            genre = genre.encode("iso-8859-15")
            if len(genre.strip()) < 1:
                genre = "Unknown"
        except:
            genre = "Unknown"
        
        try: 
            year = tags.tag().year
            year = str(year)
            if len(year.strip()) < 1:
                year = "0"
        except: 
            year = "0"
        
        try:
            bitrate = tags.audioProperties().bitrate
            bitrate = str(bitrate)
            if len(bitrate.strip()) < 1:
                bitrate = "Unknown"
        except:
            bitrate = "0"
            
        try:
            seconds = tags.audioProperties().length
            minim = seconds // 60
            rem = seconds % 60

            length = "%02d:%02d" % (minim, rem)
        except:
            length = "00:00"
        
        return [track, title, artist, album, year, genre, length, bitrate]
        
        
    def write_meta(self, file_name, *meta):
        """
        Here, using editing tools in the main ui, the file's metadata 
        can be permanently written        
        """
        print file_name, " ".join(meta)
        return
        

