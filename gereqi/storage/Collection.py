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

from PySide.QtCore import *
from PySide.QtSql import *

from gereqi.storage.Settings import Settings
import Tables

import os


class CollectionDb:
    media_db = None
    def __init__(self, name):
        self.name = name  
        self.__config_db()
        
    def __del__(self):
        """
        To ensure the db-connection is closed
        Seems to calm down the QSqlDatabasePrivate::removeDatabase warnings
        """
        self.close_connection()
        
    def __config_db(self):
        sets_db = Settings()
        self.db_type = sets_db.get_database_setting("type")
        if self.db_type == "MYSQL":                            
            CollectionDb.media_db = QSqlDatabase.addDatabase("QMYSQL", self.name)
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
            CollectionDb.media_db = QSqlDatabase.addDatabase("QSQLITE", self.name)
            CollectionDb.media_db.setDatabaseName(db_loc)
        
        
        ok = CollectionDb.media_db.open()
        if ok is True:
            print "DATABASE OK",self.db_type
            self.query = QSqlQuery(CollectionDb.media_db)
            if self.db_type == "SQLITE":
                self.__pragma()
            self.__setup_tables()
        else:
            err = self.media_db.lastError().text()
            raise StandardError(err)
        
    def __setup_tables(self):
        if self.db_type == "SQLITE":
            tables = Tables.Sqlite().tables
                  
        elif self.db_type == "MYSQL":
            # Mysql requires slightly different tables
            tables = Tables.Mysql.tables

            
        for table in tables:
            self.__query_execute(table)
            
            
    def __query_fetchall(self):
        """
        Returns the result of the last query in
        a list of dicts if more than 1 field
        otherwise, a list
        """
        record = self.query.record
        field_count = record().count()
        # To populate with the fields from the last execute.
        # Array of dicts
        fields = []
        for cnt in range(field_count):
            fields.append( record().field(cnt).name() )
        
        results = []
        row = 0
        
        while self.query.next():
            if len(fields) > 1:
                row_result = {}
                for field in fields:                    
                    row_result[field] = record().value(field) 
                results.append(row_result)
                row+=1
            else:
                results.append(record().value(0))        
        return results
        
    def __query_execute(self, query, args=None):
        if args is not None:
            self.query.prepare(query)
            for arg in args:
                self.query.addBindValue(arg)
            self.query.exec_()
        else:
            # The execute() doesn't accept NoneTypes
            self.query.exec_(query)   
            
        err = self.query.lastError()
        if err.isValid():
            print err.text(),self.query.lastQuery()
            
    
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
            query = '''INSERT OR IGNORE INTO media 
                            VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
        elif self.db_type == "MYSQL":
            # To overcome the lack of an IGNORE
            query = '''
                    INSERT INTO media(  file_name, title,
                                        artist, album,
                                        year, genre,
                                        track, length,
                                        bitrate, added) 
                    SELECT ?,?,?,?,?,?,?,?,?,? FROM dual
                    WHERE NOT EXISTS (
                    SELECT * FROM media
                    WHERE file_name=?)
                    
                    '''
            meta[10] = meta[0]           
        self.__execute_write(query, meta)
        
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
        
    def get_artist(self,album):
        query = '''SELECT artist
                        FROM media
                        WHERE album=?
                        LIMIT 1'''
        self.__query_execute(query,(album,))
        result = self.__query_fetchall()
        return result
        
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
                        AND album=?
                        ORDER BY track'''
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
                        AND added>?
                        ORDER BY track'''
        self.__query_execute(query, args)
        result = self.__query_fetchall()
        return result
        
    def get_album_titles(self, album,filt=0):
        # TODO: order by track#
        query = '''SELECT DISTINCT title
                        FROM media
                        WHERE album=?
                        AND added>?'''
        self.__query_execute(query,(album, filt))
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

    def search_by_titandart(self, tit, art):
        args = (tit, art)
        query = '''SELECT file_name   
                    FROM media 
                    WHERE title=?
                    AND artist=?'''        
        self.__query_execute(query, args)
        result = self.__query_fetchall()
        return result
   
   #TODO: replace name to reflect new operation
    def drop_media(self):
        query = '''DELETE FROM media; DELETE FROM playcount; 
                    DELETE FROM last_playlist'''
        self.__execute_write(query)
        
    def restart_db(self,name=None):
        """
        Disconnects db and removes connection
        """
        name = name if name else self.name
        self.query.finish()
        CollectionDb.media_db.removeDatabase(name)
        self.__config_db() 

    def __connections(self):
        db_names = CollectionDb.media_db.connectionNames()
        return [str(db_names[cnt]) for cnt in range(len(db_names))]
    
    def shutdown(self):
        """
            Trying to shutdown cleanly. The Qt docs fail me.
        """
        conn_names = self.__connections()
        self.query.finish()
        del self.query
        for conn in conn_names:
            CollectionDb.media_db.database(conn).close()
            CollectionDb.media_db.removeDatabase(conn)
            
            
    def update_tag(self,fname, field, val):
        query = '''UPDATE media SET %s=? WHERE file_name=?''' % field
        self.__execute_write(query, (val,fname))
        
        
    def update_tags(self, fname, key_vals):
        """
            To be used once tag-editing is enabled
        """
        query = '''UPDATE media SET ? = ? WHERE file_name=?'''
        for key in key_vals.iterkeys():
            self.__execute_write(query, (key, key_vals[key]))
            
            
    def close_connection(self,name=None):
        name = name if name else self.name
        CollectionDb.media_db.database(name).close()
        CollectionDb.media_db.removeDatabase(name)
        
        
    def save_last_playlist(self, items):
        self.__query_execute("DELETE FROM last_playlist")
        query = '''INSERT INTO last_playlist
                    (id,file_name)
                    VALUES(?,?)'''        
        for item in items:
            self.__execute_write(query, (items.index(item), item))
        return
        
    def last_playlist(self):
        query = "SELECT file_name FROM last_playlist ORDER BY id"
        self.__query_execute(query)
        return self.__query_fetchall()
    
        
            