#Copyright 2009 Jonathan.W.Noble <jonnobleuk@gmail.com>


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


from sqlite3 import dbapi2 as sqlite
import os

# TODO: stats database
# TODO: cover-art db
#FIXME: fix this horrible mess
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
        
        # Nowhere to put db
        if os.path.exists(app_dir) is False:
            os.mkdir(app_dir)
        self.media_db = sqlite.connect(db_loc)
        self.media_curs = self.media_db.cursor()        
        self.__setup_tables()
        
    def __setup_tables(self):
        tables = ['''CREATE TABLE IF NOT EXISTS media (
                file_name    TEXT ,
                title   VARCHAR(50),
                artist  VARCHAR(50),
                album   VARCHAR(50),
                added UNSIGNED MEDIUMINT(6),
                playcount SMALLINT(5),
                rating TINYINT(0),
                PRIMARY KEY (file_name) ON CONFLICT IGNORE
                )'''
                , 
                '''CREATE TABLE IF NOT EXISTS playlist (
                name TEXT,
                file_name TEXT
                )'''
                , 
                '''CREATE TABLE IF NOT EXISTS settings (
                setting   TEXT,
                value   TEXT,
                PRIMARY KEY (setting) ON CONFLICT  REPLACE
                )'''
                , 
                '''CREATE TABLE IF NOT EXISTS local_list (
                filename TEXT,
                list UNSIGNED SMALLINT(3)
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
        query = '''INSERT INTO media 
                        VALUES (?,?,?,?,?,?,?)'''
        self.__query_execute(query, meta)
        
    def get_artists(self):
        query = '''SELECT DISTINCT artist
                        FROM media'''
        artists = [art[0] for art in self.__query_fetchall(query)]
        return artists
        
    def get_artists_timed(self, time):
        query = '''SELECT DISTINCT artist 
                            FROM media
                            WHERE added>?'''
        artists = [art[0] for art  in self.__query_fetchall(query, (time, ))]
        return artists
    
    def get_albums(self, artist):
        args = (artist, )
        query = '''SELECT DISTINCT album 
                            FROM media
                            WHERE artist=?'''
                            
        albums = [alb[0] for alb in self.__query_fetchall(query, args)]
        return albums
        
    def get_albums_timed(self, artist, time):
        args = (artist, time)
        query = '''SELECT DISTINCT album   
                            FROM media
                            WHERE artist=?
                            AND added>?'''
        albums = [alb[0] for alb in self.__query_fetchall(query, args)]
        return albums
        
    def get_files(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=?
                        AND album=?'''
        files = [fnow[0] for fnow in self.__query_fetchall(query, args)]
        return files
        
    def get_file(self, artist, album, title):
        args = (artist, album, title)
        query = '''SELECT DISTINCT file_name 
                        FROM media 
                        WHERE artist=?
                        AND album=?
                        AND title=?'''
        return self.__query_fetchall(query, args)[0][0]
        
    def get_titles(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT title 
                        FROM media 
                        WHERE artist=?
                        AND album=?'''
        titles = [title[0] for title in self.__query_fetchall(query, args)]
        return titles

    def get_titles_timed(self, artist, album, time):
        args = (artist, album, time)
        query = '''SELECT DISTINCT title 
                        FROM media 
                        WHERE artist=?
                        AND album=?
                        AND added>?'''
        titles = [title[0] for title in self.__query_fetchall(query, args)]
        return titles
        
    def get_info(self, file_name):
        query = '''SELECT * 
                        FROM media 
                        WHERE file_name=?'''
        return self.__query_fetchall(query, (file_name, ))
        
    def delete_track(self, fname):
        args = (fname, )
        query = '''DELETE FROM media
                        WHERE file_name=?'''
        self.__query_execute(query, args)
    
    def playlist_add(self, *params):
        query = '''INSERT INTO playlist 
                            VALUES (?,?)'''
        self.__query_execute(query, params)
        
    def playlist_list(self):
        query = '''SELECT DISTINCT name 
                            FROM playlist'''
        return self.__query_fetchall(query)
        
    def playlist_tracks(self, name):
        query = '''SELECT file_name 
                            FROM playlist
                            WHERE name=?'''
        return self.__query_fetchall(query, (name, ))
        
        
    def playlist_delete(self, name):
        query = '''DELETE FROM playlist
                        WHERE name=?'''
        self.__query_execute(query, (name, ))

    def inc_count(self, cnt, fname):
        query = '''UPDATE media
                        SET playcount=?
                        WHERE file_name=?'''
        self.__query_execute(query, (cnt, fname))
        
    def search_by_titandart(self, art, tit):
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=?
                        AND title=?'''        
        return self.__query_fetchall(query, (art, tit))
