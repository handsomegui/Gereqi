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
# 

# FIXME: mysql password is saved plain-text. Salt them? 
"""
Saves the application's settings in an .ini-like
file at '~/.gereqi/config'
""" 

import ConfigParser
import os


CFG_DIR = "%s/.gereqi" % os.environ["HOME"]
SETSFILE = "%s/config" % CFG_DIR

# Typically needed on 1st-run of program
if os.path.exists(CFG_DIR) is False: 
    os.mkdir(CFG_DIR)


class Settings:
    # Need to be the same for all that use it
    config = ConfigParser.ConfigParser()
    
    def __init__(self):
        self.__read_config()
    
    def __read_config(self):
        self.config.read(SETSFILE)
        
    def __section_exists(self, section):
        sects = self.config.sections()
        return section in sects
    
    def __option_exists(self, section, option):
        opts = self.config.options(section) 
        return option in opts
    
    def __write_config(self):
        fnow = open(SETSFILE, "wb")
        self.config.write(fnow)
        fnow.close()
        self.__read_config()
    
    def add_collection_setting(self, opt, val):
        if self.__section_exists("collection") is False:
            self.config.add_section("collection")        
        self.config.set("collection", opt, val)
        self.__write_config()
        
    def add_database_setting(self, opt, val):
        if self.__section_exists("database") is False:
            self.config.add_section("database")        
        self.config.set("database", opt, val)      
        self.__write_config()
        
    def add_interface_setting(self, opt, val):
        if self.__section_exists("interface") is False:
            self.config.add_section("interface")        
        self.config.set("interface", opt, val)  
        self.__write_config()        
    
        
    def get_collection_setting(self, opt):
        if self.__section_exists("collection") is True:
            options = self.config.options("collection")
            if opt in options:
                # The directories are csv
                return self.config.get("collection",opt)

    def get_database_setting(self, opt):
        if self.__section_exists("database") is True:
            options = self.config.options("database")
            if opt in options:
                return self.config.get("database",opt)
        
    def get_interface_setting(self, opt): 
        if self.__section_exists("interface") is True:
            options = self.config.options("interface")
            if opt in options:
                return self.config.get("interface",opt)
            
    def default_db(self):
        """
            used in case of DB config errors
        """
        self.add_database_setting("type", "SQLITE")

