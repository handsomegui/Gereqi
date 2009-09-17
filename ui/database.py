#from PyQt4.QtSql import  QSqlDatabase
from pysqlite2 import dbapi2 as sqlite
from os import mkdir, getenv, path, remove

    
class media:
    def __init__(self):

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
                filename    TEXT PRIMARY KEY ON CONFLICT IGNORE,
                track    TINYINT(2),
                title   VARCHAR(50),
                artist  VARCHAR(50),
                album   VARCHAR(50),
                year    SMALLINT(4),
                genre   VARCHAR(50)
                )
                ''')
                
    def add_media(self, p):
        """
        Here we add data into the media database
        """
        values = ''' "%s","%s","%s","%s", "%s","%s","%s" ''' % (p[0], p[1], p[2], p[3], p[4], p[5], p[6])
        cols = "filename,track,title,artist,album,year,genre"
        query = "INSERT INTO media (%s) VALUES (%s)" % (cols, values)
        
        self.mediaCurs.execute(query) 
        self.mediaDB.commit()    
        
    def lenDB(self):
        primary = "SELECT filename FROM media"
        primary = self.mediaCurs.execute(primary)
        primary =  self.mediaCurs.fetchall()
        print len(primary)
        
    def queryDB(self, column):    
        """
        Ermm. Not sure what to put here yet.
        Maybe a testing thing
        """
        query = "SELECT DISTINCT %s FROM media" % column
        self.mediaCurs.execute(query)
        return self.mediaCurs.fetchall()
        
    def albums(self, artist):
        query = '''SELECT DISTINCT album FROM media
                            WHERE artist="%s"''' % artist
        self.mediaCurs.execute(query)
        return self.mediaCurs.fetchall()
    
    def closeDBs(self):
        #TODO: not implemented yet
        print "Called when shutting down to cleanly close databases."
        self.mediaDB.commit()
        
    

