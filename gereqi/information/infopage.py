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

from PyQt4.QtCore import QString

from gereqi.extraneous import Extraneous
from gereqi.storage.Settings import Settings
from gereqi.storage.Collection import CollectionDb

import styles


HTML = QString('''
    <html>
    <head>    
        %1
    </head>
    
    <body>
        <h1>%3 - %4</h1>
        <h2>%5</h2>
        <img class="cover" src="%6"/>
    
    <div id="albums">
        <h1>Albums by %4</h1>
            %7
    </div>
    </body>
    </html>
            ''')

ALB_HTML = QString('''
    <div id="album">
        <p>
            <a href="#"><img class="mini" src="%1"></a>
            <a href="#">%2</a>
        </p>
        <div class="tracks">
        <ul>
            %3
        </ul>
        </div>
    </div>

''')

TRACK_HTML = QString('''
<li><b>%1 :</b> %2</li>
''')
            
class InfoPage:
    def __init__(self, parent=None):
        return

    def __gen_albs(self, artist, albums):
        thing = QString()
        # Have to create a new qstring as passing a qstring into
        # a function seems to be passing a pointer thus changes are
        # carried back through to its sort. Very unpythonic.
        artist = QString(artist)
        extra = Extraneous()
        # TODO: close connection
        media_db = CollectionDb("infopage")    
        
        for alb in albums:
            t_info = QString()
            tracks = media_db.get_titles(artist, alb)
            for trk in tracks:
                t_info.append(TRACK_HTML.arg(trk["track"],trk["title"]))
            cover = extra.get_cover_source(artist, QString(alb))
            if cover is not None:
                thing = thing.append(ALB_HTML.arg(cover, alb, t_info))
            else:
                thing = thing.append(ALB_HTML.arg("file://", alb, t_info))
                
        # FIXME: causes crash on track change
#        media_db.close_connection("infopage")
        return thing
        
        
    def gen_info(self, **params):
        sets_db = Settings()
        coversize = sets_db.get_interface_setting("coversize")
        coversize = int(coversize) if coversize is not None else 200
        extra = Extraneous()
        cover = extra.get_cover_source(QString(params["artist"]), 
                                       QString(params["album"]), 
                                       params["check"])
        
        cover = cover if cover is not None else "file://"
        
        now = HTML.arg("%1").arg(styles.infostyles)
        now = now.arg("%2").arg(coversize)
        now = now.arg("%3").arg(params["title"])
        now = now.arg("%4").arg(params["artist"])
        now = now.arg("%5").arg(params["album"])
        now = now.arg("%6").arg(cover)
        now = now.arg("%7").arg(self.__gen_albs(params["artist"], 
                                                params["albums"]))
        
        return now
        
        
        
        
        
        
