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

from sqlite3 import dbapi2 as sqlite
import os

CFG_DIR = "%s/.gereqi" % os.environ["HOME"]
SETSFILE = "%s/settings.db" % CFG_DIR

if os.path.exists(CFG_DIR) is False:
    os.mkdir(CFG_DIR)

class Settings:
    def __init__(self):
        self.settings_db = sqlite.connect(SETSFILE)
        self.settings_curs = self.settings_db.cursor()
        self.__setup_tables()  
        
    def __setup_tables(self):
            tables = [''' CREATE TABLE IF NOT EXISTS interface (
                        tag TEXT,
                        value TEXT) ''', 
                      '''CREATE TABLE IF NOT EXISTS database (
                        tag TEXT,
                        value TEXT) ''', 
                      '''CREATE TABLE IF NOT EXISTS collection (
                        tag TEXT,
                        value TEXT)''']
            for table in tables:
                self.__query_execute(table)
                
    def __query_fetchone(self, query, args=None):
        self.__query_execute(query, args)
        return self.settings_curs.fetchone()
            
    def __query_fetchall(self, query, args=None):
        self.__query_execute(query, args)
        return self.settings_curs.fetchall()
                        
    def __query_execute(self, query, args=None):
        if args is not None:
            self.settings_curs.execute(query, args)
        else:
            self.settings_curs.execute(query) 
        self.settings_db.commit() 
        
    def add_collection_setting(self, *args):
        query = '''INSERT INTO collection 
                    VALUES (?,?)'''
        self.__query_execute(query, args)
        
    def add_database_setting(self, *args):
        query = '''INSERT INTO database 
                    VALUES (?,?)'''
        self.__query_execute(query, args)        
        
    def add_interface_setting(self, *args):
        query = '''INSERT INTO interface 
                    VALUES (?,?)'''
        self.__query_execute(query, args)
        
    def get_collection_settings(self):
        query = '''SELECT tag,value
                    FROM collection'''
        return self.__query_fetchall(query)

    def get_database_settings(self):
        query = '''SELECT tag,value
                    FROM database'''
        return self.__query_fetchall(query)
        
    def get_interface_settings(self):
        query = '''SELECT tag,value
                    FROM interface'''
        return self.__query_fetchall(query)
        
    def get_collection_setting(self, tag):
        query = '''SELECT value
                    FROM collection
                    WHERE tag=?'''
        result = self.__query_fetchone(query,(tag,))
       
        if result is not None:
            if tag != ("include" or "exclude"):
                return result[0]
            else:
                return result

    def get_collection_dirs(self, tag):
        query = '''SELECT value
                    FROM collection
                    WHERE tag=?'''
        return [str(val[0]) for val in self.__query_fetchall(query, (tag, ))]

    def get_database_setting(self, tag):
        query = '''SELECT value
                    FROM database
                    WHERE tag=?'''
        result = self.__query_fetchone(query, (tag, ))
        if result is not None:
            return result[0]
        
    def get_interface_setting(self, tag):
        query = '''SELECT value
                    FROM interface
                    WHERE tag=?'''
        result = self.__query_fetchone(query, (tag, ))
        if result is not None:
            return result[0]
        
    #FIXME: fix this ungodly mess

    def drop_collection(self):
        # If I use the IF NOT EXIST in the CREATE the collection TABLE
        # doesn't appear to actually exist
        # Need to do this as we may want to remove an entry, no primary key
        queries= ['''DROP TABLE collection''', 
                    '''CREATE TABLE collection (
                        tag TEXT,
                        value TEXT)''']
                    
        for query in queries:
            self.__query_execute(query)
        
    def drop_database(self):
        queries= ['''DROP TABLE database''', 
                    '''CREATE TABLE database (
                        tag TEXT,
                        value TEXT)''']
                    
        for query in queries:
            self.__query_execute(query)
            
    def drop_interface(self):
        queries= ['''DROP TABLE interface''', 
                    '''CREATE TABLE interface (
                        tag TEXT,
                        value TEXT)''']
                    
        for query in queries:
            self.__query_execute(query)
