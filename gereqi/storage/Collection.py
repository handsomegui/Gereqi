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
from PyQt4.QtCore import QCryptographicHash as QHash
from PyQt4.QtSql import *

from gereqi.storage.Settings import Settings

import os


# TODO: remove the '_timed()' functions

class CollectionDb:
    media_db = None
    def __init__(self, name):        
        self.__config_db(name)
        
    def __config_db(self,name):
        db_name = QLatin1String(name)
        sets_db = Settings()
        self.db_type = sets_db.get_database_setting("type")
        if self.db_type == "MYSQL":                            
            CollectionDb.media_db = QSqlDatabase.addDatabase("QMYSQL", db_name)
            CollectionDb.media_db.setHostName(sets_db.get_database_setting("hostname"))
            CollectionDb.media_db.setDatabaseName(sets_db.get_database_setting("dbname"))
            CollectionDb.media_db.setUserName(sets_db.get_database_setting("username"))
            CollectionDb.media_db.setPassword(sets_db.get_database_setting("password"))
            # FIXME: this clearly does nothing
            CollectionDb.media_db.setPort(int(sets_db.get_database_setting("port")))
                            
        else:        
            self.db_type = "SQLITE"
            app_dir = "%s/.gereqi/" % os.getenv("HOME")
            db_loc = "%smedia.db" % app_dir
            if QDir(app_dir).exists is False:
                QDir().mkdir(app_dir)                
            CollectionDb.media_db = QSqlDatabase.addDatabase("QSQLITE", db_name)
            CollectionDb.media_db.setDatabaseName(db_loc)
        
        
        ok = CollectionDb.media_db.open()
        if ok is True:
            print "DATABASE OK",self.db_type
            CollectionDb.query = QSqlQuery(CollectionDb.media_db)
            if self.db_type == "SQLITE":
                self.__pragma()
            self.__setup_tables()
        else:
            err = self.media_db.lastError().text()
            raise StandardError(err)
        
    def __setup_tables(self):
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
                        rating TINYINT(1),
                        PRIMARY KEY (file_name) )''', 
                    '''CREATE TABLE IF NOT EXISTS playlist (
                        name TEXT,
                        file_name TEXT)''',
                    '''CREATE TABLE IF NOT EXISTS history (
                        timestamp    INT(10) PRIMARY KEY,
                        file_name    TEXT)''']
                  
        elif self.db_type == "MYSQL":
            # Mysql requires slightly different tables
            tables = ['''CREATE TABLE IF NOT EXISTS media (
                                id VARCHAR(32) PRIMARY KEY,
                                file_name    TEXT,
                                title    VARCHAR(50),
                                artist    VARCHAR(50),
                                album    VARCHAR(50),
                                year    SMALLINT(4) UNSIGNED,
                                genre    VARCHAR(20),
                                track    TINYINT(2) UNSIGNED,
                                length    VARCHAR(5),
                                bitrate    SMALLINT(4) UNSIGNED,
                                added    INT(10) UNSIGNED ,
                                rating    TINYINT(1) UNSIGNED) DEFAULT CHARSET=utf8 ''', 
                            '''CREATE TABLE IF NOT EXISTS playlist (
                                id SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                file_name TEXT) DEFAULT CHARSET=utf8 ''',
                            '''CREATE TABLE IF NOT EXISTS history (
                                timestamp    INT(10) PRIMARY KEY,
                                file_name    TEXT) DEFAULT CHARSET=utf8 ''']
            
        for table in tables:
            self.__query_execute(table)
            
            
    def __query_fetchall(self):
        """
        Returns the result of the last query in
        a list of dicts if more than 1 field
        otherwise, a list
        """
        record = CollectionDb.query.record
        field_count = record().count()
        fields = []
        for cnt in range(field_count):
            fields.append( record().field(cnt).name() )
        
        results = []
        row = 0
        
        while CollectionDb.query.next():
            if len(fields) > 1:
                row_result = {}
                for field in fields:                    
                    row_result[str(field)] = record().value(field).toString()            
                results.append(row_result)
                row+=1
            else:
                results.append(record().value(0).toString())
        
        return results
        
    def __query_execute(self, query, args=None):
        if args is not None:
            CollectionDb.query.prepare(query)
            for arg in args:
                CollectionDb.query.addBindValue(arg)
            CollectionDb.query.exec_()
        else:
            # The execute() doesn't accept NoneTypes
            CollectionDb.query.exec_(query)   
            
        err = CollectionDb.query.lastError()
        if err.isValid():
            print err.text(),CollectionDb.query.lastQuery()
            
    
    def __execute_write(self, query, args=None):
        self.__query_execute(query, args)
        CollectionDb.media_db.commit()
        
    def __pragma(self):
        """
        This command will cause SQLite to not wait on data to reach the disk surface, 
        which will make write operations appear to be much faster. 
        But if you lose power in the middle of a transaction, 
        your database file might corrupt.
        """
        query = '''PRAGMA synchronous = OFF'''
        self.__query_execute(query)
        
#######################################################################################

    def add_media(self, meta):
        """
        Here we add data into the media database
        """
        if self.db_type == "SQLITE":
            query = '''INSERT INTO media 
                            VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
        elif self.db_type == "MYSQL":
            query = '''INSERT IGNORE INTO media
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''                        
            # Required as MYSQL will not accept a TEXT data-type as
            # a primary key. However, file_name needs to be a TEXT
            # as VARCHAR is limiting. Instead, an md5 hash of the file_name 
            # becomes the PRIMARY KEY instead.
            hash = QHash.hash(meta[0],1).toHex()
            meta.insert(0,hash)            
        self.__execute_write(query, tuple(meta))
        
    def inc_count(self, timestamp, fname):
        """
        Doesn't change count directly but by adding another
        row into DB with a file_name the row_count (play count)
        would increase
        """
        args = (timestamp, fname)
        query = '''INSERT INTO history
                    VALUES(?,?)'''
        self.__execute_write(query, args)
        
    def delete_track(self, fname):
        args = (fname, )
        query = '''DELETE FROM media
                        WHERE file_name=?'''
        print("DELETING FROM DB: %s" % fname)
        self.__execute_write(query, args)
        
    def get_artists(self, filt=0):
        query = '''SELECT DISTINCT artist 
                    FROM media
                    WHERE added > ?
                    ORDER BY lower(artist)'''
        self.__query_execute(query, (filt, ))
        result = self.__query_fetchall()
        return result
        
    def get_albums(self, artist, filt=0):
        args = (artist, filt)
        query = '''SELECT DISTINCT album   
                    FROM media
                    WHERE artist=?
                    AND added > ?
                    ORDER BY lower(album)'''
        self.__query_execute(query, args)
        result = self.__query_fetchall()
        return result
        
    def get_albums_all(self, filt=0):
        query = '''SELECT DISTINCT album
                        FROM media   
                        WHERE added>?
                        ORDER BY lower(album)'''
        self.__query_execute(query, (filt, ))
        result = self.__query_fetchall()
        return result
        
    def get_files(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=?
                        AND album=?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall()
        return result
        
    def get_files_all(self):
        query = '''SELECT DISTINCT file_name
                    FROM media'''
                    
        self.__query_execute(query)
        result = self.__query_fetchall()
        return result
        
    def get_file(self, artist, album, title):
        args = (artist, album, title)
        query = '''SELECT DISTINCT file_name 
                        FROM media 
                        WHERE artist=?
                        AND album=?
                        AND title=?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall()[0]
        return result
        
    def get_album_file(self, album, title):
        args = (album, title)
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=?
                        AND title=?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall()[0]
        return result
        
    def get_album_files(self, album,filt=0):
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=?
                        AND added>?'''
        self.__query_execute(query, (album, filt ))
        result = self.__query_fetchall()
        return result
        
       
    def get_artists_files(self, artist):
        query = '''SELECT DISTINCT file_name 
                            FROM media
                            WHERE artist=?'''
        self.__query_execute(query, (artist, ))
        result = self.__query_fetchall()
        return result
                        
    def get_titles(self, artist, album, filt=0):
        args = (artist, album, filt)
        query = '''SELECT DISTINCT title,track 
                        FROM media 
                        WHERE artist=?
                        AND album=?
                        AND added>?'''
        self.__query_execute(query, args)
        result = self.__query_fetchall()
        return result
        
    def get_album_titles(self, album):
        query = '''SELECT DISTINCT title
                        FROM media
                        WHERE album=?'''
        self.__query_execute(query,(album, ))
        result = self.__query_fetchall()
        return result
        
       
    def get_info(self, file_name):
        query = '''SELECT
                        file_name, title,artist,album,year,genre,
                        track,length,bitrate,added,rating
                        FROM media 
                        WHERE file_name=?'''
        self.__query_execute(query, (file_name, ))
        try:
            result = self.__query_fetchall()[0]
            return result
        except IndexError:
            return
        
    def playlist_add(self, *params):
        if self.db_type == "SQLITE":
            query = '''INSERT OR REPLACE INTO playlist 
                        VALUES (?,?)'''

        elif self.db_type == "MYSQL":
            query = '''INSERT INTO playlist 
                        (name,file_name)
                        VALUES (?,?)'''

        self.__execute_write(query, params)
        
    def playlist_list(self):
        query = '''SELECT DISTINCT name 
                    FROM playlist'''
        self.__query_execute(query)
        result = self.__query_fetchall()
        return result
        
    def playlist_tracks(self, name):
        query = '''SELECT file_name 
                            FROM playlist
                            WHERE name=?'''
        self.__query_execute(query, (name, ))
        result = self.__query_fetchall()
        return result
        
    def playlist_delete(self, name):
        query = '''DELETE FROM playlist
                        WHERE name=?'''
        self.__execute_write(query, (name, ))

    def search_by_titandart(self, art, tit):
        args = (art, tit)
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=?
                        AND title=?'''        
        self.__query_execute(query, args)
        result = self.__query_fetchall()
        return result
   
    def drop_media(self):
        query = '''DROP TABLE media'''
        self.__execute_write(query)
        self.__setup_tables()
        
    def restart_db(self,name=None):
        """
        Disconnects db and removes connection
        """
        #print "AVAIL: %s TOGO %s " % (self.__connections(), name)
        if name:
            CollectionDb.query.finish()
#            del CollectionDb.query
#            db = CollectionDb.media_db.database(QLatin1String(name))
#            db.close() 
            CollectionDb.media_db.removeDatabase(name)
            self.__config_db(name) 

    def __connections(self):
        db_names = CollectionDb.media_db.connectionNames()
        return [str(db_names[cnt]) for cnt in range(db_names.count())]
    
    def shutdown(self):
        """
            Trying to shutdown cleanly. The Qt docs fail me.
        """
        conn_names = self.__connections()
        CollectionDb.query.finish()
        del CollectionDb.query
        for conn in conn_names:
            CollectionDb.media_db.database(QLatin1String(conn)).close()
            CollectionDb.media_db.removeDatabase(conn)
            
        
            