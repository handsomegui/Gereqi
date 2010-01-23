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


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite
import os

#TODO: stats database

class Media:
    def __init__(self):
        """
        The table creations perform every class instance(?)
        but only creates them if they don't already exist. This means 
        to add extra columns to an existing table te database file 
        has to be deleted.
        """
        app_dir = "%s/.gereqi/" % os.getenv("HOME")
        db_loc = "%sgereqi.db" % app_dir
        
        if os.path.exists(app_dir) is False:
            print("Need to make a folder.")
            os.mkdir(app_dir)
        self.media_db = sqlite.connect(db_loc)
        self.media_curs = self.media_db.cursor()        
        self.__setup_tables()
        
    def __setup_tables(self):
        # Only the media table is actually used right now
        tables = ['''CREATE TABLE IF NOT EXISTS media (
                file_name    TEXT ,
                title   VARCHAR(50),
                artist  VARCHAR(50),
                album   VARCHAR(50),
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
            self.__query_execute(table)
            
    def __query_fetchall(self, query, args=None):
        self.__query_execute(query, args)
        return self.media_curs.fetchall()
        
    def __query_execute(self, query, args=None):
        if args is not None:
            self.media_curs.execute(query, args)
        else:
            # The execute() doesn't accept NoneTypes
            self.media_curs.execute(query) 
        # Not sure to use this on reads   
        self.media_db.commit() 

    def add_media(self, meta):
        """
        Here we add data into the media database
        """
        query = "INSERT INTO media VALUES (?,?,?,?,?)"
        self.__query_execute(query, meta)
        
    def get_artists(self):
        query = "SELECT DISTINCT artist FROM media"
        return self.__query_fetchall(query)
    
    def get_albums(self, artist):
        args = (artist, )
        query = "SELECT DISTINCT album FROM media WHERE artist=?"
        return self.__query_fetchall(query, args)
        
    def get_files(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT file_name FROM media 
        WHERE artist=?
        AND album=?'''
        return [fnow[0] for fnow in self.__query_fetchall(query, args)]

        
    def get_file(self, artist, album, title):
        args = (artist, album, title)
        query = '''SELECT DISTINCT file_name FROM media 
        WHERE artist=?
        AND album=?
        AND title=?'''
        return self.__query_fetchall(query, args)[0][0]
        
    def get_titles(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT title FROM media 
        WHERE artist=?
        AND album=?'''
        return self.__query_fetchall(query, args)
        
    def get_info(self, file_name):
        args = (file_name, )
        query = '''SELECT * FROM media 
        WHERE file_name=?'''
        return self.__query_fetchall(query, args)
        
    def delete_track(self, fname):
        args = (fname, )
        query = '''DELETE FROM media
        WHERE file_name=?'''
        self.__query_execute(query, args)
    
