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


class MysqlDb:
    def __init__(self, args):
        import MySQLdb
        
        self.media_db = MySQLdb.connect(host=args["hostname"],
                                user=args["username"],
                                passwd=args["password"],
                                db=args["dbname"])
        self.media_curs = self.media_db.cursor()
        self.__setup()

    def __setup(self):                
        tables = ['''CREATE TABLE IF NOT EXISTS media (
                            file_name    TEXT ,
                            title   VARCHAR(50),
                            artist  VARCHAR(50),
                            album   VARCHAR(50),
                            year   SMALLINT(4),
                            genre  VARCHAR(20),
                            track  TINYINT(2) UNSIGNED,
                            length  VARCHAR(5),
                            bitrate SMALLINT(4),
                            added MEDIUMINT(6) UNSIGNED ,
                            playcount SMALLINT(5),
                            rating TINYINT(1)
                            ) DEFAULT CHARSET=utf8''', 
                        '''CREATE TABLE IF NOT EXISTS playlist (
                            name TEXT,
                            file_name TEXT
                            ) DEFAULT CHARSET=utf8''']      

        for table in tables:
            self.media_curs.execute(table)
            
    def __query_fetchone(self, query, args=None):
        self.__query_execute(query, args)
        return self.media_curs.fetchone()
            
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
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        self.__query_execute(query, meta)
        
    def get_artists(self):
        query = '''SELECT DISTINCT artist
                        FROM media'''
        artists = [art[0] for art in self.__query_fetchall(query)]
        return artists
        
    def get_artists_timed(self, filt):
        print filt, type(filt)
        query = '''SELECT DISTINCT artist 
                            FROM media
                            WHERE added>%d'''
        artists = [art[0] for art  in self.__query_fetchall(query, (filt, ))]
        return artists
        
    def get_albums(self, artist):
        args = (artist, )
        query = '''SELECT DISTINCT album 
                            FROM media
                            WHERE artist=%s'''
                            
        albums = [alb[0] for alb in self.__query_fetchall(query, args)]
        return albums
        
    def get_albums_timed(self, artist, filt):
        args = (artist, filt)
        query = '''SELECT DISTINCT album   
                            FROM media
                            WHERE artist=%s
                            AND added>%d'''
        albums = [alb[0] for alb in self.__query_fetchall(query, args)]
        return albums
        
    def get_albums_all(self):
        query = '''SELECT DISTINCT album
                        FROM media                  
                    '''
        return [alb[0] for alb in self.__query_fetchall(query)]

    def get_albums_all_timed(self, filt):
        query = '''SELECT DISTINCT album
                        FROM media   
                        WHERE added>%d'''
        return [alb[0] for alb in self.__query_fetchall(query, (filt, ))]
        
    def get_files(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=%s
                        AND album=%s'''
        files = [fnow[0] for fnow in self.__query_fetchall(query, args)]
        return files
        
    def get_file(self, artist, album, title):
        args = (artist, album, title)
        query = '''SELECT DISTINCT file_name 
                        FROM media 
                        WHERE artist=%s
                        AND album=%s
                        AND title=%s'''
        return self.__query_fetchall(query, args)[0][0]
        
    def get_album_file(self, album, title):
        args = (album, title)
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=%s
                        AND title=%s'''
        return self.__query_fetchall(query, args)[0][0]
        
    def get_album_files(self, album):
        args = (album, )
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=%s'''
        return [title[0] for title in self.__query_fetchall(query, args)]
        
    def get_album_files_timed(self, album, filt):
        args = (album, filt)
        query = '''SELECT DISTINCT file_name
                        FROM media
                        WHERE album=%s
                        AND added>%d'''
        return [title[0] for title in self.__query_fetchall(query, args)]
        
    def get_artists_files(self, artist):
        args = (artist, )
        query = '''SELECT DISTINCT file_name 
                            FROM media
                            WHERE artist=%s'''
                            
        return [trk[0] for trk in self.__query_fetchall(query, args)]
                        
    def get_titles(self, artist, album):
        args = (artist, album)
        query = '''SELECT DISTINCT title,track 
                        FROM media 
                        WHERE artist=%s
                        AND album=%s'''
        return self.__query_fetchall(query, args)

    def get_titles_timed(self, artist, album, filt):
        args = (artist, album, filt)
        query = '''SELECT DISTINCT title,track 
                        FROM media 
                        WHERE artist=%s
                        AND album=%s
                        AND added>%d'''
        return self.__query_fetchall(query, args)
        
    def get_album_titles(self, album):
        args = (album, )
        query = '''SELECT DISTINCT title
                        FROM media
                        WHERE album=%s'''
        return [title[0] for title in self.__query_fetchall(query, args)]
        
    def get_album_files_timed(self, album, filt):
        args = (album, filt)
        query = '''SELECT DISTINCT title
                        FROM media
                        WHERE album=%s
                        AND added>%d'''
        return [title[0] for title in self.__query_fetchall(query, args)]
        
    def get_info(self, file_name):
        query = '''SELECT * 
                        FROM media 
                        WHERE file_name=%s'''
        result = self.__query_fetchall(query, (file_name, ))
        if len(result) > 0:
            return result[0]
        
    def delete_track(self, fname):
        args = (fname, )
        query = '''DELETE FROM media
                        WHERE file_name=%s'''
        self.__query_execute(query, args)
    
    def playlist_add(self, *params):
        query = '''INSERT INTO playlist 
                            VALUES (%s,%s)'''
        self.__query_execute(query, params)
        
    def playlist_list(self):
        query = '''SELECT DISTINCT name 
                            FROM playlist'''
        playlists = [play[0] for play in self.__query_fetchall(query)]
        return playlists
        
    def playlist_tracks(self, name):
        query = '''SELECT file_name 
                            FROM playlist
                            WHERE name=%s'''
        tracks = [track[0] for track in self.__query_fetchall(query, (name, ))]
        return tracks
    
    def playlist_delete(self, name):
        query = '''DELETE FROM playlist
                        WHERE name=%s'''
        self.__query_execute(query, (name, ))

    def inc_count(self, cnt, fname):
        query = '''UPDATE media
                        SET playcount=%s
                        WHERE file_name=%s'''
        self.__query_execute(query, (cnt, fname))
        
    def search_by_titandart(self, art, tit):
        query = '''SELECT DISTINCT file_name   
                        FROM media 
                        WHERE artist=%s
                        AND title=%s'''        
        files = [fi[0] for fi in self.__query_fetchall(query, (art, tit))]
        return files
        
#FIXME: fix this horrible mess
class SqliteDb:
    def __init__(self, parent=None):
        """
        The table creations perform every class instance(?)
        but only creates them if they don't already exist. This means 
        to add extra columns to an existing table te database file 
        has to be deleted.
        """
        from sqlite3 import dbapi2 as sqlite
        import os
        
        app_dir = "%s/.gereqi/" % os.getenv("HOME")
        db_loc = "%sgereqi.db" % app_dir
        
        # Nowhere to put db
        if os.path.exists(app_dir) is False:
            os.mkdir(app_dir)
        self.media_db = sqlite.connect(db_loc)
        self.media_curs = self.media_db.cursor()        
        self.__setup_tables()
        self.__pragma()
        
    def __setup_tables(self):
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
                added UNSIGNED MEDIUMINT(6),
                playcount SMALLINT(5),
                rating TINYINT(1),
                PRIMARY KEY (file_name) ON CONFLICT IGNORE
                )'''
                , 
                '''CREATE TABLE IF NOT EXISTS playlist (
                name TEXT,
                file_name TEXT
                )''']      
        
        for table in tables:
            self.__query_execute(table)
            
    def __query_fetchone(self, query, args=None):
        self.__query_execute(query, args)
        return self.media_curs.fetchone()
            
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
        
    def __pragma(self):
        """
        This command will cause SQLite to not wait on data to reach the disk surface, 
        which will make write operations appear to be much faster. 
        But if you lose power in the middle of a transaction, your database file might go corrupt.
        """
        query = '''PRAGMA synchronous = OFF'''
        self.__query_execute(query)

    def add_media(self, meta):
        """
        Here we add data into the media database
        """
        query = '''INSERT INTO media 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''
        self.__query_execute(query, meta)
        
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
                        WHERE added>?
                    '''
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
        files = [fi[0] for fi in self.__query_fetchall(query, (art, tit))]
        return files
   
