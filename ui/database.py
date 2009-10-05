from pysqlite2 import dbapi2 as sqlite
from os import mkdir, getenv, path
from time import localtime

#TODO: stats database

class MEDIA:
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
        tables = ['''CREATE TABLE IF NOT EXISTS media (
                file_name    TEXT ,
                track    UNSIGNED TINYINT(2),
                title   VARCHAR(50),
                artist  VARCHAR(50),
                album   VARCHAR(50),
                year    UNSIGNED SMALLINT(4),
                genre   VARCHAR(50),
                length  VARCHAR(5),
                bitrate UNSIGNED SMALLNT(4),
                rating  UNSIGNED TINYINT(1),
                playcount   UNSIGNED SMALLINT,
                added UNSIGNED MEDIUMINT(6),
                PRIMARY KEY (file_name) ON CONFLICT IGNORE
                )'''
                , 
                '''CREATE TABLE IF NOT EXISTS playlist (
                id   INT IDENTITY (1, 1),
                name    VARCHAR(20),
                file_name    TEXT,
                track  SMALLINT(3),
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
                list SMALLINT(3),
                PRIMARY KEY (id)
                )''']      
        
        for table in tables:
            self.media_curs.execute(table)
        
        
    def add_media(self, meta):
        """
        Here we add data into the media database
        """
        # A debug
        try:
            #FIXME: This doesn't seem to like unicode
            values = '"%s"' % '", "'.join(meta)
        except:
            print meta
            return
            
        cols = "file_name,track,title,artist,album,year,genre,length,bitrate"
        query = "INSERT INTO media (%s) VALUES (%s)" % (cols, values)
        
        try:
            self.media_curs.execute(query) 
            self.media_db.commit()    
        except:
            print "Database Failure: %s" % values
        

    def query_db(self, column):    
        """
        Ermm. Not sure what to put here yet.
        Maybe a testing thing
        """
        query = "SELECT DISTINCT %s FROM media" % column
        return self.queryfetchall(query)
        
    def searching(self, look_for, look_in, thing):
#        print look_for, look_in, thing
        query = '''SELECT DISTINCT %s FROM media
                            WHERE %s="%s"''' % (look_for, look_in, thing)
        return self.queryfetchall(query)
    
    def file_names(self, artist, album):
        query = '''SELECT DISTINCT file_name FROM media
                            WHERE artist="%s" AND album="%s"''' % (artist, album)
        return self.queryfetchall(query)
        
    def track_info(self, file_name):
        query = '''SELECT * FROM media
                            WHERE file_name="%s"''' % file_name
        return self.queryfetchall(query)
        
    def queryfetchall(self, query):
        self.media_curs.execute(query)
        return self.media_curs.fetchall()
