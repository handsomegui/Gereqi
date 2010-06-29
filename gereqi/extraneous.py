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


from os import environ as getenv
from PyQt4.QtCore import QDir, QString, QFile, QIODevice

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
        excludes = '''!,.%%$&(){}[]/"'''
        for item in params:
            for ch in excludes:
                item.remove(ch)
            item.replace(" ", "_")
            things.append(item)
        # FIXME: funny unicode characters should have been removed/encoded by now
        result = QString("%1-%2").arg(things[0]).arg(things[1])
        return result
        
       
    def check_source_exists(self, fname):
        """
        Checks whether if a track exists on drives.
        If not, it removes the track from the database.
        """
        if QDir(fname).exists() is True:
            return True
        else:
            database = Media()
            print("WARNING: removed non-existing track, %s, from database" % fname)
            database.delete_track(fname)
            

    def get_cover_source(self, artist, album, check=True):
        cover_dir = QString("%1/.gereqi/album-art/").arg(getenv["HOME"])
        cover = QString("%1%2.jpg").arg(cover_dir).arg(self.__filenamer(artist, album))
        
        if check is True:
            if QDir(cover_dir).exists() is False:
                QDir().mkdir(cover_dir)
            elif QFile(cover).exists() is True:
                return QString("file://%1").arg(cover)
            else:                        
                web_info = Webinfo()
                img = web_info.get_info("cover", artist, album)
                if img is not None:
                    now = QFile(cover)
                    now.open(QIODevice.WriteOnly)
                    now.writeData(img)
                    now.close()
                    return QString("file://%1").arg(cover)
        else:
            return QString("file://%1").arg(cover)
