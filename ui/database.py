#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite
from os import mkdir, getenv, path

#TODO: stats database

class Media:
    def __init__(self):
        """
        The table creations perform every class instance(?)
        but only creates them if they don't already exist. This means 
        to add extra columns to an existing table te database file amaroq.db
        has to be deleted.
        """
        app_dir = getenv("HOME")
        app_dir = "%s/.amaroq/" % app_dir
        self.media_db = "%samaroq.db" % app_dir
        
        if not path.exists(app_dir):
            print "need to make a folder"
            mkdir(app_dir)

        self.media_db = sqlite.connect(self.media_db)
        self.media_curs = self.media_db.cursor()
        
        self.setup_tables()
        
    def setup_tables(self):
        # Only the media table is actually used right now
        tables = ['''CREATE TABLE IF NOT EXISTS media (
                file_name    TEXT ,
                track    UNSIGNED TINYINT(2),
                title   VARCHAR(50),
                artist  VARCHAR(50),
                album   VARCHAR(50),
                year    UNSIGNED SMALLINT(4),
                genre   VARCHAR(50),
                length  VARCHAR(5),
                bitrate UNSIGNED SMALLINT(4),
                added UNSIGNED MEDIUMINT(6),
                PRIMARY KEY (file_name) ON CONFLICT IGNORE
                )'''
                , 
                '''CREATE TABLE IF NOT EXISTS playlist (
                id   INT IDENTITY (1, 1),
                name    VARCHAR(20),
                file_name    TEXT,
                track  UNSIGNED SMALLINT(3),
                PRIMARY KEY (id)
                )'''
                , 
                '''CREATE TABLE IF NOT EXISTS settings (
                setting   TEXT,
                value   TEXT,
                PRIMARY KEY (setting) ON CONFLICT  REPLACE
                )'''
                , 
                '''CREATE TABLE IF NOT EXISTS local_list (
                id INT  IDENTITY (1,1),
                filename TEXT,
                list UNSIGNED SMALLINT(3),
                PRIMARY KEY (id)
                )''']      
        
        for table in tables:
            self.media_curs.execute(table)
            self.media_db.commit() 

    def add_media(self, meta):
        """
        Here we add data into the media database
        """
        try:
            self.media_curs.execute("INSERT INTO media VALUES (?,?,?,?,?,?,?,?,?,?)", meta)
            self.media_db.commit()
        except:
            print meta
        
        
    def get_artists(self):
        self.media_curs.execute("SELECT DISTINCT artist FROM media")
        return self.media_curs.fetchall()
    
    def get_albums(self, artist):
        artist = (artist, )
        self.media_curs.execute("SELECT DISTINCT album FROM media WHERE artist=?", artist)
        return self.media_curs.fetchall()
        
    def get_files(self, artist, album):
        args = (artist, album)
        print args
        query = '''SELECT DISTINCT file_name FROM media 
        WHERE artist=?
        AND album=?'''
        self.media_curs.execute(query, args)
        return self.media_curs.fetchall()
        
    def get_file(self, artist, album, title):
        args = (artist, album, title)
        print args
        query = '''SELECT DISTINCT file_name FROM media 
        WHERE artist=?
        AND album=?
        AND title=?'''
        self.media_curs.execute(query, args)
        # Should really be fetchOne()
        return self.media_curs.fetchall()
        
    def get_titles(self, artist, album):
        args = (artist, album)
        print args
        query = '''SELECT DISTINCT title FROM media 
        WHERE artist=?
        AND album=?'''
        self.media_curs.execute(query, args)
        return self.media_curs.fetchall()
        
    def get_info(self, file_name):
        args = (file_name, )
        query = '''SELECT * FROM media 
        WHERE file_name=?'''
        self.media_curs.execute(query, args)
        return self.media_curs.fetchall()
        
        
    def queryfetchall(self, query, args):
        self.media_curs.execute(query, args)
        return self.media_curs.fetchall()
        
    def query_execute(self, query, args=None):
        self.media_curs.execute(query, args)
        # Not sure to use this on reads   
        self.media_db.commit() 
        
