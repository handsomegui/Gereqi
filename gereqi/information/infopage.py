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

from gereqi.extraneous import Extraneous
from gereqi.storage.Settings import Settings
from gereqi.storage.Collection import CollectionDb

import styles


HTML = '''
    <html>
    <head>    
        %(style)s
    </head>
    
    <body>
        <h1>%(title)s - %(artist)s</h1>
        <h2>%(album)s</h2>
        <img class="cover" src="%(cover)s"/>
    
    <div id="albums">
        <h1>Albums by %(artist)s</h1>
            %(albums)s
    </div>
    </body>
    </html>
            '''

ALB_HTML = '''
    <div id="album">
        <p>
            <a href="#"><img class="mini" src="%(cover)s"></a>
            <a href="#">%(album)s</a>
        </p>
        <div class="tracks">
        <ul>
            %(tracks)s
        </ul>
        </div>
    </div>

        '''

TRACK_HTML = '''<li><b>%(track)s :</b> %(title)s</li>'''

            
class InfoPage:
    def __init__(self, parent=None):
        return

    def __gen_albs(self, artist, albums):
        thing = ""
        extra = Extraneous()
        media_db = CollectionDb("infopage")    
        
        for alb in albums:
            t_info = ""
            tracks = media_db.get_titles(artist, alb)
            for trk in tracks:
                t_info += TRACK_HTML % {'track': trk["track"],'title': trk["title"]}
            cover = extra.get_cover_source(artist, alb)
            if cover is None:
                cover = "file://"
            thing += ALB_HTML % {'cover':cover, 'album' :alb, 'tracks': t_info}

        return thing
        
        
    def gen_info(self, **params):
        sets_db = Settings()
        coversize = sets_db.get_interface_setting("coversize")
        coversize = int(coversize) if coversize is not None else 200
        extra = Extraneous()
        cover = extra.get_cover_source(params["artist"], 
                                       params["album"], 
                                       params["check"])
        
        cover = cover if cover is not None else "file://"
        
        now = HTML % {}
        
#        now = HTML.arg("%1").arg(styles.infostyles)
#        now = now.arg("%2").arg(coversize)
#        now = now.arg("%3").arg(params["title"])
#        now = now.arg("%4").arg(params["artist"])
#        now = now.arg("%5").arg(params["album"])
#        now = now.arg("%6").arg(cover)
#        now = now.arg("%7").arg(self.__gen_albs(params["artist"], 
#                                                params["albums"]))
        
        return now
        
        
        
        
        
        
