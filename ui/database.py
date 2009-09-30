#from PyQt4.QtSql import  QSqlDatabase
from pysqlite2 import dbapi2 as sqlite
from os import mkdir, getenv, path, remove

#TODO: stats database

class media:
    def __init__(self):
        """
        The table creations perform every class instance(?)
        but only creates them if they don't already exist. This means 
        to add extra columns to an existing table te database file amaroq.db
        has to be deleted.
        """
        appDir = getenv("HOME")
        appDir = "%s/.amaroq/" % appDir
        self.mediaDB = "%samaroq.db" % appDir
        
        if not path.exists(appDir):
            print "need to make a folder"
            mkdir(appDir)

        self.mediaDB = sqlite.connect(self.mediaDB)
        self.mediaCurs = self.mediaDB.cursor()
        
        # using filename as PRIMARY KEY to prevent multiple entries
        self.mediaCurs.execute('''
            CREATE TABLE IF NOT EXISTS media (
                filename    TEXT ,
                track    UNSIGNED TINYINT(2),
                title   VARCHAR(50),
                artist  VARCHAR(50),
                album   VARCHAR(50),
                year    UNSIGNED SMALLINT(4),
                genre   VARCHAR(50),
                length  VARCHAR(5),
                bitrate UNSIGNED TINYINT(4),
                rating  UNSIGNED TINYINT(1),
                playcount   UNSIGNED SMALLINT,
                PRIMARY KEY (filename) ON CONFLICT IGNORE
                )
                ''')
                
        self.mediaCurs.execute('''
            CREATE TABLE IF NOT EXISTS playlist (
                id   SMALLINT UNSIGNED IDENTITY (1, 1),
                name    VARCHAR(20),
                filename    TEXT,
                track  SMALLINT(3),
                PRIMARY KEY (id)
                )
                ''')
                
        self.mediaCurs.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                setting   TEXT,
                value   TEXT,
                PRIMARY KEY (setting) ON CONFLICT  REPLACE
                )
                ''')
                
        
    def add_media(self, p):
        """
        Here we add data into the media database
        """
        values = ''' "%s","%s","%s","%s", "%s","%s","%s","%s","%s"  ''' % (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]) #FIXME:ugly
        cols = "filename,track,title,artist,album,year,genre,length,bitrate"
        query = "INSERT INTO media (%s) VALUES (%s)" % (cols, values)
        
        try:
            self.mediaCurs.execute(query) 
            self.mediaDB.commit()    
        except:
            print "Database Failure: %s" % values
        
    def lenDB(self):
        query = "SELECT filename FROM media"
        primary = self.queryfetchall(query)
        print len(primary)
        
    def queryDB(self, column):    
        """
        Ermm. Not sure what to put here yet.
        Maybe a testing thing
        """
        query = "SELECT DISTINCT %s FROM media" % column
        return self.queryfetchall(query)
        
    def searching(self, looknFr, looknIn, thing):
#        print looknFr, looknIn, thing
        query = '''SELECT DISTINCT %s FROM media
                            WHERE %s="%s"''' % (looknFr, looknIn, thing)
        return self.queryfetchall(query)
    
    def filenames(self, artist, album):
        query = '''SELECT DISTINCT filename FROM media
                            WHERE artist="%s" AND album="%s"''' % (artist, album)
        return self.queryfetchall(query)
        
    def trackInfo(self, fileName):
        query = '''SELECT * FROM media
                            WHERE filename="%s"''' % fileName
        return self.queryfetchall(query)
        
    def closeDBs(self):
        #TODO: not implemented yet
        print "Called when shutting down to cleanly close databases."
        self.mediaDB.commit()
        
    
    def queryfetchall(self, query):
        self.mediaCurs.execute(query)
        return self.mediaCurs.fetchall()
