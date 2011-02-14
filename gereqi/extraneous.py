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


from PySide.QtCore import QDir, QFile, QIODevice
from os import environ as getenv
from os import path

from gereqi.information.webinfo import Webinfo



class Extraneous:
    """
    Miscellaneous functions that have no real place to
    go but are used in various Classes.
    """
    def __init__(self, parent=None):
        self.ui_main = parent
        
    def __filenamer(self, *params):
        things = []
        excludes = '''!,.%%$&(){}[]/"'''
        for item in params:
            for ch in excludes:
                item.replace(ch,'')
            item.replace(" ", "_")
            things.append(item)
        result = "%s-%s" % (things[0], things[1])
        return result

    def get_cover_source(self, artist, album, check=True,download=True):
        cover_dir = "%s/.gereqi/album-art/" % getenv["HOME"]
        fname = self.__filenamer(artist, album)
        fname = fname.replace('/','_')
        cover = "%s%s.jpg" % (cover_dir, fname)
        
        # Check=False just provides a filename creator. Used when track has
        # changed but not the album
        if check:
            # Place to save the covers doesn't exist
            if QDir(cover_dir).exists() is False:
                QDir().mkdir(cover_dir)
            
            if path.exists(cover):
                return "file://%s" % cover
            elif download == True:                        
                web_info = Webinfo()
                img = web_info.get_cover(artist, album)
                if img is not None:
                    now = open(cover, "wb")
                    now.write(img)
                    now.close()
                    return "file://%s" % cover
        else:
            return "file://%s" % cover
