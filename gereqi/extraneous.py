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


from os import path
from database import Media

class Extraneous:
    """
    Miscellaneous functions that have no real place to
    go but are used in various Classes.
    """
    def __init__(self):
        return
        
       
    def check_source_exists(self, fname):
        """
        Checks whether if a track exists on drives.
        If not, it removes the track from the database.
        """
        if path.exists(fname) is True:
            return True
        else:
            db = Media()
            print("WARNING: removed non-existing track, %s, from database" % fname)
            db.delete_track(fname)
