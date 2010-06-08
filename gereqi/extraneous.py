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


import os
from database import Media

from webinfo import Webinfo

class Extraneous:
    """
    Miscellaneous functions that have no real place to
    go but are used in various Classes.
    """
    def __init__(self, parent=None):
        self.ui_main = parent
        
    def __filenamer(self, *params):
        things = []
        exc = '''!,.%%$&(){}[]/"'''
        for item in params:
            result = filter(lambda x : x not in exc, item.lower())
            result = result.replace(" ", "_")
            things.append(result)
        return "%s-%s" % tuple(things)
        
       
    def check_source_exists(self, fname):
        """
        Checks whether if a track exists on drives.
        If not, it removes the track from the database.
        """
        if os.path.exists(fname) is True:
            return True
        else:
            database = Media()
            print("WARNING: removed non-existing track, %s, from database" % fname)
            database.delete_track(fname)
            

    def get_cover_source(self, artist, album):
        cover_dir = "%s/.gereqi/album-art/" % os.environ["HOME"]
        cover = "%s%s.jpg" % (cover_dir, self.__filenamer(artist, album))
        print cover
        if os.path.exists(cover_dir) is False:
            os.mkdir(cover_dir)
        elif os.path.exists(cover) is True:
            return cover
        else:                        
            info = Webinfo()
            img = info.get_info("cover", artist, album)            
            if img is not None:
                now = open(cover, "wb")
                now.write(img)
                return cover
