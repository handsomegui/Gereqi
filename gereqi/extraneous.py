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


from PyQt4.QtCore import QDir, QFile, QIODevice
from os import path, mkdir, environ

from information.webinfo import Webinfo


def __filenamer(artist='', album=''):
    things = []
    excludes = '''!,.%%$&(){}[]/"'''
    for ch in excludes:
        artist = artist.replace(ch, '')
    artist = artist.replace(" ", "_")
    things.append(artist)
    
    for ch in excludes:
        album = album.replace(ch,'')
    album = album.replace(" ", "_")
    things.append(album)
    result = "%s-%s" % (things[0], things[1])
    return result

#TODO: look in the item's folder for cover.jpg etc if the album is in the dir-name
def get_cover_source(artist='', album='', check=True, download=True):
    """
    Find the source for the cover of a given album
    """
    cover_dir = "%s/.gereqi/album-art/" % environ["HOME"]
    fname = __filenamer(artist, album)
    fname = fname.replace('/', '_')
    cover = "%s%s.jpg" % (cover_dir, fname)
    
    # Check=False just provides a filename creator. Used when track has
    # changed but not the album
    if check:
        # Place to save the covers doesn't exist
        if path.exists(cover_dir) is False:
            mkdir(cover_dir, 0700)
        try:
            if path.exists(cover):
                return "file://%s" % cover
            elif download == True:                 
                web_info = Webinfo()
                img = web_info.get_cover(artist, album)
                if img:
                    now = open(cover, "wb")
                    now.write(img)
                    now.close()
                    return "file://%s" % cover
        except UnicodeEncodeError, err:
            print("ERROR: %s" % err)
    else:
        return "file://%s" % cover
