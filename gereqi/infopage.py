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



HTML = '''
            <html>
            <head>
            <style type="text/css">
            h1{
                text-align: left;
                font-size: 1em;
                font-weight: bold;
            }
            h2{
                text-align: left;
                font-size: 0.9em;
            }
            ul{list-style-type: none;}
            </style>
            </head>
            
            <body>
            <h1>%s - %s</h1>
            <h2>%s</h2>
            <img border="0" src="%s" width="200" />
            <h1>Albums by %s</h1>
            <p>%s</p>
            </body>
            </html>
            '''
            
class InfoPage:
    def __init__(self, parent):
        self.ui_main = parent
        
    def __gen_info(self):
        return
        
    def __gen_albs(self, albums):
        tmpl = '''<li>%s</li>'''
        thing = "<ul>"
        for alb in albums:
            thing += tmpl % alb
        return thing
        
        
    def set_info(self, info):
        albs = self.ui_main.media_db.get_albums(info["artist"])
        
        now = HTML % (info["title"], info["artist"], info["album"], 
                                info["cover"], info["artist"], self.__gen_albs(albs))
        print now
        self.ui_main.info_view.setHtml(now)
        
        
        
        
        
        
