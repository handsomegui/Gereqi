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

from extraneous import Extraneous
from settings import Settings
from PyQt4.QtCore import QString

# TODO: put some javascript in here where it loops through a list
HTML = QString('''
            <html>
            <head>
            
            <style type="text/css">
            img.cover{
                width: %1px;
                border: 0;
            }
            img.mini{
                width: 48px;
                height: 48px;
                border: 0;
            }
            h1{
                text-align: left;
                font-size: 1em;
                font-weight: bold;
            }
            h2{
                text-align: left;
                font-size: 0.9em;
            }
            ul{
                list-style-type: none;
                font-size: 0.8em;
            }
            </style>
            </head>
            
            <body>
            <h1>%2 - %3</h1>
            <h2>%4</h2>
            <img class="cover" src="%5"/>
            <h1>Albums by %3</h1>
            %6
            </body>
            </html>
            ''')
            
class InfoPage:
    def __init__(self, parent=None):
        return

    def __gen_albs(self, artist, albums):
        tmpl = QString('''<img class="mini" src="%1" /> %2<br>\n''')
        thing = QString()
        # Have to create a new qstring as passing a qstring into
        # a function seems to be passing a pointer thus changes are
        # carried back through to its sort. Very unpythonic.
        artist = QString(artist)
        extra = Extraneous()        
        
        for alb in albums:
            cover = extra.get_cover_source(artist, QString(alb))
            if cover is not None:
                thing = thing.append(tmpl.arg(cover, alb))
            else:
                thing = thing.append(tmpl.arg("file://", alb))

        html = QString("<p>%1</p>").arg(thing)
        return html
        
        
    def gen_info(self, **params):
        sets_db = Settings()
        coversize = sets_db.get_interface_setting("coversize")
        coversize = int(coversize) if coversize is not None else 200
        extra = Extraneous()
        cover = extra.get_cover_source(QString(params["artist"]), 
                                       QString(params["album"]), 
                                       params["check"])
        
        cover = cover if cover is not None else "file://"
        
        now = HTML.arg("%1").arg(coversize)
        now = now.arg("%2").arg(params["title"])
        now = now.arg("%3").arg(params["artist"])
        now = now.arg("%4").arg(params["album"])
        now = now.arg("%5").arg(cover)
        now = now.arg("%6").arg(self.__gen_albs(params["artist"], 
                                                params["albums"]))
        return now
        
        
        
        
        
        
