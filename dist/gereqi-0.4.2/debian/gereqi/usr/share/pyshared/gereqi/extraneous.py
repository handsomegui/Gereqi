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


from PyQt4.QtCore import QDir, QString, QFile, QIODevice

from os import environ as getenv

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
        result = QString("%1-%2").arg(things[0]).arg(things[1])
        return result

    def get_cover_source(self, artist, album, check=True):
        cover_dir = QString("%1/.gereqi/album-art/").arg(getenv["HOME"])
        cover = QString("%1%2.jpg").arg(cover_dir).arg(self.__filenamer(artist, album))
        
        # Check=False just provides a filename creator. Used when track has
        # changed but not the album
        if check is True:
            # Place to save the covers doesn't exist
            if QDir(cover_dir).exists() is False:
                QDir().mkdir(cover_dir)
            
            if QFile(cover).exists() is True:
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
