#from PyQt4.QtSql import  QSqlDatabase
from pysqlite2 import dbapi2 as sqlite
from os import mkdir, getenv, path, remove

    
class media:
    def __init__(self):

        # Again, despite being boilerplate, does fuck all.
        # PyQt's databasing fails again. Switching to pysqlite
#        self.db = QSqlDatabase()
#        self.db.addDatabase("QSQLITE") 
#        self.db.setDatabaseName("/tmp/test.db")
#        ok = self.db.open()
#        if ok:
#            print "OK"

        appDir = getenv("HOME")
        appDir = "%s/.amaroq/" % appDir
        self.mediaDB = "%samaroq.db" % appDir
        
        # For testing purposes
        remove(self.mediaDB)
        
        if not path.exists(appDir):
            print "need to make a folder"
            mkdir(appDir)

        self.mediaDB = sqlite.connect(self.mediaDB)
        self.mediaCurs = self.mediaDB.cursor()
        
        # YEAR() data type causes a crash
        # using filename as PRIMARY KEY to prevent multiple entries
        self.mediaCurs.execute('''
            CREATE TABLE IF NOT EXISTS media (
                filename    TEXT PRIMARY KEY,
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
        Not sure what'll happen when the same filename comes up
        more than once.
        """
        # Next is a bodge
        values = ''' "%s","%s","%s","%s", "%s","%s","%s" ''' % (p[0], p[1], p[2], p[3], p[4], p[5], p[6])
        
# Here is probably a good place to put ina  check to see if the filename, PRIMARY KEY, already exists
# Of course this would prevent tags/metadata being updated since first INSERT.
        query = "INSERT INTO media (filename,track,title,artist,album,year,genre) VALUES (%s)" % values

        self.mediaCurs.execute(query) 
        self.mediaDB.commit()    
#        self.mediaDB()
        
        
    def queryDB(self):    
        """
        Ermm. Not sure what to put here yet.
        Maybe a testing thing
        """
        self.mediaCurs.execute("SELECT * FROM history")
        print self.mediaCurs.fetchall()
    
    def closeDBs(self):
        #TODO: not implemented yet
        print "Called when shutting down to cleanly close databases."
        self.mediaDB.commit()
        


