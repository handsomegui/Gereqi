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
from database import Media

HTML = '''
            <html>
            <head>
            
            <style type="text/css">
            img.cover{
                width: 240px;
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
            }
            </style>
            </head>
            
            <body>
            <h1>%s - %s</h1>
            <h2>%s</h2>
            <img class="cover" src="%s"/>
            <h1>Albums by %s</h1>
            %s
            </body>
            </html>
            '''
            
class InfoPage:
    def __init__(self, parent=None):
        return
    def __gen_info(self):
        return
        
    def __gen_albs(self, artist, albums):
        tmpl = '''<img class="mini" src="%s" /> %s<br>\n'''
        thing = ""
        for alb in albums:
            cover = Extraneous().get_cover_source(artist, alb)
            thing += tmpl % (cover, alb)
        return "<p>%s</p>" % thing
        
        
    def gen_info(self, **params):
        albs = Media().get_albums(params["artist"])
        cover = Extraneous().get_cover_source(params["artist"], params["album"])
        now = HTML % (params["title"], params["artist"], params["album"], 
                                cover, params["artist"], self.__gen_albs(params["artist"], albs))
        return now
        
        
        
        
        
        
