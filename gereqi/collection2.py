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

from PyQt4.QtCore import *
from PyQt4.QtSql import *
import os

class CollectionDb:
    def __init__(self, mode="SQLITE", args=None):
        """
        Experimental. As sqlite and mysql are barely different trying to
        account for the differences
        """
        self.db_type = mode
        if mode == "SQLITE":
            
            app_dir = "%s/.gereqi/" % os.getenv("HOME")
            db_loc = "%smedia.db" % app_dir
            if QDir(app_dir).exists is False:
                QDir().mkdir(app_dir)
                
            self.media_db = QSqlDatabase.addDatabase("QSQLITE");
            self.media_db.setDatabaseName(db_loc)
        
        elif mode == "MYSQL":
            self.media_db = QSqlDatabase.addDatabase("QMYSQL");
            self.media_db.setHostName(args["hostname"])
            self.media_db.setDatabaseName(args["dbname"])
            self.media_db.setUserName(args["username"])
            self.media_db.setPassword(args["password"])
            # FIXME: this clearly does nothing
            self.media_db.setPort(int(args["port"]))
        
        ok = self.media_db.open()
        if ok is True:
            print "DATABASE OK"
            self.query = QSqlQuery(self.media_db)
            if mode == "SQLITE":
                self.__pragma()
            self.__setup_tables()
        else:
            print "DATABASE ERROR"
            return        
        
    def __setup_tables(self):
        print self.db_type
        if self.db_type == "SQLITE":
            tables = ['''CREATE TABLE IF NOT EXISTS media (
                    file_name    TEXT ,
                    title   VARCHAR(50),
                    artist  VARCHAR(50),
                    album   VARCHAR(50),
                    year   SMALLINT(4),
                    genre  VARCHAR(20),
                    track UNSIGNED TINYINT(2),
                    length  VARCHAR(5),
                    bitrate SMALLINT(4),
                    added UNSIGNED INT(10),
                    playcount SMALLINT(5),
                    rating TINYINT(1),
                    PRIMARY KEY (file_name)
                    )'''
                    , 
                    '''CREATE TABLE IF NOT EXISTS playlist (
                    name TEXT,
                    file_name TEXT
                    )''']      
        elif self.db_type == "MYSQL":
            tables = ['''CREATE TABLE IF NOT EXISTS media (
                                file_name    VARCHAR(255) ,
                                title   VARCHAR(50),
                                artist  VARCHAR(50),
                                album   VARCHAR(50),
                                year   SMALLINT(4) UNSIGNED,
                                genre  VARCHAR(20),
                                track  TINYINT(2) UNSIGNED,
                                length  VARCHAR(5),
                                bitrate SMALLINT(4) UNSIGNED,
                                added INT(10) UNSIGNED ,
                                playcount SMALLINT(5) UNSIGNED,
                                rating TINYINT(1) UNSIGNED,
                                PRIMARY KEY (file_name)
                                ) DEFAULT CHARSET=utf8''', 
                            '''CREATE TABLE IF NOT EXISTS playlist (
                                name VARCHAR(255),
                                file_name VARCHAR(255),
                                PRIMARY KEY (name)
                                ) DEFAULT CHARSET=utf8''']  
        for table in tables:
            self.__query_execute(table)            
            
    def __query_fetchone(self, query, args=None):
        result = self.__query_execute(self.__query_process(query, args), args)
        return self.query.result()
            
    def __query_fetchall(self, field_num):
        output = []
        while self.query.next() is True:
            if field_num <=1:
                output.append(self.query.value(0).toString())
            else:
                tmp = []
                for  n in range(field_num):
                    r = self.query.value(n).toString()
                    tmp.append(r)
                output.append(tmp)
        return output
        
    def __query_execute(self, query, args=None):
            if args is not None:
                self.query.prepare(query)
                for arg in args:
                    self.query.addBindValue(arg)
                self.query.exec_()
            else:
                # The execute() doesn't accept NoneTypes
                self.query.exec_(query)                 
    
    def __execute_write(self, query, args=None):
        self.__query_execute(query, args)
        self.media_db.commit()
        
    def __pragma(self):
        """
        This command will cause SQLite to not wait on data to reach the disk surface, 
        which will make write operations appear to be much faster. 
        But if you lose power in the middle of a transaction, your database file might corrupt.
        """
        query = '''PRAGMA synchronous = OFF'''
        self.__query_execute(query)
        

    def add_media(self, meta):
        """
        Here we add data into the media database
        """
        if self.db_type == "SQLITE":
            query = '''INSERT OR REPLACE INTO media 
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''
        elif self.db_type == "MYSQL":
            query = '''REPLACE INTO media
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''
        self.__execute_write(query, tuple(meta))
        
    def inc_count(self, cnt, fname):
        args = (cnt, fname)
        query = '''UPDATE media
                        SET playcount=?
                        WHERE file_name=?'''
        self.__execute_write(query, args)
        
    def delete_track(self, fname):
        args = (fname, )
        query = '''DELETE FROM media
                        WHERE file_name=?'''
        print("DELETING FROM DB: %s" % fname)
        self.__execute_write(query, args)
        
    def get_artists(self):
        query = '''SELECT DISTINCT artist
                        FROM media'''  
        self.__query_execute(query)
        result = self.__query_fetchall(1)
        return result

    def get_artists_timed(self, filt):
        query = '''SELECT DISTINCT artist 
                            FROM media
                            WHERE added>?'''
        self.__query_execute(query, (filt, ))
        result = self.__query_fetchall(1)
        return result
        
    def get_albums(self, artist):
        query = '''SELECT DISTINCT album 
                            FROM media
                            WHERE artist=?'''
        self.__query_execute(query, (artist, ))
        result = self.__query_fetchall(1)
        return result
        
    def get_albums_timed(self, artist, filt):
        args = (artist, filt)
        query = '''SELECT DISTINCT album   
                            FROM media
                            WHERE artist=?
                            AND added>?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall(1)
        return result
        
    def get_albums_all(self):
        query = '''SELECT DISTINCT album
                        FROM media'''
        self.__query_execute(query)
        result = self.__query_fetchall(1)
        return result        

    def get_albums_all_timed(self, filt):
        query = '''SELECT DISTINCT album
                        FROM media   
                        WHERE added>?'''
        self.__query_execute(query, (filt, ))
        result = self.__query_fetchall(1)
        return result
        
    def get_files(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=?
                        AND album=?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall(1)
        return result
        
    def get_file(self, artist, album, title):
        args = (artist, album, title)
        query = '''SELECT DISTINCT file_name 
                        FROM media 
                        WHERE artist=?
                        AND album=?
                        AND title=?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall(1)[0]
        return result
        
    def get_album_file(self, album, title):
        args = (album, title)
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=?
                        AND title=?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall(1)[0]
        return result
        
    def get_album_files(self, album):
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=?'''
        self.__query_execute(query, (album, ))
        result = self.__query_fetchall(1)
        return result
        
    def get_album_files_timed(self, album, filt):
        args = (album, filt)
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=?
                        AND added>?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall(1)
        return result
        
    def get_artists_files(self, artist):
        query = '''SELECT DISTINCT file_name 
                            FROM media
                            WHERE artist=?'''
        self.__query_execute(query, (artist, ))
        result = self.__query_fetchall(1)
        return result
                        
    def get_titles(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT title,track 
                        FROM media 
                        WHERE artist=?
                        AND album=?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall(2)
        return result

    def get_titles_timed(self, artist, album, filt):
        args = (artist, album, filt)
        query = '''SELECT DISTINCT title,track 
                        FROM media 
                        WHERE artist=?
                        AND album=?
                        AND added>?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall(2)
        return result
        
    def get_album_titles(self, album):
        query = '''SELECT DISTINCT title
                        FROM media
                        WHERE album=?'''
        self.__query_execute(query,(album, ))
        result = self.__query_fetchall(1)
        return result
        
    def get_album_files_timed(self, album, filt):
        args = (album, filt)
        query = '''SELECT DISTINCT title
                        FROM media
                        WHERE album=?
                        AND added>?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall(1)
        return result
        
    def get_info(self, file_name):
        query = '''SELECT
                        file_name, title,artist,album,year,genre,
                        track,length,bitrate,added,playcount,rating
                        FROM media 
                        WHERE file_name=?'''
        self.__query_execute(query, (file_name, ))
        try:
            result = self.__query_fetchall(12)[0]
            return result
        except IndexError:
            return
        
    def playlist_add(self, *params):
        query = '''INSERT INTO playlist 
                            VALUES (?,?)'''
        self.__execute_write(query, params)
        
    def playlist_list(self):
        query = '''SELECT DISTINCT name 
                            FROM playlist'''
        self.__query_execute(query)
        result = self.__query_fetchall(1)
        return result
        
    def playlist_tracks(self, name):
        query = '''SELECT file_name 
                            FROM playlist
                            WHERE name=?'''
        self.__query_execute(query, (name, ))
        result = self.__query_fetchall(1)
        return result
        
    def playlist_delete(self, name):
        query = '''DELETE FROM playlist
                        WHERE name=?'''
        self. __execute_write(query, (name, ))

    def search_by_titandart(self, art, tit):
        args = (art, tit)
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=?
                        AND title=?'''        
        self.__query_execute(query, args)
        result = self.__query_fetchall(1)
        return result
   
    def drop_media(self):
        query = '''DROP TABLE media'''
        self.__execute_write(query)
        self.__setup_tables()
