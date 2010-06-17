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


class CollectionDb:
    def __init__(self, mode="SQLITE", args=None):
        """
        Experimental. As sqlite and mysql are barely different trying to
        account for the differences
        """
        self.db_type = mode
        if mode == "SQLITE":
            from sqlite3 import dbapi2 as sqlite
            import os
            
            app_dir = "%s/.gereqi/" % os.getenv("HOME")
            db_loc = "%smedia.db" % app_dir
            if os.path.exists(app_dir) is False:
                os.mkdir(app_dir)
            self.media_db = sqlite.connect(db_loc)
            self.media_curs = self.media_db.cursor()        
#            self.__pragma()
        
        elif mode == "MYSQL":
            import MySQLdb

            self.media_db = MySQLdb.connect(host=args["hostname"],
                                    user=args["username"],
                                    passwd=args["password"],
                                    db=args["dbname"])
        
        self.__setup_tables()
        
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
            
    # FIXME: HACK ALERT!!!!!!!!!!
    def __setup_tables2(self):
        """
        For some reason you cannot use
        IF NOT EXISTS after you've dropped 
        the table and commited it
        """
        if self.db_type == "SQLITE":
            table = '''CREATE TABLE media (
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
        elif self.db_type == "MYSQL":
            table = '''CREATE TABLE media (
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
                                ) DEFAULT CHARSET=utf8'''
        self.__query_execute(table)
            
    def __query_process(self, query, args):
        if self.db_type == "MYSQL":
            now =  query.replace("?", '''"%s"''')
            if args is None:
                return now
            else:
                fin = now % args
                return fin
        elif self.db_type == "SQLITE":
            return query
            
    def __query_fetchone(self, query, args=None):
        result = self.__query_execute(self.__query_process(query, args), args)
        if self.db_type == "MYSQL":
            return self.media_db.store_result().fetch_row()
        return self.media_curs.fetchone()
            
    def __query_fetchall(self, query, args=None):
        result = self.__query_execute(self.__query_process(query, args), args)
        if self.db_type == "MYSQL":
            r = self.media_db.store_result()
            return r.fetch_row(maxrows=0)
        return self.media_curs.fetchall()
        
    def __query_execute(self, query, args=None):
        if self.db_type == "SQLITE":
            if args is not None:
                self.media_curs.execute(query, args)
            else:
                # The execute() doesn't accept NoneTypes
                self.media_curs.execute(query)                 
        elif self.db_type == "MYSQL":
                self.media_db.query(query)
    
    def __execute_write(self, query, args=None):
        if self.db_type == "SQLITE":
            self.__query_execute(query, args)
        elif self.db_type == "MYSQL":
            self.media_db.query(self.__query_process(query, args))
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
        artists = [art[0] for art in self.__query_fetchall(query)]
        return artists
        
    def get_artists_timed(self, filt):
        query = '''SELECT DISTINCT artist 
                            FROM media
                            WHERE added>?'''
        artists = [art[0] for art  in self.__query_fetchall(query, (filt, ))]
        return artists
        
    def get_albums(self, artist):
        args = (artist, )
        query = '''SELECT DISTINCT album 
                            FROM media
                            WHERE artist=?'''
                            
        albums = [alb[0] for alb in self.__query_fetchall(query, args)]
        return albums
        
    def get_albums_timed(self, artist, filt):
        args = (artist, filt)
        query = '''SELECT DISTINCT album   
                            FROM media
                            WHERE artist=?
                            AND added>?'''
        albums = [alb[0] for alb in self.__query_fetchall(query, args)]
        return albums
        
    def get_albums_all(self):
        query = '''SELECT DISTINCT album
                        FROM media'''
        return [alb[0] for alb in self.__query_fetchall(query)]

    def get_albums_all_timed(self, filt):
        query = '''SELECT DISTINCT album
                        FROM media   
                        WHERE added>?'''
        return [alb[0] for alb in self.__query_fetchall(query, (filt, ))]
        
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
        
    def get_album_file(self, album, title):
        args = (album, title)
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=?
                        AND title=?'''
        return self.__query_fetchall(query, args)[0][0]
        
    def get_album_files(self, album):
        args = (album, )
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=?'''
        return [title[0] for title in self.__query_fetchall(query, args)]
        
    def get_album_files_timed(self, album, filt):
        args = (album, filt)
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=?
                        AND added>?'''
        return [title[0] for title in self.__query_fetchall(query, args)]
        
    def get_artists_files(self, artist):
        args = (artist, )
        query = '''SELECT DISTINCT file_name 
                            FROM media
                            WHERE artist=?'''
        return [trk[0] for trk in self.__query_fetchall(query, args)]
                        
    def get_titles(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT title,track 
                        FROM media 
                        WHERE artist=?
                        AND album=?'''
        return self.__query_fetchall(query, args)

    def get_titles_timed(self, artist, album, filt):
        args = (artist, album, filt)
        query = '''SELECT DISTINCT title,track 
                        FROM media 
                        WHERE artist=?
                        AND album=?
                        AND added>?'''
        return self.__query_fetchall(query, args)
        
    def get_album_titles(self, album):
        args = (album, )
        query = '''SELECT DISTINCT title
                        FROM media
                        WHERE album=?'''
        return [title[0] for title in self.__query_fetchall(query, args)]
        
    def get_album_files_timed(self, album, filt):
        args = (album, filt)
        query = '''SELECT DISTINCT title
                        FROM media
                        WHERE album=?
                        AND added>?'''
        return [title[0] for title in self.__query_fetchall(query, args)]
        
    def get_info(self, file_name):
        query = '''SELECT * 
                        FROM media 
                        WHERE file_name=?'''
        result = self.__query_fetchall(query, (file_name, ))
        if len(result) > 0:
            return result[0]
        
    def playlist_add(self, *params):
        query = '''INSERT INTO playlist 
                            VALUES (?,?)'''
        self.__query_execute(query, params)
        
    def playlist_list(self):
        query = '''SELECT DISTINCT name 
                            FROM playlist'''
        playlists = [play[0] for play in self.__query_fetchall(query)]
        return playlists
        
    def playlist_tracks(self, name):
        query = '''SELECT file_name 
                            FROM playlist
                            WHERE name=?'''
        tracks = [track[0] for track in self.__query_fetchall(query, (name, ))]
        return tracks
    
    def playlist_delete(self, name):
        query = '''DELETE FROM playlist
                        WHERE name=?'''
        self.__query_execute(query, (name, ))

    def search_by_titandart(self, art, tit):
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=?
                        AND title=?'''        
        files = [fi[0] for fi in self.__query_fetchall(query, (art, tit))]
        return files
   
    def drop_media(self):
        query = '''DROP TABLE media'''
        self.__execute_write(query)
        self.__setup_tables2()
        
