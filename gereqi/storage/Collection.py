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

from . Settings import Settings
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
        CollectionDb.media_db = None
        self.close_connection()
        
    def __config_db(self):
        sets_db = Settings()
        app_dir = "%s/.gereqi/" % os.getenv("HOME")
        db_loc  = "%smedia.db" % app_dir
        if QDir(app_dir).exists is False:
            QDir().mkdir(app_dir)                
        CollectionDb.media_db = QSqlDatabase.addDatabase("QSQLITE", self.name)
        CollectionDb.media_db.setDatabaseName(db_loc)
        
        ok = CollectionDb.media_db.open()
        if ok is True:
            self.query = QSqlQuery(CollectionDb.media_db)
            self.__pragma()
            self.__setup_tables()
        else:
            err = self.media_db.lastError().text()
            raise StandardError(err)
        
    def __setup_tables(self):
        for table in Tables.Sqlite().tables:
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
                    row_result[unicode(field)] = unicode(record().value(field).toString()) 
                results.append(row_result)
                row+=1
            else:
                results.append(unicode(record().value(0).toString()))        
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
        
#===============================================================================
# 
#===============================================================================
    def add_media(self, meta):
        """
        Here we add data into the media database
        """
        query = '''INSERT OR IGNORE INTO media 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)'''          
        self.__execute_write(query, meta)
        
    def inc_count(self, timestamp, fname):
        """
        Doesn't change count directly but by adding another
        row into DB with a file_name the row_count (play count)
        would increase
        """
        query = '''SELECT * FROM playcount
                    WHERE file_name=?'''
        self.__query_execute(query,(fname,))
        go = self.__query_fetchall() 
             
        if len(go) < 1: 
            query = '''INSERT INTO playcount (file_name,count) VALUES(?,1)'''
            self.__execute_write(query, (fname,))
        else:
            query = '''UPDATE playcount SET count=count+1 WHERE id=?'''
            self.__execute_write(query, (go[0]['id'],) )
        
    def delete_track(self, fname):
        args = (fname, )
        query = '''DELETE FROM media WHERE file_name=?'''
        self.__execute_write(query, args)
        
    def get_artist(self,album):
        query = '''SELECT artist
                        FROM media
                        WHERE album=?
                        LIMIT 1'''
        self.__query_execute(query,(album,))
        result = self.__query_fetchall()
        return result
        
    def get_artists(self, time_filt=0,filt=''):
        filt = "%%%s%%" % filt
        query = '''SELECT DISTINCT artist 
                    FROM media
                    WHERE added > ? AND artist LIKE ?
                    ORDER BY lower(artist)'''
        self.__query_execute(query, (time_filt, filt))
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
        
    def get_albums_all(self, time_filt=0, filt=''):
        filt = "%%%s%%" % filt
        query = '''SELECT DISTINCT album,artist
                        FROM media   
                        WHERE added>?
                        AND album LIKE ?
                        ORDER BY lower(album)'''
        self.__query_execute(query, (time_filt, filt))
        result = self.__query_fetchall()
        return result
    
    def get_album_count(self,album):
        query = '''SELECT DISTINCT artist
                    FROM media
                    WHERE album=?'''
        self.__query_execute(query, (album,))
        return len(self.__query_fetchall())
        
    def get_files(self, artist, album,filt=0):
        args = (artist, album, filt)
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=?
                        AND album=?
                        AND added>?
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
        
    def get_file(self, artist, album, title,filt=0):
        args = (artist, album, title,filt)
        query = '''SELECT DISTINCT file_name 
                        FROM media 
                        WHERE artist=?
                        AND album=?
                        AND title=?
                        AND added>?'''
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
        self.__query_execute(query, (album, filt))
        result = self.__query_fetchall()
        return result
        
       
    def get_artists_files(self, artist,filt=0):
        query = '''SELECT DISTINCT file_name 
                            FROM media
                            WHERE artist=?
                            AND added>?'''
        self.__query_execute(query, (artist, filt))
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
                        AND added>
                        ORDER BY track?'''
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
        
    # Can't think of a better name. I wanted to overload get_info
    def get_info_from_info(self,artist,album,title):
        query = '''SELECT file_name,year,genre,track,length,bitrate,added,rating
                    FROM media
                    WHERE artist=? AND album=? AND title=?'''
        
        self.__query_execute(query, (artist,album,title))
        result = self.__query_fetchall()
        if len(result) > 0:
            return result[0]
        
    def playlist_add(self, *params):
        query = '''INSERT OR REPLACE INTO playlist (?,?)'''
        self.__execute_write(query, params)
        
    def playlist_list(self):
        query = '''SELECT DISTINCT name 
                    FROM playlist'''
        self.__query_execute(query)
        result = self.__query_fetchall()
        return result
        
    def playlist_tracks(self, name):
        query = '''SELECT DISTINCT file_name 
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
        queries = [ "DELETE FROM media;", 
                    "DELETE FROM playcount;", 
                    "DELETE FROM last_playlist;", 
                    "DELETE FROM playlist;"]
        for q in queries:
            self.__execute_write(q)
        
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
    
    def top_tracks(self,amount=10):
        query = '''SELECT * FROM media 
                    WHERE EXISTS ( 
                        SELECT file_name FROM playcount 
                        WHERE playcount.file_name = media.file_name) 
                        LIMIT ?
                    '''
                   
        self.__query_execute(query, (amount,))
        return self.__query_fetchall()

    def unplayed(self):
        query = '''SELECT * FROM media 
                    WHERE NOT EXISTS ( 
                        SELECT file_name FROM playcount 
                        WHERE playcount.file_name = media.file_name) 
                        LIMIT 10
                    '''
        self.__query_execute(query)
        return self.__query_fetchall()
        
    def all_files(self):
        """
        Return all the filenames of tracks in the DB
        """
        query = ''' SELECT file_name FROM media'''
        self.__query_execute(query)
        return self.__query_fetchall()            
