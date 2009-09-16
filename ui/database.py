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
#        remove(self.mediaDB)
        
        if not path.exists(appDir):
            print "need to make a folder"
            mkdir(appDir)

        self.mediaDB = sqlite.connect(self.mediaDB)
        self.mediaCurs = self.mediaDB.cursor()
        
        # YEAR() data type causes a crash
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
        Not sure what'll happen when the same filename comes up
        more than once.
        """
        # Next is a bodge
        values = ''' "%s","%s","%s","%s", "%s","%s","%s" ''' % (p[0], p[1], p[2], p[3], p[4], p[5], p[6])
        cols = "filename,track,title,artist,album,year,genre"
# Here is probably a good place to put in a  check to see if the filename, PRIMARY KEY, already exists
# Of course this would prevent tags/metadata being updated since first INSERT.
        query = "INSERT INTO media (%s) VALUES (%s)" % (cols, values)
        
        # The below query is what i'd prefer for additions to database. It won't work as i've no idea how to
        # make it so.
        '''INSERT INTO media (%s) VALUES (%s)
            WHERE NOT EXISTS( 
                          SELECT filename 
                          FROM media 
                          )'''
        
#        if not self.checkDB(p[0]):
        self.mediaCurs.execute(query) 
        self.mediaDB.commit()    
        
    def lenDB(self):
        primary = "SELECT filename FROM media"
        primary = self.mediaCurs.execute(primary)
        primary =  self.mediaCurs.fetchall()
        print len(primary)
        
    def checkDB(self, fileName):
        """
        To check that the file is not already present in database.
        May replace with an UPDATE media THINGS WHERE
        """
        primary = "SELECT filename FROM media"
        primary = self.mediaCurs.execute(primary)
        # below creates a list,good, but for some reason there's a trailing comma in each item
        primary =  self.mediaCurs.fetchall()
        
        # This for loop is not ideal in the slighest, but it works. Fixes the issue mentioned above
        # Prefer if I could use "return fileName in primary"
        #FIXME:This really needs to be better. Although a rescan of a fully created  database
        # it is still really slow. At least it maxes out one core.
        for item in primary:
            # If fileName already present in database
            if item[0] == fileName:
#                print "Here"
                return True
                break
        return False

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
        


